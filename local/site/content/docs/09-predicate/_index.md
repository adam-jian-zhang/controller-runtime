---
title: "Predicate"
weight: 9
---


## Overview

The `pkg/predicate` package provides filters (predicates) that determine which events should be processed by controllers. Predicates help reduce unnecessary reconciliations by filtering events before they reach the handler.

## Package Location

```
pkg/predicate/
├── predicate.go        # Predicate interfaces and implementations
└── doc.go              # Package documentation
```

## Core Concepts

### Predicate Flow

<div class="mermaid-diagram">
<svg aria-roledescription="flowchart-v2" role="graphics-document document" viewBox="-8 -8 744.4921875 133" style="max-width: 744.492px; background-color: transparent;" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" width="100%" id="my-svg"><style>#my-svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}#my-svg .error-icon{fill:#552222;}#my-svg .error-text{fill:#552222;stroke:#552222;}#my-svg .edge-thickness-normal{stroke-width:2px;}#my-svg .edge-thickness-thick{stroke-width:3.5px;}#my-svg .edge-pattern-solid{stroke-dasharray:0;}#my-svg .edge-pattern-dashed{stroke-dasharray:3;}#my-svg .edge-pattern-dotted{stroke-dasharray:2;}#my-svg .marker{fill:#333333;stroke:#333333;}#my-svg .marker.cross{stroke:#333333;}#my-svg svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#my-svg .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#333;}#my-svg .cluster-label text{fill:#333;}#my-svg .cluster-label span,#my-svg p{color:#333;}#my-svg .label text,#my-svg span,#my-svg p{fill:#333;color:#333;}#my-svg .node rect,#my-svg .node circle,#my-svg .node ellipse,#my-svg .node polygon,#my-svg .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#my-svg .flowchart-label text{text-anchor:middle;}#my-svg .node .label{text-align:center;}#my-svg .node.clickable{cursor:pointer;}#my-svg .arrowheadPath{fill:#333333;}#my-svg .edgePath .path{stroke:#333333;stroke-width:2.0px;}#my-svg .flowchart-link{stroke:#333333;fill:none;}#my-svg .edgeLabel{background-color:#e8e8e8;text-align:center;}#my-svg .edgeLabel rect{opacity:0.5;background-color:#e8e8e8;fill:#e8e8e8;}#my-svg .labelBkg{background-color:rgba(232, 232, 232, 0.5);}#my-svg .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#my-svg .cluster text{fill:#333;}#my-svg .cluster span,#my-svg p{color:#333;}#my-svg div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(80, 100%, 96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#my-svg .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#333;}#my-svg :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}</style><g><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="6" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointEnd"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 0 L 10 5 L 0 10 z"/></marker><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="4.5" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointStart"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 5 L 10 10 L 10 0 z"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="11" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleEnd"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="-1" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleStart"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="12" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossEnd"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="-1" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossStart"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><g class="root"><g class="clusters"/><g class="edgePaths"><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Event LE-Predicate" id="L-Event-Predicate-0" d="M140.3671875,58.5L147.78125,58.5C155.1953125,58.5,170.0234375,58.5,183.96822916666667,58.5C197.91302083333335,58.5,210.97447916666667,58.5,217.50520833333334,58.5L224.0359375,58.5"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Predicate LE-Handler" id="L-Predicate-Handler-0" d="M304.23643338323353,41.75L312.54598615269464,37.583333333333336C320.8555389221557,33.416666666666664,337.47464446107784,25.083333333333332,352.1860201472056,20.916666666666668C366.89739583333335,16.75,379.7010416666667,16.75,386.1028645833333,16.75L392.5046875,16.75"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Predicate LE-Dropped" id="L-Predicate-Dropped-0" d="M304.23643338323353,75.25L312.54598615269464,79.41666666666667C320.8555389221557,83.58333333333333,337.47464446107784,91.91666666666667,351.8618013972056,96.08333333333333C366.24895833333335,100.25,378.4041666666667,100.25,384.4817708333333,100.25L390.559375,100.25"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Handler LE-Queue" id="L-Handler-Queue-0" d="M514.0390625,16.75L523.626953125,16.75C533.21484375,16.75,552.390625,16.75,570.3588541666667,16.75C588.3270833333333,16.75,605.0877604166667,16.75,613.4680989583334,16.75L621.8484375,16.75"/></g><g class="edgeLabels"><g transform="translate(184.8515625, 58.5)" class="edgeLabel"><g transform="translate(-19.484375, -9.25)" class="label"><foreignObject height="18.5" width="38.96875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Filter</span></div></foreignObject></g></g><g transform="translate(354.09375, 16.75)" class="edgeLabel"><g transform="translate(-14.765625, -9.25)" class="label"><foreignObject height="18.5" width="29.53125"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Pass</span></div></foreignObject></g></g><g transform="translate(354.09375, 100.25)" class="edgeLabel"><g transform="translate(-16.765625, -9.25)" class="label"><foreignObject height="18.5" width="33.53125"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Drop</span></div></foreignObject></g></g><g transform="translate(571.56640625, 16.75)" class="edgeLabel"><g transform="translate(-30.58203125, -9.25)" class="label"><foreignObject height="18.5" width="61.1640625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Enqueue</span></div></foreignObject></g></g></g><g class="nodes"><g transform="translate(70.18359375, 58.5)" id="flowchart-Event-0" class="node default default flowchart-label"><rect height="33.5" width="140.3671875" y="-16.75" x="-70.18359375" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-62.68359375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="125.3671875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Kubernetes Event</span></div></foreignObject></g></g><g transform="translate(270.83203125, 58.5)" id="flowchart-Predicate-1" class="node default default flowchart-label"><rect height="33.5" width="82.9921875" y="-16.75" x="-41.49609375" ry="0" rx="0" style="fill:#e1f5ff;" class="basic label-container"/><g transform="translate(-33.99609375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="67.9921875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Predicate</span></div></foreignObject></g></g><g transform="translate(455.921875, 16.75)" id="flowchart-Handler-3" class="node default default flowchart-label"><rect height="33.5" width="116.234375" y="-16.75" x="-58.1171875" ry="0" rx="0" style="fill:#fff4e1;" class="basic label-container"/><g transform="translate(-50.6171875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="101.234375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Event Handler</span></div></foreignObject></g></g><g transform="translate(455.921875, 100.25)" id="flowchart-Dropped-5" class="node default default flowchart-label"><rect height="33.5" width="120.125" y="-16.75" x="-60.0625" ry="0" rx="0" style="fill:#ffebee;" class="basic label-container"/><g transform="translate(-52.5625, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="105.125"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Event Dropped</span></div></foreignObject></g></g><g transform="translate(677.8203125, 16.75)" id="flowchart-Queue-7" class="node default default flowchart-label"><rect height="33.5" width="101.34375" y="-16.75" x="-50.671875" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-43.171875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="86.34375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Work Queue</span></div></foreignObject></g></g></g></g></g></svg>
</div>

