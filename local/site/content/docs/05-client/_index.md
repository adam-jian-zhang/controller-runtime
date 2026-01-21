---
title: "Client"
weight: 5
---


## Overview

The `pkg/client` package provides a unified, type-safe interface for interacting with Kubernetes API servers. It abstracts the complexity of client-go and provides a consistent API for reading and writing Kubernetes objects.

## Package Location

```
pkg/client/
├── client.go               # Main client implementation
├── interfaces.go           # Client interfaces
├── options.go              # Client options
├── patch.go                # Patch implementations
├── typed_client.go         # Typed client
├── unstructured_client.go  # Unstructured client
├── metadata_client.go      # Metadata-only client
├── fake/                   # Fake client for testing
├── apiutil/                # API utilities
├── config/                 # Config utilities
└── interceptor/            # Client interceptors
```

## Core Concepts

### Client Architecture

<div class="mermaid-diagram">
<img src="/images/diagrams/diagram-922e86d6a44a.svg" alt="Diagram" />
</div>


## Client Interface

The Client interface combines Reader, Writer, and StatusClient:

```go
type Client interface {
    Reader
    Writer
    StatusClient
    SubResourceClientConstructor
    
    // Scheme returns the scheme this client is using
    Scheme() *runtime.Scheme
    
    // RESTMapper returns the REST mapper
    RESTMapper() meta.RESTMapper
    
    // GroupVersionKindFor returns the GroupVersionKind for the given object
    GroupVersionKindFor(obj runtime.Object) (schema.GroupVersionKind, error)
    
    // IsObjectNamespaced returns true if the object is namespaced
    IsObjectNamespaced(obj runtime.Object) (bool, error)
}
```

## Reader Interface

The Reader interface provides read operations:

```go
type Reader interface {
    // Get retrieves an object
    Get(ctx context.Context, key ObjectKey, obj Object, opts ...GetOption) error
    
    // List retrieves a list of objects
    List(ctx context.Context, list ObjectList, opts ...ListOption) error
}
```

### Get Operation

```go
import (
    "context"
    corev1 "k8s.io/api/core/v1"
    "k8s.io/apimachinery/pkg/types"
    "sigs.k8s.io/controller-runtime/pkg/client"
)

// Get a Pod
var pod corev1.Pod
err := c.Get(ctx, types.NamespacedName{
    Name:      "my-pod",
    Namespace: "default",
}, &pod)

// Get with options
err = c.Get(ctx, key, &pod, &client.GetOptions{
    Raw: &metav1.GetOptions{
        ResourceVersion: "12345",
    },
})
```

### List Operation

```go
// List all Pods in a namespace
var podList corev1.PodList
err := c.List(ctx, &podList, &client.ListOptions{
    Namespace: "default",
})

// List with label selector
err = c.List(ctx, &podList, client.InNamespace("default"),
    client.MatchingLabels{"app": "myapp"})

// List with field selector
err = c.List(ctx, &podList, client.InNamespace("default"),
    client.MatchingFields{"spec.nodeName": "node-1"})

// List all across all namespaces
err = c.List(ctx, &podList)
```

## Writer Interface

The Writer interface provides write operations:

```go
type Writer interface {
    // Create saves a new object
    Create(ctx context.Context, obj Object, opts ...CreateOption) error
    
    // Delete deletes an object
    Delete(ctx context.Context, obj Object, opts ...DeleteOption) error
    
    // Update updates an existing object
    Update(ctx context.Context, obj Object, opts ...UpdateOption) error
    
    // Patch patches an existing object
    Patch(ctx context.Context, obj Object, patch Patch, opts ...PatchOption) error
    
    // DeleteAllOf deletes all objects matching the given options
    DeleteAllOf(ctx context.Context, obj Object, opts ...DeleteAllOfOption) error
}
```

### Create Operation

