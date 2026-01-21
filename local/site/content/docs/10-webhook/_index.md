---
title: "Webhook"
weight: 10
---


## Overview

The `pkg/webhook` package provides support for implementing Kubernetes admission webhooks (validating and mutating) and conversion webhooks for CRD version conversion.

## Package Location

```
pkg/webhook/
├── webhook.go              # Webhook server
├── server.go               # HTTP server implementation
├── admission/              # Admission webhooks
│   ├── webhook.go          # Admission webhook handler
│   ├── validator.go        # Validator interface
│   ├── defaulter.go        # Defaulter interface
│   └── response.go         # Admission response
├── conversion/             # Conversion webhooks
│   └── conversion.go       # Conversion webhook
└── authentication/         # Authentication webhooks
    └── http.go             # Token review webhook
```

## Core Concepts

### Webhook Types

<div class="mermaid-diagram">
<img src="/images/diagrams/diagram-5dc74cc6d4b8.svg" alt="Diagram" />
</div>


## Admission Webhooks

### Webhook Flow

<div class="mermaid-diagram">
<img src="/images/diagrams/diagram-4cfedde66cbe.svg" alt="Diagram" />
</div>


## Webhook Server

### Creating a Webhook Server

```go
import (
    "sigs.k8s.io/controller-runtime/pkg/webhook"
)

// Get webhook server from manager
webhookServer := mgr.GetWebhookServer()

// Configure webhook server
mgr, err := ctrl.NewManager(cfg, ctrl.Options{
    WebhookServer: webhook.NewServer(webhook.Options{
        Port:    9443,
        CertDir: "/tmp/k8s-webhook-server/serving-certs",
        CertName: "tls.crt",
        KeyName:  "tls.key",
    }),
})
```

### Registering Webhooks

```go
// Register admission webhook
webhookServer.Register("/mutate-v1-pod", &webhook.Admission{
    Handler: &PodDefaulter{},
})

webhookServer.Register("/validate-v1-pod", &webhook.Admission{
    Handler: &PodValidator{},
})
```

## Mutating Webhooks (Defaulter)

### Defaulter Interface

```go
type Defaulter interface {
    Default()
}
```

### Implementing a Defaulter

```go
import (
    corev1 "k8s.io/api/core/v1"
    "sigs.k8s.io/controller-runtime/pkg/webhook/admission"
)

type PodDefaulter struct{}

// Default implements admission.Defaulter
func (d *PodDefaulter) Default(ctx context.Context, obj runtime.Object) error {
    pod, ok := obj.(*corev1.Pod)
    if !ok {
        return fmt.Errorf("expected a Pod but got a %T", obj)
    }
    
    // Set default values
    if pod.Labels == nil {
        pod.Labels = make(map[string]string)
    }
    pod.Labels["defaulted"] = "true"
    
    // Set default container resources
    for i := range pod.Spec.Containers {
        if pod.Spec.Containers[i].Resources.Requests == nil {
            pod.Spec.Containers[i].Resources.Requests = corev1.ResourceList{
                corev1.ResourceCPU:    resource.MustParse("100m"),
                corev1.ResourceMemory: resource.MustParse("128Mi"),
            }
        }
    }
    
    return nil
}

// Register with builder
err := ctrl.NewWebhookManagedBy(mgr).
    For(&corev1.Pod{}).
    WithDefaulter(&PodDefaulter{}).
    Complete()
```

### CustomDefaulter

For more control, implement CustomDefaulter:

```go
type CustomDefaulter interface {
    Default(ctx context.Context, obj runtime.Object) error
}

type PodCustomDefaulter struct {
    Client client.Client
}

func (d *PodCustomDefaulter) Default(ctx context.Context, obj runtime.Object) error {
    pod := obj.(*corev1.Pod)
    
    // Can use client for lookups
    var configMap corev1.ConfigMap
    if err := d.Client.Get(ctx, types.NamespacedName{
        Name:      "defaults",
        Namespace: pod.Namespace,
    }, &configMap); err == nil {
        // Apply defaults from ConfigMap
        if cpu, ok := configMap.Data["default-cpu"]; ok {
            // Apply CPU default
        }
    }
    
    return nil
}
```

## Validating Webhooks (Validator)

### Validator Interface

