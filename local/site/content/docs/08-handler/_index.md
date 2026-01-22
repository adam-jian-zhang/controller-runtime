---
title: "Handler"
weight: 8
---


## Overview

The `pkg/handler` package provides event handlers that transform Kubernetes events into reconcile requests. Handlers determine which objects should be reconciled in response to an event.

## Package Location

```
pkg/handler/
├── eventhandler.go         # Handler interfaces
├── enqueue.go              # EnqueueRequestForObject
├── enqueue_owner.go        # EnqueueRequestForOwner
├── enqueue_mapped.go       # EnqueueRequestsFromMapFunc
├── doc.go                  # Package documentation
└── example_test.go         # Usage examples
```

## Core Concepts

### Handler Flow

<div class="mermaid-diagram">
<svg aria-roledescription="flowchart-v2" role="graphics-document document" viewBox="-8 -8 1173.6328125 49.5" style="max-width: 1173.63px; background-color: transparent;" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" width="100%" id="my-svg"><style>#my-svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}#my-svg .error-icon{fill:#552222;}#my-svg .error-text{fill:#552222;stroke:#552222;}#my-svg .edge-thickness-normal{stroke-width:2px;}#my-svg .edge-thickness-thick{stroke-width:3.5px;}#my-svg .edge-pattern-solid{stroke-dasharray:0;}#my-svg .edge-pattern-dashed{stroke-dasharray:3;}#my-svg .edge-pattern-dotted{stroke-dasharray:2;}#my-svg .marker{fill:#333333;stroke:#333333;}#my-svg .marker.cross{stroke:#333333;}#my-svg svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#my-svg .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#333;}#my-svg .cluster-label text{fill:#333;}#my-svg .cluster-label span,#my-svg p{color:#333;}#my-svg .label text,#my-svg span,#my-svg p{fill:#333;color:#333;}#my-svg .node rect,#my-svg .node circle,#my-svg .node ellipse,#my-svg .node polygon,#my-svg .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#my-svg .flowchart-label text{text-anchor:middle;}#my-svg .node .label{text-align:center;}#my-svg .node.clickable{cursor:pointer;}#my-svg .arrowheadPath{fill:#333333;}#my-svg .edgePath .path{stroke:#333333;stroke-width:2.0px;}#my-svg .flowchart-link{stroke:#333333;fill:none;}#my-svg .edgeLabel{background-color:#e8e8e8;text-align:center;}#my-svg .edgeLabel rect{opacity:0.5;background-color:#e8e8e8;fill:#e8e8e8;}#my-svg .labelBkg{background-color:rgba(232, 232, 232, 0.5);}#my-svg .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#my-svg .cluster text{fill:#333;}#my-svg .cluster span,#my-svg p{color:#333;}#my-svg div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(80, 100%, 96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#my-svg .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#333;}#my-svg :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}</style><g><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="6" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointEnd"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 0 L 10 5 L 0 10 z"/></marker><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="4.5" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointStart"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 5 L 10 10 L 10 0 z"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="11" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleEnd"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="-1" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleStart"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="12" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossEnd"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="-1" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossStart"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><g class="root"><g class="clusters"/><g class="edgePaths"><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Event LE-Handler" id="L-Event-Handler-0" d="M140.3671875,16.75L158.15950520833334,16.75C175.95182291666666,16.75,211.53645833333334,16.75,246.23776041666667,16.75C280.93906250000003,16.75,314.75703125,16.75,331.666015625,16.75L348.575,16.75"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Handler LE-Requests" id="L-Handler-Requests-0" d="M470.109375,16.75L480.2239583333333,16.75C490.3385416666667,16.75,510.5677083333333,16.75,529.9135416666667,16.75C549.259375,16.75,567.7218750000001,16.75,576.953125,16.75L586.184375,16.75"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Requests LE-Queue" id="L-Requests-Queue-0" d="M742.9453125,16.75L752.208984375,16.75C761.47265625,16.75,780,16.75,797.6440104166667,16.75C815.2880208333332,16.75,832.0486979166667,16.75,840.4290364583334,16.75L848.809375,16.75"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Queue LE-Reconciler" id="L-Queue-Reconciler-0" d="M955.453125,16.75L964.8190104166666,16.75C974.1848958333334,16.75,992.9166666666666,16.75,1010.7651041666667,16.75C1028.6135416666666,16.75,1045.5786458333334,16.75,1054.0611979166667,16.75L1062.54375,16.75"/></g><g class="edgeLabels"><g transform="translate(247.12109375, 16.75)" class="edgeLabel"><g transform="translate(-81.75390625, -9.25)" class="label"><foreignObject height="18.5" width="163.5078125"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Create/Update/Delete</span></div></foreignObject></g></g><g transform="translate(530.796875, 16.75)" class="edgeLabel"><g transform="translate(-35.6875, -9.25)" class="label"><foreignObject height="18.5" width="71.375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Transform</span></div></foreignObject></g></g><g transform="translate(798.52734375, 16.75)" class="edgeLabel"><g transform="translate(-30.58203125, -9.25)" class="label"><foreignObject height="18.5" width="61.1640625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Enqueue</span></div></foreignObject></g></g><g transform="translate(1011.6484375, 16.75)" class="edgeLabel"><g transform="translate(-31.1953125, -9.25)" class="label"><foreignObject height="18.5" width="62.390625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Dequeue</span></div></foreignObject></g></g></g><g class="nodes"><g transform="translate(70.18359375, 16.75)" id="flowchart-Event-0" class="node default default flowchart-label"><rect height="33.5" width="140.3671875" y="-16.75" x="-70.18359375" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-62.68359375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="125.3671875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Kubernetes Event</span></div></foreignObject></g></g><g transform="translate(411.9921875, 16.75)" id="flowchart-Handler-1" class="node default default flowchart-label"><rect height="33.5" width="116.234375" y="-16.75" x="-58.1171875" ry="0" rx="0" style="fill:#e1f5ff;" class="basic label-container"/><g transform="translate(-50.6171875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="101.234375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Event Handler</span></div></foreignObject></g></g><g transform="translate(667.21484375, 16.75)" id="flowchart-Requests-3" class="node default default flowchart-label"><rect height="33.5" width="151.4609375" y="-16.75" x="-75.73046875" ry="0" rx="0" style="fill:#fff4e1;" class="basic label-container"/><g transform="translate(-68.23046875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="136.4609375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Reconcile Requests</span></div></foreignObject></g></g><g transform="translate(904.78125, 16.75)" id="flowchart-Queue-5" class="node default default flowchart-label"><rect height="33.5" width="101.34375" y="-16.75" x="-50.671875" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-43.171875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="86.34375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Work Queue</span></div></foreignObject></g></g><g transform="translate(1112.73828125, 16.75)" id="flowchart-Reconciler-7" class="node default default flowchart-label"><rect height="33.5" width="89.7890625" y="-16.75" x="-44.89453125" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-37.39453125, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="74.7890625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Reconciler</span></div></foreignObject></g></g></g></g></g></svg>
</div>