```go
// Create a Pod
pod := &corev1.Pod{
    ObjectMeta: metav1.ObjectMeta{
        Name:      "my-pod",
        Namespace: "default",
    },
    Spec: corev1.PodSpec{
        Containers: []corev1.Container{{
            Name:  "nginx",
            Image: "nginx:latest",
        }},
    },
}
err := c.Create(ctx, pod)

// Create with options
err = c.Create(ctx, pod, &client.CreateOptions{
    FieldManager: "my-controller",
})
```

### Update Operation

```go
// Get the object first
var pod corev1.Pod
err := c.Get(ctx, key, &pod)
if err != nil {
    return err
}

// Modify the object
pod.Spec.Containers[0].Image = "nginx:1.21"

// Update
err = c.Update(ctx, &pod)

// Update with options
err = c.Update(ctx, &pod, &client.UpdateOptions{
    FieldManager: "my-controller",
})
```

### Patch Operation

```go
import "sigs.k8s.io/controller-runtime/pkg/client"

// Strategic Merge Patch
patch := client.MergeFrom(pod.DeepCopy())
pod.Labels["new-label"] = "value"
err := c.Patch(ctx, &pod, patch)

// JSON Patch
jsonPatch := client.RawPatch(types.JSONPatchType, []byte(`[
    {"op": "replace", "path": "/spec/replicas", "value": 3}
]`))
err = c.Patch(ctx, &deployment, jsonPatch)

// Merge Patch
mergePatch := client.RawPatch(types.MergePatchType, []byte(`{
    "metadata": {
        "labels": {
            "new-label": "value"
        }
    }
}`))
err = c.Patch(ctx, &pod, mergePatch)
```

### Delete Operation

```go
// Delete a Pod
pod := &corev1.Pod{
    ObjectMeta: metav1.ObjectMeta{
        Name:      "my-pod",
        Namespace: "default",
    },
}
err := c.Delete(ctx, pod)

// Delete with options
err = c.Delete(ctx, pod, &client.DeleteOptions{
    GracePeriodSeconds: ptr.To(int64(30)),
    PropagationPolicy:  ptr.To(metav1.DeletePropagationForeground),
})

// DeleteAllOf - delete all matching objects
err = c.DeleteAllOf(ctx, &corev1.Pod{},
    client.InNamespace("default"),
    client.MatchingLabels{"app": "myapp"})
```

## Status SubResource

The StatusClient provides access to the status subresource:

```go
// Update status
var deployment appsv1.Deployment
err := c.Get(ctx, key, &deployment)
if err != nil {
    return err
}

deployment.Status.Replicas = 3
deployment.Status.ReadyReplicas = 3

// Update only the status subresource
err = c.Status().Update(ctx, &deployment)

// Patch status
patch := client.MergeFrom(deployment.DeepCopy())
deployment.Status.Conditions = append(deployment.Status.Conditions, condition)
err = c.Status().Patch(ctx, &deployment, patch)
```

## SubResource Client

Access other subresources:

```go
// ServiceAccount token creation
sa := &corev1.ServiceAccount{
    ObjectMeta: metav1.ObjectMeta{
        Namespace: "default",
        Name:      "my-sa",
    },
}
token := &authenticationv1.TokenRequest{
    Spec: authenticationv1.TokenRequestSpec{
        ExpirationSeconds: ptr.To(int64(3600)),
    },
}
err := c.SubResource("token").Create(ctx, sa, token)

// Pod eviction
pod := &corev1.Pod{
    ObjectMeta: metav1.ObjectMeta{
        Namespace: "default",
        Name:      "my-pod",
    },
}
eviction := &policyv1.Eviction{
    DeleteOptions: &metav1.DeleteOptions{
        GracePeriodSeconds: ptr.To(int64(30)),
    },
}
err = c.SubResource("eviction").Create(ctx, pod, eviction)

// Scale subresource
deployment := &appsv1.Deployment{
    ObjectMeta: metav1.ObjectMeta{
        Namespace: "default",
        Name:      "my-deployment",
    },
}
scale := &autoscalingv1.Scale{}
err = c.SubResource("scale").Get(ctx, deployment, scale)

scale.Spec.Replicas = 5
err = c.SubResource("scale").Update(ctx, deployment, client.WithSubResourceBody(scale))
```