```go
type Validator interface {
    ValidateCreate(ctx context.Context, obj runtime.Object) (warnings admission.Warnings, error)
    ValidateUpdate(ctx context.Context, oldObj, newObj runtime.Object) (warnings admission.Warnings, error)
    ValidateDelete(ctx context.Context, obj runtime.Object) (warnings admission.Warnings, error)
}
```

### Implementing a Validator

```go
type PodValidator struct{}

func (v *PodValidator) ValidateCreate(ctx context.Context, obj runtime.Object) (admission.Warnings, error) {
    pod, ok := obj.(*corev1.Pod)
    if !ok {
        return nil, fmt.Errorf("expected a Pod but got a %T", obj)
    }
    
    // Validate pod
    if len(pod.Spec.Containers) == 0 {
        return nil, fmt.Errorf("pod must have at least one container")
    }
    
    // Check container names
    for _, container := range pod.Spec.Containers {
        if container.Name == "" {
            return nil, fmt.Errorf("container name cannot be empty")
        }
        if container.Image == "" {
            return nil, fmt.Errorf("container %s must have an image", container.Name)
        }
    }
    
    // Return warnings (non-blocking)
    var warnings admission.Warnings
    if pod.Spec.RestartPolicy == "" {
        warnings = append(warnings, "restartPolicy not set, defaulting to Always")
    }
    
    return warnings, nil
}

func (v *PodValidator) ValidateUpdate(ctx context.Context, oldObj, newObj runtime.Object) (admission.Warnings, error) {
    oldPod := oldObj.(*corev1.Pod)
    newPod := newObj.(*corev1.Pod)
    
    // Validate immutable fields
    if oldPod.Spec.ServiceAccountName != newPod.Spec.ServiceAccountName {
        return nil, fmt.Errorf("serviceAccountName is immutable")
    }
    
    // Run create validation
    return v.ValidateCreate(ctx, newObj)
}

func (v *PodValidator) ValidateDelete(ctx context.Context, obj runtime.Object) (admission.Warnings, error) {
    pod := obj.(*corev1.Pod)
    
    // Prevent deletion of critical pods
    if pod.Labels["critical"] == "true" {
        return nil, fmt.Errorf("cannot delete critical pod")
    }
    
    return nil, nil
}

// Register with builder
err := ctrl.NewWebhookManagedBy(mgr).
    For(&corev1.Pod{}).
    WithValidator(&PodValidator{}).
    Complete()
```

### CustomValidator

For more control:

```go
type CustomValidator interface {
    ValidateCreate(ctx context.Context, obj runtime.Object) (warnings admission.Warnings, error)
    ValidateUpdate(ctx context.Context, oldObj, newObj runtime.Object) (warnings admission.Warnings, error)
    ValidateDelete(ctx context.Context, obj runtime.Object) (warnings admission.Warnings, error)
}

type PodCustomValidator struct {
    Client client.Client
}

func (v *PodCustomValidator) ValidateCreate(ctx context.Context, obj runtime.Object) (admission.Warnings, error) {
    pod := obj.(*corev1.Pod)
    
    // Can use client for validation
    var namespace corev1.Namespace
    if err := v.Client.Get(ctx, types.NamespacedName{
        Name: pod.Namespace,
    }, &namespace); err != nil {
        return nil, fmt.Errorf("namespace not found: %w", err)
    }
    
    // Validate based on namespace labels
    if namespace.Labels["environment"] == "production" {
        // Stricter validation for production
        if pod.Spec.PriorityClassName == "" {
            return nil, fmt.Errorf("production pods must have priorityClassName")
        }
    }
    
    return nil, nil
}
```

## Combined Defaulter and Validator

```go
type PodWebhook struct {
    Client client.Client
}

// Implement both interfaces
func (w *PodWebhook) Default(ctx context.Context, obj runtime.Object) error {
    pod := obj.(*corev1.Pod)
    // Set defaults
    if pod.Labels == nil {
        pod.Labels = make(map[string]string)
    }
    pod.Labels["defaulted"] = "true"
    return nil
}

func (w *PodWebhook) ValidateCreate(ctx context.Context, obj runtime.Object) (admission.Warnings, error) {
    pod := obj.(*corev1.Pod)
    // Validate
    if len(pod.Spec.Containers) == 0 {
        return nil, fmt.Errorf("pod must have at least one container")
    }
    return nil, nil
}

func (w *PodWebhook) ValidateUpdate(ctx context.Context, oldObj, newObj runtime.Object) (admission.Warnings, error) {
    return w.ValidateCreate(ctx, newObj)
}

func (w *PodWebhook) ValidateDelete(ctx context.Context, obj runtime.Object) (admission.Warnings, error) {
    return nil, nil
}

// Register both
err := ctrl.NewWebhookManagedBy(mgr).
    For(&corev1.Pod{}).
    WithDefaulter(&PodWebhook{Client: mgr.GetClient()}).
    WithValidator(&PodWebhook{Client: mgr.GetClient()}).
    Complete()
```