## EventHandler Interface

```go
type EventHandler = TypedEventHandler[client.Object, reconcile.Request]

type TypedEventHandler[object any, request comparable] interface {
    // Create is called in response to a create event
    Create(context.Context, event.TypedCreateEvent[object], workqueue.TypedRateLimitingInterface[request])
    
    // Update is called in response to an update event
    Update(context.Context, event.TypedUpdateEvent[object], workqueue.TypedRateLimitingInterface[request])
    
    // Delete is called in response to a delete event
    Delete(context.Context, event.TypedDeleteEvent[object], workqueue.TypedRateLimitingInterface[request])
    
    // Generic is called for synthetic events
    Generic(context.Context, event.TypedGenericEvent[object], workqueue.TypedRateLimitingInterface[request])
}
```

## Built-in Handlers

### 1. EnqueueRequestForObject

Enqueues the object that triggered the event:

```go
import "sigs.k8s.io/controller-runtime/pkg/handler"

// Enqueue the Pod itself
handler := &handler.EnqueueRequestForObject{}

// Use with builder
ctrl.NewControllerManagedBy(mgr).
    For(&corev1.Pod{}) // Automatically uses EnqueueRequestForObject
```

**Use case**: Reconcile the object that changed.

**Example**:
- Pod created → Reconcile that Pod
- Deployment updated → Reconcile that Deployment