## Client Types

### 1. Default Split Client

The default client reads from cache and writes to API server:

```go
// Provided by manager
client := mgr.GetClient()

// Reads come from cache
var pod corev1.Pod
err := client.Get(ctx, key, &pod) // From cache

// Writes go to API server
err = client.Update(ctx, &pod) // To API server
```

<div class="mermaid-diagram">
<img src="/images/diagrams/diagram-acd9bd667685.svg" alt="Diagram" />
</div>


### 2. Direct Client (API Reader)

Reads directly from API server, bypassing cache:

```go
// Get API reader from manager
apiReader := mgr.GetAPIReader()

// Always reads from API server
var pod corev1.Pod
err := apiReader.Get(ctx, key, &pod) // From API server, not cache
```

**Use cases**:
- Need most up-to-date data
- Verify cache consistency
- Read resources not in cache

### 3. Fake Client

For testing:

```go
import "sigs.k8s.io/controller-runtime/pkg/client/fake"

// Create fake client with initial objects
fakeClient := fake.NewClientBuilder().
    WithScheme(scheme).
    WithObjects(&pod1, &pod2).
    WithStatusSubresource(&pod1).
    Build()

// Use like a real client
err := fakeClient.Get(ctx, key, &pod)
err = fakeClient.Update(ctx, &pod)
```

## List Options

### Namespace Filtering

```go
// Single namespace
client.InNamespace("default")

// All namespaces (default)
// No namespace option
```

### Label Selectors

```go
// Match specific labels
client.MatchingLabels{"app": "myapp", "env": "prod"}

// Label selector
selector, _ := labels.Parse("app=myapp,env!=dev")
client.MatchingLabelsSelector{Selector: selector}
```

### Field Selectors

```go
// Match specific fields
client.MatchingFields{"spec.nodeName": "node-1"}

// Field selector
selector, _ := fields.ParseSelector("spec.nodeName=node-1")
client.MatchingFieldsSelector{Selector: selector}
```

### Limit and Continue

```go
// Limit results
client.Limit(100)

// Continue token for pagination
client.Continue("token-from-previous-list")
```

### Combined Options

```go
err := c.List(ctx, &podList,
    client.InNamespace("default"),
    client.MatchingLabels{"app": "myapp"},
    client.MatchingFields{"spec.nodeName": "node-1"},
    client.Limit(100))
```

## Patch Types

### Strategic Merge Patch

```go
// Create patch from original object
patch := client.MergeFrom(original.DeepCopy())

// Modify object
original.Labels["new-label"] = "value"

// Apply patch
err := c.Patch(ctx, original, patch)
```

### Merge Patch

```go
// JSON merge patch
patch := client.RawPatch(types.MergePatchType, []byte(`{
    "metadata": {
        "labels": {
            "new-label": "value"
        }
    }
}`))
err := c.Patch(ctx, &pod, patch)
```

### JSON Patch

```go
// JSON patch operations
patch := client.RawPatch(types.JSONPatchType, []byte(`[
    {"op": "add", "path": "/metadata/labels/new-label", "value": "value"},
    {"op": "replace", "path": "/spec/replicas", "value": 3}
]`))
err := c.Patch(ctx, &deployment, patch)
```

### Server-Side Apply

```go
// Apply configuration
applyConfig := appsv1ac.Deployment("my-deployment", "default").
    WithSpec(appsv1ac.DeploymentSpec().
        WithReplicas(3))

err := c.Apply(ctx, applyConfig, client.ForceOwnership, client.FieldOwner("my-controller"))
```