## Webhook Builder

### Basic Webhook

```go
err := ctrl.NewWebhookManagedBy(mgr).
    For(&myv1.MyResource{}).
    WithDefaulter(&MyResourceDefaulter{}).
    WithValidator(&MyResourceValidator{}).
    Complete()
```

### Custom Path

```go
err := ctrl.NewWebhookManagedBy(mgr).
    For(&myv1.MyResource{}).
    WithDefaulter(&MyResourceDefaulter{}).
    WithPath("/mutate-mygroup-v1-myresource").
    Complete()
```

### Custom Log Constructor

```go
err := ctrl.NewWebhookManagedBy(mgr).
    For(&myv1.MyResource{}).
    WithValidator(&MyResourceValidator{}).
    WithLogConstructor(func(base logr.Logger, req *admission.Request) logr.Logger {
        return base.WithValues(
            "webhook", "myresource-validator",
            "name", req.Name,
            "namespace", req.Namespace,
            "operation", req.Operation,
        )
    }).
    Complete()
```

## Conversion Webhooks

For CRD version conversion:

```go
import "sigs.k8s.io/controller-runtime/pkg/webhook/conversion"

// Implement Hub interface on one version
type MyResourceV1 struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`
    Spec   MyResourceV1Spec   `json:"spec,omitempty"`
    Status MyResourceV1Status `json:"status,omitempty"`
}

// Hub marks this as the hub version
func (*MyResourceV1) Hub() {}

// Implement Convertible on other versions
type MyResourceV2 struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`
    Spec   MyResourceV2Spec   `json:"spec,omitempty"`
    Status MyResourceV2Status `json:"status,omitempty"`
}

// ConvertTo converts this version to the Hub version
func (src *MyResourceV2) ConvertTo(dstRaw conversion.Hub) error {
    dst := dstRaw.(*MyResourceV1)
    // Conversion logic
    dst.Spec.Field1 = src.Spec.NewField1
    return nil
}

// ConvertFrom converts from the Hub version to this version
func (dst *MyResourceV2) ConvertFrom(srcRaw conversion.Hub) error {
    src := srcRaw.(*MyResourceV1)
    // Conversion logic
    dst.Spec.NewField1 = src.Spec.Field1
    return nil
}

// Register conversion webhook
err := ctrl.NewWebhookManagedBy(mgr).
    For(&MyResourceV2{}).
    Complete()
```

## Webhook Configuration

### Kubernetes Webhook Configuration

You need to create a `ValidatingWebhookConfiguration` or `MutatingWebhookConfiguration`:

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: MutatingWebhookConfiguration
metadata:
  name: myresource-mutating-webhook
webhooks:
  - name: myresource.example.com
    clientConfig:
      service:
        name: webhook-service
        namespace: default
        path: /mutate-mygroup-v1-myresource
      caBundle: <base64-encoded-ca-cert>
    rules:
      - operations: ["CREATE", "UPDATE"]
        apiGroups: ["mygroup.example.com"]
        apiVersions: ["v1"]
        resources: ["myresources"]
    admissionReviewVersions: ["v1"]
    sideEffects: None
```

### Certificate Management

Controller-runtime provides certificate management:

```go
import "sigs.k8s.io/controller-runtime/pkg/webhook"

mgr, err := ctrl.NewManager(cfg, ctrl.Options{
    WebhookServer: webhook.NewServer(webhook.Options{
        Port:    9443,
        CertDir: "/tmp/k8s-webhook-server/serving-certs",
    }),
})
```

Or use cert-manager for automatic certificate management.

## Best Practices

### 1. Validate Early

```go
func (v *Validator) ValidateCreate(ctx context.Context, obj runtime.Object) (admission.Warnings, error) {
    // Type check first
    pod, ok := obj.(*corev1.Pod)
    if !ok {
        return nil, fmt.Errorf("expected Pod, got %T", obj)
    }
    
    // Validate
    return nil, nil
}
```

### 2. Use Warnings for Non-Critical Issues

```go
var warnings admission.Warnings
if pod.Spec.RestartPolicy == "" {
    warnings = append(warnings, "restartPolicy not set")
}
return warnings, nil
```

### 3. Keep Webhooks Fast

Webhooks block API requests, so keep them fast:
- Avoid expensive operations
- Use timeouts for external calls
- Cache frequently accessed data

### 4. Handle All Operations

```go
func (v *Validator) ValidateCreate(ctx context.Context, obj runtime.Object) (admission.Warnings, error) {
    // Implement
    return nil, nil
}