### 2. EnqueueRequestForOwner

Enqueues the owner of the object:

```go
// Enqueue the Deployment that owns the Pod
handler := handler.EnqueueRequestForOwner(
    mgr.GetScheme(),
    mgr.GetRESTMapper(),
    &appsv1.Deployment{}, // Owner type
    handler.OnlyControllerOwner(), // Only controller owner
)

// Use with builder
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    Owns(&corev1.Pod{}) // Automatically uses EnqueueRequestForOwner
```

**Use case**: Reconcile the owner when owned resource changes.

**Example**:
- Pod created → Reconcile owning Deployment
- ReplicaSet updated → Reconcile owning Deployment

### 3. EnqueueRequestsFromMapFunc

Custom mapping from event to reconcile requests:

```go
// Map ConfigMap to Deployments that reference it
handler := handler.EnqueueRequestsFromMapFunc(
    func(ctx context.Context, obj client.Object) []reconcile.Request {
        // Find Deployments that reference this ConfigMap
        var deployments appsv1.DeploymentList
        if err := mgr.GetClient().List(ctx, &deployments); err != nil {
            return nil
        }
        
        var requests []reconcile.Request
        for _, deploy := range deployments.Items {
            // Check if deployment references this ConfigMap
            for _, vol := range deploy.Spec.Template.Spec.Volumes {
                if vol.ConfigMap != nil && vol.ConfigMap.Name == obj.GetName() {
                    requests = append(requests, reconcile.Request{
                        NamespacedName: types.NamespacedName{
                            Name:      deploy.Name,
                            Namespace: deploy.Namespace,
                        },
                    })
                }
            }
        }
        return requests
    },
)

// Use with builder
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    Watches(&corev1.ConfigMap{}, handler)
```

**Use case**: Custom mapping logic between resources.

**Example**:
- ConfigMap updated → Reconcile all Deployments using it
- Node updated → Reconcile all Pods on that Node
- Secret changed → Reconcile all resources referencing it

## Handler Usage Patterns

### Pattern 1: Watch Primary Resource

```go
// Automatically uses EnqueueRequestForObject
ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{})
```

Equivalent to:

```go
ctrl.NewControllerManagedBy(mgr).
    WatchesRawSource(
        source.Kind(mgr.GetCache(), &myv1.MyResource{},
            &handler.EnqueueRequestForObject{}),
    )
```

### Pattern 2: Watch Owned Resources

```go
// Automatically uses EnqueueRequestForOwner
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    Owns(&corev1.Pod{})
```

Equivalent to:

```go
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    WatchesRawSource(
        source.Kind(mgr.GetCache(), &corev1.Pod{},
            handler.EnqueueRequestForOwner(
                mgr.GetScheme(),
                mgr.GetRESTMapper(),
                &appsv1.Deployment{},
                handler.OnlyControllerOwner(),
            )),
    )
```

### Pattern 3: Custom Mapping

```go
ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}).
    Watches(
        &corev1.ConfigMap{},
        handler.EnqueueRequestsFromMapFunc(mapFunc),
    )
```

## EnqueueRequestForOwner Details

### Controller Owner Only

```go
// Only enqueue if owner reference has controller=true
handler.EnqueueRequestForOwner(
    scheme,
    mapper,
    &appsv1.Deployment{},
    handler.OnlyControllerOwner(), // Default behavior
)
```

### All Owners

```go
// Enqueue for all owner references
handler.EnqueueRequestForOwner(
    scheme,
    mapper,
    &appsv1.Deployment{},
    // No OnlyControllerOwner option
)

// Or with builder
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    Owns(&corev1.Pod{}, builder.MatchEveryOwner)
```

### Typed Owner Handler

```go
// Type-safe owner handler
handler := handler.TypedEnqueueRequestForOwner[*corev1.Pod](
    mgr.GetScheme(),
    mgr.GetRESTMapper(),
    &appsv1.Deployment{},
    handler.OnlyControllerOwner(),
)
```

## EnqueueRequestsFromMapFunc Details

### Basic Mapping