## Predicate Interface

```go
type Predicate = TypedPredicate[client.Object]

type TypedPredicate[object any] interface {
    // Create returns true if the Create event should be processed
    Create(event.TypedCreateEvent[object]) bool
    
    // Delete returns true if the Delete event should be processed
    Delete(event.TypedDeleteEvent[object]) bool
    
    // Update returns true if the Update event should be processed
    Update(event.TypedUpdateEvent[object]) bool
    
    // Generic returns true if the Generic event should be processed
    Generic(event.TypedGenericEvent[object]) bool
}
```

## Built-in Predicates

### 1. GenerationChangedPredicate

Filters events where only the generation changed (spec changes):

```go
import "sigs.k8s.io/controller-runtime/pkg/predicate"

// Only process when spec changes
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}, builder.WithPredicates(
        predicate.GenerationChangedPredicate{},
    ))
```

**Use case**: Ignore status-only updates.

**Example**: Deployment status updated → Event dropped

### 2. ResourceVersionChangedPredicate

Filters events where resource version didn't change:

```go
// Process all changes including status
ctrl.NewControllerManagedBy(mgr).
    For(&corev1.Pod{}, builder.WithPredicates(
        predicate.ResourceVersionChangedPredicate{},
    ))
```

**Use case**: Process all updates including status changes.

