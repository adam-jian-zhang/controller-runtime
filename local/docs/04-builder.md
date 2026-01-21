# Builder Package

## Overview

The `pkg/builder` package provides a fluent, declarative API for constructing controllers and webhooks with minimal boilerplate. It simplifies the process of wiring together sources, handlers, predicates, and reconcilers.

## Package Location

```
pkg/builder/
├── controller.go           # Controller builder implementation
├── webhook.go              # Webhook builder implementation
├── options.go              # Builder options
├── doc.go                  # Package documentation
└── example_test.go         # Usage examples
```

## Core Concepts

### Builder Pattern

The Builder pattern provides a fluent API for configuring controllers:

```mermaid
graph LR
    Start[Start] --> For[For Primary Resource]
    For --> Owns[Owns Child Resources]
    Owns --> Watches[Watches Related Resources]
    Watches --> Options[WithOptions]
    Options --> Complete[Complete with Reconciler]
    Complete --> Controller[Controller Created]
    
    style Start fill:#e1f5ff
    style Controller fill:#c8e6c9
```

## Controller Builder

### Basic Controller Builder

```go
import (
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/builder"
)

// Create a controller builder
err := ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    Owns(&corev1.Pod{}).
    Complete(&DeploymentReconciler{
        Client: mgr.GetClient(),
        Scheme: mgr.GetScheme(),
    })
```

### Builder Methods

```mermaid
graph TB
    Builder[Builder]
    Builder --> For[For - Primary Resource]
    Builder --> Owns[Owns - Owned Resources]
    Builder --> Watches[Watches - Custom Watches]
    Builder --> WithOptions[WithOptions - Controller Options]
    Builder --> WithEventFilter[WithEventFilter - Global Predicates]
    Builder --> Named[Named - Controller Name]
    Builder --> Complete[Complete - Build Controller]
    
    style Builder fill:#e1f5ff
    style For fill:#fff4e1
    style Owns fill:#fff4e1
    style Watches fill:#fff4e1
```

## For Method

The `For` method specifies the primary resource type to reconcile:

```go
// Watch Deployments
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{})

// With options
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}, builder.WithPredicates(predicate.GenerationChangedPredicate{}))

// Metadata-only watch (reduces memory)
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}, builder.OnlyMetadata)
```

### For Options

```go
// WithPredicates adds predicates to the For watch
builder.WithPredicates(
    predicate.GenerationChangedPredicate{},
    predicate.ResourceVersionChangedPredicate{},
)

// OnlyMetadata watches only metadata (not full objects)
builder.OnlyMetadata
```

## Owns Method

The `Owns` method watches resources owned by the primary resource:

```go
// Watch Pods owned by Deployment
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    Owns(&corev1.Pod{})

// With options
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    Owns(&corev1.Pod{}, builder.WithPredicates(predicate.ResourceVersionChangedPredicate{}))

// Match all owners (not just controller owner)
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    Owns(&corev1.Pod{}, builder.MatchEveryOwner)
```

### How Owns Works

```mermaid
sequenceDiagram
    participant Pod
    participant Handler
    participant Queue
    participant Reconciler
    
    Pod->>Handler: Pod Event (Create/Update/Delete)
    Handler->>Handler: Extract Owner Reference
    Handler->>Queue: Enqueue Owner (Deployment)
    Queue->>Reconciler: Reconcile(Deployment)
    
    Note over Handler,Queue: Only enqueues if owner matches<br/>the For type and is controller owner
```

### Owns Options

```go
// WithPredicates adds predicates to the Owns watch
builder.WithPredicates(predicate.ResourceVersionChangedPredicate{})

// MatchEveryOwner reconciles all owners, not just controller owner
builder.MatchEveryOwner

// OnlyMetadata watches only metadata
builder.OnlyMetadata
```

## Watches Method

The `Watches` method adds custom watch configurations:

```go
// Watch ConfigMaps and enqueue related Deployments
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    Watches(
        &corev1.ConfigMap{},
        handler.EnqueueRequestsFromMapFunc(func(ctx context.Context, obj client.Object) []reconcile.Request {
            // Map ConfigMap to Deployments that reference it
            return []reconcile.Request{
                {NamespacedName: types.NamespacedName{
                    Name:      obj.GetName() + "-deployment",
                    Namespace: obj.GetNamespace(),
                }},
            }
        }),
    )
```

### Watches with Predicates

```go
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    Watches(
        &corev1.ConfigMap{},
        handler.EnqueueRequestsFromMapFunc(mapFunc),
        builder.WithPredicates(predicate.LabelChangedPredicate{}),
    )
```

## WatchesRawSource Method

For advanced use cases, you can watch raw sources:

```go
import "sigs.k8s.io/controller-runtime/pkg/source"

ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    WatchesRawSource(
        source.Kind(mgr.GetCache(), &corev1.Pod{},
            handler.TypedEnqueueRequestForOwner[*corev1.Pod](
                mgr.GetScheme(),
                mgr.GetRESTMapper(),
                &appsv1.Deployment{},
                handler.OnlyControllerOwner(),
            ),
        ),
    )
```

## WithOptions Method

Configure controller-specific options:

```go
import "sigs.k8s.io/controller-runtime/pkg/controller"

ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    WithOptions(controller.Options{
        MaxConcurrentReconciles: 5,
        RecoverPanic: ptr.To(true),
        CacheSyncTimeout: 5 * time.Minute,
        RateLimiter: workqueue.NewItemExponentialFailureRateLimiter(
            100*time.Millisecond,
            1*time.Minute,
        ),
    }).
    Complete(&DeploymentReconciler{})
```

## WithEventFilter Method

Add global predicates that apply to all watches:

```go
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    Owns(&corev1.Pod{}).
    WithEventFilter(predicate.Funcs{
        CreateFunc: func(e event.CreateEvent) bool {
            // Only process creates in specific namespace
            return e.Object.GetNamespace() == "production"
        },
    }).
    Complete(&DeploymentReconciler{})
```

## Named Method

Set a custom controller name:

```go
ctrl.NewControllerManagedBy(mgr).
    Named("deployment-controller").
    For(&appsv1.Deployment{}).
    Complete(&DeploymentReconciler{})
```

**Note**: Controller names must be unique within a manager.

## Complete Method

The `Complete` method builds and registers the controller:

```go
// With reconciler struct
err := ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    Complete(&DeploymentReconciler{
        Client: mgr.GetClient(),
        Scheme: mgr.GetScheme(),
    })

// With reconciler function
err := ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    Complete(reconcile.Func(func(ctx context.Context, req reconcile.Request) (reconcile.Result, error) {
        // Reconciliation logic
        return reconcile.Result{}, nil
    }))
```

## Common Patterns

### 1. Basic Controller

```go
err := ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}).
    Complete(&MyReconciler{
        Client: mgr.GetClient(),
        Scheme: mgr.GetScheme(),
    })
```

### 2. Controller with Owned Resources

```go
err := ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}).
    Owns(&corev1.Pod{}).
    Owns(&corev1.Service{}).
    Complete(&MyReconciler{})
```

### 3. Controller with Custom Watches

```go
err := ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}).
    Watches(
        &corev1.ConfigMap{},
        handler.EnqueueRequestsFromMapFunc(func(ctx context.Context, obj client.Object) []reconcile.Request {
            // Find MyResources that reference this ConfigMap
            var resources myv1.MyResourceList
            if err := mgr.GetClient().List(ctx, &resources); err != nil {
                return nil
            }
            
            var requests []reconcile.Request
            for _, res := range resources.Items {
                if res.Spec.ConfigMapRef == obj.GetName() {
                    requests = append(requests, reconcile.Request{
                        NamespacedName: types.NamespacedName{
                            Name:      res.Name,
                            Namespace: res.Namespace,
                        },
                    })
                }
            }
            return requests
        }),
    ).
    Complete(&MyReconciler{})
```

### 4. Controller with Predicates

```go
err := ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}, builder.WithPredicates(
        predicate.GenerationChangedPredicate{},
    )).
    Owns(&corev1.Pod{}, builder.WithPredicates(
        predicate.ResourceVersionChangedPredicate{},
    )).
    WithEventFilter(predicate.Funcs{
        CreateFunc: func(e event.CreateEvent) bool {
            return e.Object.GetLabels()["managed-by"] == "my-controller"
        },
    }).
    Complete(&MyReconciler{})
```

### 5. High-Performance Controller

```go
err := ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}, builder.OnlyMetadata).
    Owns(&corev1.Pod{}, builder.OnlyMetadata).
    WithOptions(controller.Options{
        MaxConcurrentReconciles: 10,
        UsePriorityQueue: ptr.To(true),
    }).
    Complete(&MyReconciler{})
```

### 6. Namespace-Scoped Controller

```go
// Use predicates to filter by namespace
err := ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}).
    WithEventFilter(predicate.NewPredicateFuncs(func(obj client.Object) bool {
        return obj.GetNamespace() == "my-namespace"
    })).
    Complete(&MyReconciler{})
```

## Webhook Builder

The builder also supports creating webhooks:

```go
import "sigs.k8s.io/controller-runtime/pkg/webhook/admission"

// Validating webhook
err := ctrl.NewWebhookManagedBy(mgr).
    For(&myv1.MyResource{}).
    WithValidator(&MyResourceValidator{}).
    Complete()

// Mutating webhook
err := ctrl.NewWebhookManagedBy(mgr).
    For(&myv1.MyResource{}).
    WithDefaulter(&MyResourceDefaulter{}).
    Complete()

// Both validating and mutating
err := ctrl.NewWebhookManagedBy(mgr).
    For(&myv1.MyResource{}).
    WithDefaulter(&MyResourceDefaulter{}).
    WithValidator(&MyResourceValidator{}).
    Complete()
```

### Webhook Builder Methods

```go
// Set custom webhook path
err := ctrl.NewWebhookManagedBy(mgr).
    For(&myv1.MyResource{}).
    WithDefaulter(&MyResourceDefaulter{}).
    WithPath("/mutate-mygroup-v1-myresource").
    Complete()

// Set log constructor
err := ctrl.NewWebhookManagedBy(mgr).
    For(&myv1.MyResource{}).
    WithValidator(&MyResourceValidator{}).
    WithLogConstructor(func(base logr.Logger, req *admission.Request) logr.Logger {
        return base.WithValues(
            "webhook", "myresource-validator",
            "name", req.Name,
            "namespace", req.Namespace,
        )
    }).
    Complete()
```

## Builder Flow

### Controller Build Flow

```mermaid
sequenceDiagram
    participant User
    participant Builder
    participant Manager
    participant Controller
    participant Sources
    
    User->>Builder: NewControllerManagedBy(mgr)
    User->>Builder: For(&Resource{})
    User->>Builder: Owns(&Child{})
    User->>Builder: Watches(&Related{}, handler)
    User->>Builder: WithOptions(opts)
    User->>Builder: Complete(reconciler)
    
    Builder->>Controller: Create controller
    Builder->>Sources: Configure watch sources
    Builder->>Controller: Add watches
    Builder->>Manager: Register controller
    Manager->>User: Return error or nil
```

## Best Practices

### 1. Use For for Primary Resource

```go
// The resource type you're reconciling
ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{})
```

### 2. Use Owns for Owned Resources

```go
// Resources created and owned by your primary resource
ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}).
    Owns(&corev1.Pod{}).
    Owns(&corev1.Service{})
```

### 3. Use Watches for Related Resources

```go
// Resources that aren't owned but should trigger reconciliation
ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}).
    Watches(&corev1.ConfigMap{}, handler.EnqueueRequestsFromMapFunc(mapFunc))
```

### 4. Add Predicates to Reduce Load

```go
// Filter events to reduce unnecessary reconciliations
ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}, builder.WithPredicates(
        predicate.GenerationChangedPredicate{},
    ))
```

### 5. Use OnlyMetadata for Large Objects

```go
// Reduce memory usage for large resources
ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}, builder.OnlyMetadata)
```

### 6. Name Controllers Descriptively

```go
ctrl.NewControllerManagedBy(mgr).
    Named("myresource-controller").
    For(&myv1.MyResource{})
```

## Common Pitfalls

### 1. Calling For Multiple Times

```go
// BAD - For should only be called once
ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}).
    For(&myv1.AnotherResource{}) // Error!

// GOOD - Create separate controllers
ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}).
    Complete(&MyReconciler{})

ctrl.NewControllerManagedBy(mgr).
    For(&myv1.AnotherResource{}).
    Complete(&AnotherReconciler{})
```

### 2. Using Owns for Non-Owned Resources

```go
// BAD - ConfigMap is not owned by MyResource
ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}).
    Owns(&corev1.ConfigMap{}) // Won't work unless ConfigMap has owner reference

// GOOD - Use Watches instead
ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}).
    Watches(&corev1.ConfigMap{}, handler.EnqueueRequestsFromMapFunc(mapFunc))
```

### 3. Forgetting to Call Complete

```go
// BAD - Controller not registered
builder := ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{})
// Missing Complete()!

// GOOD
err := ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}).
    Complete(&MyReconciler{})
```

## TypedBuilder

For advanced use cases, you can use `TypedBuilder` with custom request types:

```go
type CustomRequest struct {
    NamespacedName types.NamespacedName
    Priority       int
}

builder := ctrl.TypedControllerManagedBy[CustomRequest](mgr).
    For(&myv1.MyResource{}).
    Complete(&MyTypedReconciler{})
```

## Related Packages

- [Controller Package](./02-controller.md) - Controllers built by the builder
- [Manager Package](./01-manager.md) - Manages built controllers
- [Source Package](./07-source.md) - Event sources configured by builder
- [Handler Package](./08-handler.md) - Event handlers used in Watches
- [Predicate Package](./09-predicate.md) - Predicates used in WithPredicates