```go
mapFunc := func(ctx context.Context, obj client.Object) []reconcile.Request {
    return []reconcile.Request{
        {
            NamespacedName: types.NamespacedName{
                Name:      obj.GetName(),
                Namespace: obj.GetNamespace(),
            },
        },
    }
}

handler := handler.EnqueueRequestsFromMapFunc(mapFunc)
```

### Mapping with Client Lookup

```go
mapFunc := func(ctx context.Context, obj client.Object) []reconcile.Request {
    // Get client from context
    c := client.FromContext(ctx)
    
    // List resources that reference this object
    var resources myv1.MyResourceList
    if err := c.List(ctx, &resources); err != nil {
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
}
```

### Mapping with Field Index

```go
// Add index first
mgr.GetFieldIndexer().IndexField(ctx, &myv1.MyResource{}, "spec.configMapRef",
    func(obj client.Object) []string {
        res := obj.(*myv1.MyResource)
        return []string{res.Spec.ConfigMapRef}
    })

// Use index in map function
mapFunc := func(ctx context.Context, obj client.Object) []reconcile.Request {
    c := client.FromContext(ctx)
    
    var resources myv1.MyResourceList
    if err := c.List(ctx, &resources,
        client.MatchingFields{"spec.configMapRef": obj.GetName()}); err != nil {
        return nil
    }
    
    var requests []reconcile.Request
    for _, res := range resources.Items {
        requests = append(requests, reconcile.Request{
            NamespacedName: types.NamespacedName{
                Name:      res.Name,
                Namespace: res.Namespace,
            },
        })
    }
    return requests
}
```

## Custom Handlers

### Implementing EventHandler

```go
type MyHandler struct {
    client client.Client
}

func (h *MyHandler) Create(ctx context.Context, evt event.CreateEvent, q workqueue.RateLimitingInterface) {
    // Custom create logic
    q.Add(reconcile.Request{
        NamespacedName: types.NamespacedName{
            Name:      evt.Object.GetName(),
            Namespace: evt.Object.GetNamespace(),
        },
    })
}

func (h *MyHandler) Update(ctx context.Context, evt event.UpdateEvent, q workqueue.RateLimitingInterface) {
    // Custom update logic
    q.Add(reconcile.Request{
        NamespacedName: types.NamespacedName{
            Name:      evt.ObjectNew.GetName(),
            Namespace: evt.ObjectNew.GetNamespace(),
        },
    })
}

func (h *MyHandler) Delete(ctx context.Context, evt event.DeleteEvent, q workqueue.RateLimitingInterface) {
    // Custom delete logic
}

func (h *MyHandler) Generic(ctx context.Context, evt event.GenericEvent, q workqueue.RateLimitingInterface) {
    // Custom generic logic
}

// Use custom handler
handler := &MyHandler{client: mgr.GetClient()}
```

### Using Funcs

```go
handler := handler.Funcs{
    CreateFunc: func(ctx context.Context, evt event.CreateEvent, q workqueue.RateLimitingInterface) {
        // Handle create
        q.Add(reconcile.Request{
            NamespacedName: types.NamespacedName{
                Name:      evt.Object.GetName(),
                Namespace: evt.Object.GetNamespace(),
            },
        })
    },
    UpdateFunc: func(ctx context.Context, evt event.UpdateEvent, q workqueue.RateLimitingInterface) {
        // Handle update
    },
    DeleteFunc: func(ctx context.Context, evt event.DeleteEvent, q workqueue.RateLimitingInterface) {
        // Handle delete
    },
    GenericFunc: func(ctx context.Context, evt event.GenericEvent, q workqueue.RateLimitingInterface) {
        // Handle generic
    },
}
```

## Common Patterns

### 1. One-to-One Mapping

```go
// Object triggers reconciliation of itself
&handler.EnqueueRequestForObject{}
```

### 2. Child-to-Parent Mapping

```go
// Child triggers reconciliation of parent
handler.EnqueueRequestForOwner(scheme, mapper, &Parent{})
```

### 3. One-to-Many Mapping

```go
// One object triggers reconciliation of many
handler.EnqueueRequestsFromMapFunc(func(ctx context.Context, obj client.Object) []reconcile.Request {
    // Return multiple requests
    return []reconcile.Request{req1, req2, req3}
})
```