### 3. AnnotationChangedPredicate

Filters events where annotations didn't change:

```go
// Only process when annotations change
ctrl.NewControllerManagedBy(mgr).
    For(&corev1.Pod{}, builder.WithPredicates(
        predicate.AnnotationChangedPredicate{},
    ))
```

**Use case**: React to annotation changes only.

### 4. LabelChangedPredicate

Filters events where labels didn't change:

```go
// Only process when labels change
ctrl.NewControllerManagedBy(mgr).
    For(&corev1.Pod{}, builder.WithPredicates(
        predicate.LabelChangedPredicate{},
    ))
```

**Use case**: React to label changes only.

### 5. NewPredicateFuncs

Creates a predicate from a simple function:

```go
// Filter by namespace
predicate.NewPredicateFuncs(func(obj client.Object) bool {
    return obj.GetNamespace() == "production"
})
```

**Use case**: Simple filtering based on object properties.

## Using Predicates

### With For Method

```go
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}, builder.WithPredicates(
        predicate.GenerationChangedPredicate{},
    ))
```

### With Owns Method

```go
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    Owns(&corev1.Pod{}, builder.WithPredicates(
        predicate.ResourceVersionChangedPredicate{},
    ))
```

### With Watches Method

```go
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    Watches(
        &corev1.ConfigMap{},
        handler.EnqueueRequestsFromMapFunc(mapFunc),
        builder.WithPredicates(predicate.LabelChangedPredicate{}),
    )
```

### Global Predicates

Apply to all watches:

```go
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}).
    Owns(&corev1.Pod{}).
    WithEventFilter(predicate.GenerationChangedPredicate{})
```

### Multiple Predicates

Combine multiple predicates (AND logic):

```go
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}, builder.WithPredicates(
        predicate.GenerationChangedPredicate{},
        predicate.NewPredicateFuncs(func(obj client.Object) bool {
            return obj.GetNamespace() == "production"
        }),
    ))
```

## Custom Predicates

### Using Funcs

```go
import "sigs.k8s.io/controller-runtime/pkg/predicate"

pred := predicate.Funcs{
    CreateFunc: func(e event.CreateEvent) bool {
        // Only process creates in production namespace
        return e.Object.GetNamespace() == "production"
    },
    UpdateFunc: func(e event.UpdateEvent) bool {
        // Only process if generation changed
        return e.ObjectNew.GetGeneration() != e.ObjectOld.GetGeneration()
    },
    DeleteFunc: func(e event.DeleteEvent) bool {
        // Process all deletes
        return true
    },
    GenericFunc: func(e event.GenericEvent) bool {
        // Process all generic events
        return true
    },
}

ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}, builder.WithPredicates(pred))
```

### Implementing Predicate Interface

```go
type MyPredicate struct{}

func (p MyPredicate) Create(e event.CreateEvent) bool {
    return e.Object.GetLabels()["managed-by"] == "my-controller"
}

func (p MyPredicate) Update(e event.UpdateEvent) bool {
    oldLabels := e.ObjectOld.GetLabels()
    newLabels := e.ObjectNew.GetLabels()
    return oldLabels["version"] != newLabels["version"]
}

func (p MyPredicate) Delete(e event.DeleteEvent) bool {
    return true
}

func (p MyPredicate) Generic(e event.GenericEvent) bool {
    return true
}

// Use custom predicate
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}, builder.WithPredicates(MyPredicate{}))
```

## Predicate Combinators

### And

Combine predicates with AND logic:

```go
pred := predicate.And(
    predicate.GenerationChangedPredicate{},
    predicate.NewPredicateFuncs(func(obj client.Object) bool {
        return obj.GetNamespace() == "production"
    }),
)
```