## Field Indexing

Add indexes to the cache for efficient lookups:

```go
// Add index on Pod's spec.nodeName field
err := mgr.GetFieldIndexer().IndexField(ctx, &corev1.Pod{}, "spec.nodeName",
    func(obj client.Object) []string {
        pod := obj.(*corev1.Pod)
        return []string{pod.Spec.NodeName}
    })

// List Pods on a specific node using the index
var podList corev1.PodList
err = c.List(ctx, &podList, client.MatchingFields{"spec.nodeName": "node-1"})
```

## Client Interceptors

Intercept client operations for logging, metrics, etc.:

```go
import "sigs.k8s.io/controller-runtime/pkg/client/interceptor"

// Create interceptor
funcs := interceptor.Funcs{
    Get: func(ctx context.Context, client client.WithWatch, key client.ObjectKey, obj client.Object, opts ...client.GetOption) error {
        log.Info("Getting object", "key", key)
        return client.Get(ctx, key, obj, opts...)
    },
}

// Create client with interceptor
c, err := client.NewWithWatch(config, client.Options{
    Scheme: scheme,
    Interceptor: funcs,
})
```

## Best Practices

### 1. Use Context

Always pass context for cancellation and timeouts:

```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

err := c.Get(ctx, key, &pod)
```

### 2. Handle Not Found Errors

```go
err := c.Get(ctx, key, &pod)
if err != nil {
    if apierrors.IsNotFound(err) {
        // Object doesn't exist
        return nil
    }
    return err
}

// Or use helper
err = c.Get(ctx, key, &pod)
return client.IgnoreNotFound(err)
```

### 3. Use Patch Instead of Update

Patches are more efficient and avoid conflicts:

```go
// Instead of Get + Modify + Update
patch := client.MergeFrom(pod.DeepCopy())
pod.Labels["key"] = "value"
err := c.Patch(ctx, &pod, patch)
```

### 4. Update Status Separately

```go
// Update spec
err := c.Update(ctx, &obj)

// Update status
err = c.Status().Update(ctx, &obj)
```

### 5. Use Field Selectors for Indexed Fields

```go
// Add index first
mgr.GetFieldIndexer().IndexField(ctx, &corev1.Pod{}, "spec.nodeName", indexFunc)

// Then use field selector
c.List(ctx, &podList, client.MatchingFields{"spec.nodeName": "node-1"})
```

### 6. Use Fake Client for Testing

```go
fakeClient := fake.NewClientBuilder().
    WithScheme(scheme).
    WithObjects(initialObjects...).
    Build()
```

## Common Patterns

### Create or Update

```go
import "sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"

op, err := controllerutil.CreateOrUpdate(ctx, c, obj, func() error {
    // Mutate obj here
    obj.Spec.Replicas = ptr.To(int32(3))
    return nil
})
// op is one of: Created, Updated, Unchanged
```

### Create or Patch

```go
op, err := controllerutil.CreateOrPatch(ctx, c, obj, func() error {
    // Mutate obj here
    obj.Labels["key"] = "value"
    return nil
})
```

### List and Process

```go
var podList corev1.PodList
err := c.List(ctx, &podList, client.InNamespace("default"))
if err != nil {
    return err
}

for _, pod := range podList.Items {
    // Process each pod
}
```

### Pagination

```go
var continueToken string
for {
    var podList corev1.PodList
    err := c.List(ctx, &podList,
        client.Limit(100),
        client.Continue(continueToken))
    if err != nil {
        return err
    }
    
    // Process pods
    for _, pod := range podList.Items {
        // ...
    }
    
    continueToken = podList.Continue
    if continueToken == "" {
        break
    }
}
```

## Related Packages

- [Cache Package](/docs/06-cache/) - Provides cached reads
- [Manager Package](/docs/01-manager/) - Provides client instances
- [Reconcile Package](/docs/03-reconcile/) - Uses client for reconciliation