func (v *Validator) ValidateUpdate(ctx context.Context, oldObj, newObj runtime.Object) (admission.Warnings, error) {
    // Implement
    return nil, nil
}

func (v *Validator) ValidateDelete(ctx context.Context, obj runtime.Object) (admission.Warnings, error) {
    // Implement
    return nil, nil
}
```

### 5. Use Immutability Checks

```go
func (v *Validator) ValidateUpdate(ctx context.Context, oldObj, newObj runtime.Object) (admission.Warnings, error) {
    oldRes := oldObj.(*MyResource)
    newRes := newObj.(*MyResource)
    
    // Check immutable fields
    if oldRes.Spec.ImmutableField != newRes.Spec.ImmutableField {
        return nil, fmt.Errorf("immutableField cannot be changed")
    }
    
    return nil, nil
}
```

## Common Patterns

### 1. Namespace-Based Validation

```go
func (v *Validator) ValidateCreate(ctx context.Context, obj runtime.Object) (admission.Warnings, error) {
    pod := obj.(*corev1.Pod)
    
    if pod.Namespace == "production" {
        // Stricter validation for production
        if pod.Spec.PriorityClassName == "" {
            return nil, fmt.Errorf("production pods must have priorityClassName")
        }
    }
    
    return nil, nil
}
```

### 2. Label-Based Defaulting

```go
func (d *Defaulter) Default(ctx context.Context, obj runtime.Object) error {
    pod := obj.(*corev1.Pod)
    
    if pod.Labels == nil {
        pod.Labels = make(map[string]string)
    }
    
    // Add standard labels
    pod.Labels["managed-by"] = "my-controller"
    pod.Labels["created-at"] = time.Now().Format(time.RFC3339)
    
    return nil
}
```

### 3. Cross-Field Validation

```go
func (v *Validator) ValidateCreate(ctx context.Context, obj runtime.Object) (admission.Warnings, error) {
    res := obj.(*MyResource)
    
    // Validate field combinations
    if res.Spec.Type == "advanced" && res.Spec.Config == nil {
        return nil, fmt.Errorf("advanced type requires config")
    }
    
    return nil, nil
}
```

## Common Pitfalls

### 1. Blocking Webhooks

```go
// BAD - slow operation blocks API requests
func (v *Validator) ValidateCreate(ctx context.Context, obj runtime.Object) (admission.Warnings, error) {
    time.Sleep(10 * time.Second) // Don't do this!
    return nil, nil
}

// GOOD - fast validation
func (v *Validator) ValidateCreate(ctx context.Context, obj runtime.Object) (admission.Warnings, error) {
    // Quick checks only
    return nil, nil
}
```

### 2. Not Handling All Operations

```go
// BAD - only implements ValidateCreate
type Validator struct{}

func (v *Validator) ValidateCreate(ctx context.Context, obj runtime.Object) (admission.Warnings, error) {
    return nil, nil
}
// Missing ValidateUpdate and ValidateDelete

// GOOD - implement all methods
```

### 3. Mutating in Validator

```go
// BAD - mutating in validator
func (v *Validator) ValidateCreate(ctx context.Context, obj runtime.Object) (admission.Warnings, error) {
    pod := obj.(*corev1.Pod)
    pod.Labels["validated"] = "true" // Don't mutate!
    return nil, nil
}

// GOOD - only validate
func (v *Validator) ValidateCreate(ctx context.Context, obj runtime.Object) (admission.Warnings, error) {
    pod := obj.(*corev1.Pod)
    // Only check, don't modify
    if pod.Labels["required"] == "" {
        return nil, fmt.Errorf("required label missing")
    }
    return nil, nil
}
```

## Related Packages

- [Manager Package](/docs/01-manager/) - Manages webhook server
- [Builder Package](/docs/04-builder/) - Builds webhooks
- [Client Package](/docs/05-client/) - Used in webhook handlers