### 4. Cross-Namespace Mapping

```go
// Map object in one namespace to objects in other namespaces
handler.EnqueueRequestsFromMapFunc(func(ctx context.Context, obj client.Object) []reconcile.Request {
    var resources myv1.MyResourceList
    c.List(ctx, &resources) // List across all namespaces
    
    var requests []reconcile.Request
    for _, res := range resources.Items {
        if res.Spec.Reference == obj.GetName() {
            requests = append(requests, reconcile.Request{
                NamespacedName: types.NamespacedName{
                    Name:      res.Name,
                    Namespace: res.Namespace,
                },
            })
        }
    }
    return requests
})
```

### 5. Conditional Mapping

```go
// Only map if certain conditions are met
handler.EnqueueRequestsFromMapFunc(func(ctx context.Context, obj client.Object) []reconcile.Request {
    // Check condition
    if obj.GetLabels()["trigger"] != "true" {
        return nil
    }
    
    return []reconcile.Request{
        {NamespacedName: types.NamespacedName{
            Name:      obj.GetName(),
            Namespace: obj.GetNamespace(),
        }},
    }
})
```

## Best Practices

### 1. Use Built-in Handlers When Possible

```go
// Preferred
ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}).
    Owns(&corev1.Pod{})

// Instead of custom handler
```

### 2. Use Field Indexes for Efficient Lookups

```go
// Add index
mgr.GetFieldIndexer().IndexField(ctx, &myv1.MyResource{}, "spec.ref", indexFunc)

// Use in map function
mapFunc := func(ctx context.Context, obj client.Object) []reconcile.Request {
    var resources myv1.MyResourceList
    c.List(ctx, &resources, client.MatchingFields{"spec.ref": obj.GetName()})
    // ...
}
```

### 3. Handle Errors Gracefully

```go
mapFunc := func(ctx context.Context, obj client.Object) []reconcile.Request {
    var resources myv1.MyResourceList
    if err := c.List(ctx, &resources); err != nil {
        // Log error but don't fail
        log.Error(err, "failed to list resources")
        return nil
    }
    // ...
}
```

### 4. Avoid Expensive Operations

```go
// BAD - expensive API calls
mapFunc := func(ctx context.Context, obj client.Object) []reconcile.Request {
    // Multiple API calls
    for _, ns := range namespaces {
        c.List(ctx, &list, client.InNamespace(ns))
    }
}

// GOOD - single API call with index
mapFunc := func(ctx context.Context, obj client.Object) []reconcile.Request {
    c.List(ctx, &list, client.MatchingFields{"field": value})
}
```

### 5. Return Empty Slice, Not Nil

```go
// Preferred
return []reconcile.Request{}

// Also acceptable
return nil
```

## Common Pitfalls

### 1. Not Handling Empty Owner References

```go
// BAD - assumes owner reference exists
handler.EnqueueRequestForOwner(scheme, mapper, &Parent{})
// Fails if child has no owner reference

// GOOD - handled automatically by EnqueueRequestForOwner
// Returns empty if no owner reference
```

### 2. Expensive Map Functions

```go
// BAD - lists all resources every time
mapFunc := func(ctx context.Context, obj client.Object) []reconcile.Request {
    var resources myv1.MyResourceList
    c.List(ctx, &resources) // Expensive!
    // Filter in memory
}

// GOOD - use field index
mapFunc := func(ctx context.Context, obj client.Object) []reconcile.Request {
    var resources myv1.MyResourceList
    c.List(ctx, &resources, client.MatchingFields{"ref": obj.GetName()})
}
```

### 3. Forgetting Context

```go
// BAD - not using context
mapFunc := func(ctx context.Context, obj client.Object) []reconcile.Request {
    c.List(context.Background(), &resources) // Wrong!
}

// GOOD - use provided context
mapFunc := func(ctx context.Context, obj client.Object) []reconcile.Request {
    c.List(ctx, &resources)
}
```

## Related Packages

- [Source Package](/docs/07-source/) - Provides events to handlers
- [Predicate Package](/docs/09-predicate/) - Filters events before handlers
- [Controller Package](/docs/02-controller/) - Uses handlers
- [Builder Package](/docs/04-builder/) - Configures handlers