### Or

Combine predicates with OR logic:

```go
pred := predicate.Or(
    predicate.LabelChangedPredicate{},
    predicate.AnnotationChangedPredicate{},
)
```

### Not

Negate a predicate:

```go
pred := predicate.Not(
    predicate.NewPredicateFuncs(func(obj client.Object) bool {
        return obj.GetNamespace() == "kube-system"
    }),
)
```

## Common Predicate Patterns

### 1. Filter by Namespace

```go
predicate.NewPredicateFuncs(func(obj client.Object) bool {
    return obj.GetNamespace() == "production"
})
```

### 2. Filter by Label

```go
predicate.NewPredicateFuncs(func(obj client.Object) bool {
    labels := obj.GetLabels()
    return labels["managed-by"] == "my-controller"
})
```

### 3. Filter by Annotation

```go
predicate.NewPredicateFuncs(func(obj client.Object) bool {
    annotations := obj.GetAnnotations()
    return annotations["reconcile"] == "true"
})
```

### 4. Ignore Status-Only Updates

```go
predicate.GenerationChangedPredicate{}
```

### 5. Process Only Spec Changes

```go
predicate.Funcs{
    UpdateFunc: func(e event.UpdateEvent) bool {
        oldObj := e.ObjectOld.(*appsv1.Deployment)
        newObj := e.ObjectNew.(*appsv1.Deployment)
        return !reflect.DeepEqual(oldObj.Spec, newObj.Spec)
    },
}
```

### 6. Filter by Owner

```go
predicate.NewPredicateFuncs(func(obj client.Object) bool {
    for _, owner := range obj.GetOwnerReferences() {
        if owner.Kind == "MyResource" {
            return true
        }
    }
    return false
})
```

### 7. Filter by Deletion

```go
predicate.Funcs{
    CreateFunc: func(e event.CreateEvent) bool {
        return e.Object.GetDeletionTimestamp().IsZero()
    },
    UpdateFunc: func(e event.UpdateEvent) bool {
        // Only process if being deleted
        return !e.ObjectNew.GetDeletionTimestamp().IsZero()
    },
}
```

### 8. Filter by Field Value

```go
predicate.NewPredicateFuncs(func(obj client.Object) bool {
    pod := obj.(*corev1.Pod)
    return pod.Spec.NodeName == "node-1"
})
```

### 9. Ignore System Namespaces

```go
predicate.NewPredicateFuncs(func(obj client.Object) bool {
    systemNamespaces := []string{"kube-system", "kube-public", "kube-node-lease"}
    for _, ns := range systemNamespaces {
        if obj.GetNamespace() == ns {
            return false
        }
    }
    return true
})
```

### 10. Paused Annotation

```go
predicate.NewPredicateFuncs(func(obj client.Object) bool {
    annotations := obj.GetAnnotations()
    return annotations["reconcile.paused"] != "true"
})
```

## Advanced Patterns

### Stateful Predicate

```go
type StatefulPredicate struct {
    lastSeen map[string]time.Time
    mu       sync.RWMutex
}

func (p *StatefulPredicate) Update(e event.UpdateEvent) bool {
    p.mu.Lock()
    defer p.mu.Unlock()
    
    key := e.ObjectNew.GetNamespace() + "/" + e.ObjectNew.GetName()
    lastSeen, exists := p.lastSeen[key]
    
    if !exists || time.Since(lastSeen) > 5*time.Minute {
        p.lastSeen[key] = time.Now()
        return true
    }
    
    return false
}

// Implement other methods...
```

### Type-Specific Predicate

```go
func PodReadyPredicate() predicate.Predicate {
    return predicate.Funcs{
        CreateFunc: func(e event.CreateEvent) bool {
            pod := e.Object.(*corev1.Pod)
            return isPodReady(pod)
        },
        UpdateFunc: func(e event.UpdateEvent) bool {
            oldPod := e.ObjectOld.(*corev1.Pod)
            newPod := e.ObjectNew.(*corev1.Pod)
            return isPodReady(oldPod) != isPodReady(newPod)
        },
    }
}

func isPodReady(pod *corev1.Pod) bool {
    for _, cond := range pod.Status.Conditions {
        if cond.Type == corev1.PodReady {
            return cond.Status == corev1.ConditionTrue
        }
    }
    return false
}
```

## Best Practices

### 1. Use GenerationChangedPredicate for Spec Changes

```go
// Ignore status-only updates
predicate.GenerationChangedPredicate{}
```

### 2. Combine Predicates for Complex Logic

```go
predicate.And(
    predicate.GenerationChangedPredicate{},
    predicate.NewPredicateFuncs(func(obj client.Object) bool {
        return obj.GetNamespace() != "kube-system"
    }),
)
```

### 3. Use NewPredicateFuncs for Simple Filters

```go
// Simple namespace filter
predicate.NewPredicateFuncs(func(obj client.Object) bool {
    return obj.GetNamespace() == "production"
})
```

### 4. Handle All Event Types

```go
predicate.Funcs{
    CreateFunc:  func(e event.CreateEvent) bool { return true },
    UpdateFunc:  func(e event.UpdateEvent) bool { return true },
    DeleteFunc:  func(e event.DeleteEvent) bool { return true },
    GenericFunc: func(e event.GenericEvent) bool { return true },
}
```

### 5. Type Assert Safely

```go
predicate.Funcs{
    UpdateFunc: func(e event.UpdateEvent) bool {
        pod, ok := e.ObjectNew.(*corev1.Pod)
        if !ok {
            return false
        }
        // Use pod
        return true
    },
}
```

## Common Pitfalls

### 1. Forgetting Event Types

```go
// BAD - only handles updates
predicate.Funcs{
    UpdateFunc: func(e event.UpdateEvent) bool {
        return true
    },
    // Missing Create, Delete, Generic
}

// GOOD - handle all types
predicate.Funcs{
    CreateFunc:  func(e event.CreateEvent) bool { return true },
    UpdateFunc:  func(e event.UpdateEvent) bool { return true },
    DeleteFunc:  func(e event.DeleteEvent) bool { return true },
    GenericFunc: func(e event.GenericEvent) bool { return true },
}
```

### 2. Type Assertion Without Check

```go
// BAD - panics if wrong type
pod := e.ObjectNew.(*corev1.Pod)

// GOOD - safe type assertion
pod, ok := e.ObjectNew.(*corev1.Pod)
if !ok {
    return false
}
```

### 3. Expensive Predicate Logic

```go
// BAD - API calls in predicate
predicate.Funcs{
    UpdateFunc: func(e event.UpdateEvent) bool {
        var list corev1.PodList
        c.List(ctx, &list) // Expensive!
        return true
    },
}

// GOOD - simple checks only
predicate.Funcs{
    UpdateFunc: func(e event.UpdateEvent) bool {
        return e.ObjectNew.GetGeneration() != e.ObjectOld.GetGeneration()
    },
}
```

## Performance Considerations

### Predicate Efficiency

Predicates are called for every event, so they should be:
- **Fast**: Avoid expensive operations
- **Stateless**: Don't rely on external state
- **Simple**: Keep logic straightforward

### Reducing Reconciliations

Use predicates to reduce unnecessary reconciliations:

```go
// Without predicate: reconcile on every update
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{})

// With predicate: reconcile only on spec changes
ctrl.NewControllerManagedBy(mgr).
    For(&appsv1.Deployment{}, builder.WithPredicates(
        predicate.GenerationChangedPredicate{},
    ))
```

This can reduce reconciliations by 50-90% in typical scenarios.

## Related Packages

- [Source Package](/docs/07-source/) - Generates events filtered by predicates
- [Handler Package](/docs/08-handler/) - Processes events that pass predicates
- [Controller Package](/docs/02-controller/) - Uses predicates
- [Builder Package](/docs/04-builder/) - Configures predicates
