---
title: "Cache"
weight: 6
---


## Overview

The `pkg/cache` package provides an in-memory cache of Kubernetes objects backed by informers. The cache reduces load on the API server and improves controller performance by serving read requests from local memory.

## Package Location

```
pkg/cache/
├── cache.go                # Cache interface and implementation
├── informer_cache.go       # Informer-based cache
├── multi_namespace_cache.go # Multi-namespace cache
├── delegating_by_gvk_cache.go # GVK-based cache delegation
└── internal/               # Internal implementation
```

## Core Concepts

### Cache Architecture

<div class="mermaid-diagram">
<svg aria-roledescription="flowchart-v2" role="graphics-document document" viewBox="-43 -8 485.603515625 402" style="max-width: 485.604px; background-color: transparent;" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" width="100%" id="my-svg"><style>#my-svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}#my-svg .error-icon{fill:#552222;}#my-svg .error-text{fill:#552222;stroke:#552222;}#my-svg .edge-thickness-normal{stroke-width:2px;}#my-svg .edge-thickness-thick{stroke-width:3.5px;}#my-svg .edge-pattern-solid{stroke-dasharray:0;}#my-svg .edge-pattern-dashed{stroke-dasharray:3;}#my-svg .edge-pattern-dotted{stroke-dasharray:2;}#my-svg .marker{fill:#333333;stroke:#333333;}#my-svg .marker.cross{stroke:#333333;}#my-svg svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#my-svg .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#333;}#my-svg .cluster-label text{fill:#333;}#my-svg .cluster-label span,#my-svg p{color:#333;}#my-svg .label text,#my-svg span,#my-svg p{fill:#333;color:#333;}#my-svg .node rect,#my-svg .node circle,#my-svg .node ellipse,#my-svg .node polygon,#my-svg .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#my-svg .flowchart-label text{text-anchor:middle;}#my-svg .node .label{text-align:center;}#my-svg .node.clickable{cursor:pointer;}#my-svg .arrowheadPath{fill:#333333;}#my-svg .edgePath .path{stroke:#333333;stroke-width:2.0px;}#my-svg .flowchart-link{stroke:#333333;fill:none;}#my-svg .edgeLabel{background-color:#e8e8e8;text-align:center;}#my-svg .edgeLabel rect{opacity:0.5;background-color:#e8e8e8;fill:#e8e8e8;}#my-svg .labelBkg{background-color:rgba(232, 232, 232, 0.5);}#my-svg .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#my-svg .cluster text{fill:#333;}#my-svg .cluster span,#my-svg p{color:#333;}#my-svg div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(80, 100%, 96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#my-svg .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#333;}#my-svg :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}</style><g><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="6" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointEnd"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 0 L 10 5 L 0 10 z"/></marker><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="4.5" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointStart"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 5 L 10 10 L 10 0 z"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="11" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleEnd"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="-1" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleStart"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="12" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossEnd"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="-1" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossStart"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><g class="root"><g class="clusters"/><g class="edgePaths"><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Cache LE-Informers" id="L-Cache-Informers-0" d="M202.46875,24.451984010673026L229.81217447916666,31.668320008894188C257.1555989583333,38.88465600711535,311.8424479166667,53.31732800355767,339.1858723958333,65.35866400177883C366.529296875,77.39999999999999,366.529296875,87.05,366.529296875,91.875L366.529296875,96.7"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Cache LE-Store" id="L-Cache-Store-0" d="M144.1015625,23.895796215374805L114.25130208333333,31.204830179479004C84.40104166666667,38.5138641435832,24.700520833333332,53.1319320717916,-5.149739583333333,68.9409660358958C-35,84.75,-35,101.75,-35,117.20833333333333C-35,132.66666666666666,-35,146.58333333333334,-35,160.5C-35,174.41666666666666,-35,188.33333333333334,-35,202.25C-35,216.16666666666666,-35,230.08333333333334,-35,244C-35,257.9166666666667,-35,271.8333333333333,-35,285.75C-35,299.6666666666667,-35,313.5833333333333,-11.80560229740488,325.13929317739724C11.388795405190242,336.69525302146116,57.77759081038048,345.89050604292225,80.9719885129756,350.48813255365286L104.16638621557072,355.0857590643834"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Cache LE-Indexer" id="L-Cache-Indexer-0" d="M144.1015625,29.276580530624322L129.16276041666666,35.688817108853605C114.22395833333333,42.10105368708288,84.34635416666667,54.92552684354144,69.40755208333333,66.16276342177072C54.46875,77.39999999999999,54.46875,87.05,54.46875,91.875L54.46875,96.7"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Informers LE-Watch" id="L-Informers-Watch-0" d="M366.529296875,135.5L366.529296875,139.66666666666666C366.529296875,143.83333333333334,366.529296875,152.16666666666666,366.529296875,159.61666666666667C366.529296875,167.06666666666666,366.529296875,173.63333333333333,366.529296875,176.91666666666666L366.529296875,180.2"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Watch LE-Events" id="L-Watch-Events-0" d="M366.529296875,219L366.529296875,223.16666666666666C366.529296875,227.33333333333334,366.529296875,235.66666666666666,366.529296875,243.11666666666667C366.529296875,250.5666666666667,366.529296875,257.1333333333333,366.529296875,260.4166666666667L366.529296875,263.7"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Events LE-Store" id="L-Events-Store-0" d="M366.529296875,302.5L366.529296875,306.6666666666667C366.529296875,310.8333333333333,366.529296875,319.1666666666667,346.6174957759187,327.68791939788935C326.70569467683737,336.209172129112,286.8820924786747,344.91834425822407,266.9702913795934,349.27293032278004L247.05849028051207,353.6275163873361"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Controller LE-Cache" id="L-Controller-Cache-0" d="M244.22650505514707,102L250.20372817095588,96.29166666666667C256.1809512867647,90.58333333333333,268.1353975183824,79.16666666666667,261.97289061202775,67.66152566859171C255.81038370567316,56.15638467051675,231.53092366134635,44.562769341033494,219.39119363918292,38.76596167629187L207.2514636170195,32.969154011550245"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Cache LE-Controller" id="L-Cache-Controller-0" d="M173.28515625,33.5L173.28515625,39.208333333333336C173.28515625,44.916666666666664,173.28515625,56.333333333333336,178.62356490020534,67.13992307344604C183.96197355041068,77.94651281355875,194.63879085082135,88.14302562711752,199.9771995010267,93.24128203389692L205.31560815123203,98.3395384406763"/></g><g class="edgeLabels"><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g transform="translate(280.08984375, 67.75)" class="edgeLabel"><g transform="translate(-17.35546875, -9.25)" class="label"><foreignObject height="18.5" width="34.7109375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Read</span></div></foreignObject></g></g><g transform="translate(173.28515625, 67.75)" class="edgeLabel"><g transform="translate(-69.44921875, -9.25)" class="label"><foreignObject height="18.5" width="138.8984375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Serve from Memory</span></div></foreignObject></g></g></g><g class="nodes"><g transform="translate(173.28515625, 16.75)" id="flowchart-Cache-0" class="node default default flowchart-label"><rect height="33.5" width="58.3671875" y="-16.75" x="-29.18359375" ry="0" rx="0" style="fill:#e1f5ff;" class="basic label-container"/><g transform="translate(-21.68359375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="43.3671875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Cache</span></div></foreignObject></g></g><g transform="translate(366.529296875, 118.75)" id="flowchart-Informers-2" class="node default default flowchart-label"><rect height="33.5" width="83.6171875" y="-16.75" x="-41.80859375" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-34.30859375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="68.6171875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Informers</span></div></foreignObject></g></g><g transform="translate(175.623046875, 369.25)" id="flowchart-Store-4" class="node default default flowchart-label"><rect height="33.5" width="132.515625" y="-16.75" x="-66.2578125" ry="0" rx="0" style="fill:#fff4e1;" class="basic label-container"/><g transform="translate(-58.7578125, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="117.515625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">In-Memory Store</span></div></foreignObject></g></g><g transform="translate(54.46875, 118.75)" id="flowchart-Indexer-6" class="node default default flowchart-label"><rect height="33.5" width="108.9375" y="-16.75" x="-54.46875" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-46.96875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="93.9375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Field Indexer</span></div></foreignObject></g></g><g transform="translate(366.529296875, 202.25)" id="flowchart-Watch-8" class="node default default flowchart-label"><rect height="33.5" width="136.1484375" y="-16.75" x="-68.07421875" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-60.57421875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="121.1484375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Watch API Server</span></div></foreignObject></g></g><g transform="translate(366.529296875, 285.75)" id="flowchart-Events-10" class="node default default flowchart-label"><rect height="33.5" width="130.578125" y="-16.75" x="-65.2890625" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-57.7890625, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="115.578125"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Resource Events</span></div></foreignObject></g></g><g transform="translate(226.6875, 118.75)" id="flowchart-Controller-13" class="node default default flowchart-label"><rect height="33.5" width="87.4296875" y="-16.75" x="-43.71484375" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-36.21484375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="72.4296875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Controller</span></div></foreignObject></g></g></g></g></g></svg>
</div>

## Cache Interface

The Cache interface combines Reader and Informers:

```go
type Cache interface {
    // Reader interface for reading objects
    client.Reader
    
    // Informers interface for managing informers
    Informers
}

type Informers interface {
    // GetInformer fetches or constructs an informer
    GetInformer(ctx context.Context, obj client.Object, opts ...InformerGetOption) (Informer, error)
    
    // GetInformerForKind fetches an informer by GVK
    GetInformerForKind(ctx context.Context, gvk schema.GroupVersionKind, opts ...InformerGetOption) (Informer, error)
    
    // RemoveInformer removes and stops an informer
    RemoveInformer(ctx context.Context, obj client.Object) error
    
    // Start runs all informers
    Start(ctx context.Context) error
    
    // WaitForCacheSync waits for all caches to sync
    WaitForCacheSync(ctx context.Context) bool
    
    // FieldIndexer for adding field indexes
    client.FieldIndexer
}
```

## Creating a Cache

### Basic Cache Creation

```go
import (
    "sigs.k8s.io/controller-runtime/pkg/cache"
    "sigs.k8s.io/controller-runtime/pkg/client/config"
)

// Create a cache
c, err := cache.New(config.GetConfigOrDie(), cache.Options{
    Scheme: scheme,
})

// Start the cache
go func() {
    if err := c.Start(ctx); err != nil {
        // Handle error
    }
}()

// Wait for cache to sync
if !c.WaitForCacheSync(ctx) {
    // Cache didn't sync
}
```

### Cache from Manager

The manager automatically creates and manages a cache:

```go
mgr, err := ctrl.NewManager(cfg, ctrl.Options{
    Cache: cache.Options{
        // Cache configuration
    },
})

// Get the cache
cache := mgr.GetCache()
```

## Cache Options

### Namespace Filtering

```go
// Watch specific namespaces
cache.Options{
    DefaultNamespaces: map[string]cache.Config{
        "namespace1": {},
        "namespace2": {},
    },
}

// Watch all namespaces (default)
cache.Options{
    // No DefaultNamespaces specified
}
```

### Label and Field Selectors

```go
// Global label selector for all resources
cache.Options{
    DefaultLabelSelector: labels.SelectorFromSet(labels.Set{
        "managed-by": "my-controller",
    }),
}

// Per-resource selectors
cache.Options{
    ByObject: map[client.Object]cache.ByObject{
        &corev1.Pod{}: {
            Label: labels.SelectorFromSet(labels.Set{"app": "myapp"}),
            Field: fields.SelectorFromSet(fields.Set{"spec.nodeName": "node-1"}),
        },
    },
}
```

### Transform Functions

Reduce memory usage by transforming objects before caching:

```go
cache.Options{
    DefaultTransform: func(obj interface{}) (interface{}, error) {
        // Remove unnecessary fields
        if pod, ok := obj.(*corev1.Pod); ok {
            pod.ManagedFields = nil
            pod.Annotations = nil
        }
        return obj, nil
    },
}

// Per-resource transforms
cache.Options{
    ByObject: map[client.Object]cache.ByObject{
        &corev1.Pod{}: {
            Transform: func(obj interface{}) (interface{}, error) {
                // Custom transform for Pods
                return obj, nil
            },
        },
    },
}
```

### Sync Period

```go
// Set sync period (default: 10 hours)
cache.Options{
    SyncPeriod: ptr.To(5 * time.Minute),
}
```

### Namespace-Specific Configuration

```go
cache.Options{
    DefaultNamespaces: map[string]cache.Config{
        "namespace1": {
            LabelSelector: labels.SelectorFromSet(labels.Set{"env": "prod"}),
            FieldSelector: fields.SelectorFromSet(fields.Set{"status.phase": "Running"}),
        },
        "namespace2": {
            LabelSelector: labels.SelectorFromSet(labels.Set{"env": "dev"}),
        },
    },
}
```

## Reading from Cache

### Get Operation

```go
// Get a Pod from cache
var pod corev1.Pod
err := cache.Get(ctx, types.NamespacedName{
    Name:      "my-pod",
    Namespace: "default",
}, &pod)
```

### List Operation

```go
// List all Pods from cache
var podList corev1.PodList
err := cache.List(ctx, &podList, &client.ListOptions{
    Namespace: "default",
})

// List with label selector
err = cache.List(ctx, &podList,
    client.InNamespace("default"),
    client.MatchingLabels{"app": "myapp"})

// List with field selector (requires index)
err = cache.List(ctx, &podList,
    client.MatchingFields{"spec.nodeName": "node-1"})
```

## Field Indexing

Field indexes enable efficient lookups by field values:

### Adding an Index

```go
// Index Pods by node name
err := cache.IndexField(ctx, &corev1.Pod{}, "spec.nodeName",
    func(obj client.Object) []string {
        pod := obj.(*corev1.Pod)
        if pod.Spec.NodeName == "" {
            return nil
        }
        return []string{pod.Spec.NodeName}
    })

// Index Pods by owner reference
err = cache.IndexField(ctx, &corev1.Pod{}, "owner",
    func(obj client.Object) []string {
        pod := obj.(*corev1.Pod)
        var owners []string
        for _, ref := range pod.OwnerReferences {
            owners = append(owners, string(ref.UID))
        }
        return owners
    })
```

### Using an Index

```go
// List Pods on a specific node using the index
var podList corev1.PodList
err := cache.List(ctx, &podList,
    client.MatchingFields{"spec.nodeName": "node-1"})

// List Pods owned by a specific object
err = cache.List(ctx, &podList,
    client.MatchingFields{"owner": string(owner.UID)})
```

### Common Indexes

```go
// Index by owner reference
cache.IndexField(ctx, &corev1.Pod{}, ".metadata.ownerReferences.uid",
    func(obj client.Object) []string {
        pod := obj.(*corev1.Pod)
        var uids []string
        for _, ref := range pod.OwnerReferences {
            uids = append(uids, string(ref.UID))
        }
        return uids
    })

// Index by label
cache.IndexField(ctx, &corev1.Pod{}, ".metadata.labels.app",
    func(obj client.Object) []string {
        pod := obj.(*corev1.Pod)
        if app, ok := pod.Labels["app"]; ok {
            return []string{app}
        }
        return nil
    })

// Index by status field
cache.IndexField(ctx, &corev1.Pod{}, ".status.phase",
    func(obj client.Object) []string {
        pod := obj.(*corev1.Pod)
        return []string{string(pod.Status.Phase)}
    })
```

## Informers

### Getting an Informer

```go
// Get informer for a resource type
informer, err := cache.GetInformer(ctx, &corev1.Pod{})

// Get informer by GVK
gvk := schema.GroupVersionKind{
    Group:   "",
    Version: "v1",
    Kind:    "Pod",
}
informer, err = cache.GetInformerForKind(ctx, gvk)
```

### Using Informers

```go
// Add event handler to informer
registration, err := informer.AddEventHandler(toolscache.ResourceEventHandlerFuncs{
    AddFunc: func(obj interface{}) {
        // Handle add
    },
    UpdateFunc: func(oldObj, newObj interface{}) {
        // Handle update
    },
    DeleteFunc: func(obj interface{}) {
        // Handle delete
    },
})

// Remove event handler
err = informer.RemoveEventHandler(registration)
```

### Informer Options

```go
// Block until informer is synced
informer, err := cache.GetInformer(ctx, &corev1.Pod{},
    cache.BlockUntilSynced(true))
```

## Cache Lifecycle

### Starting the Cache

<div class="mermaid-diagram">
<svg aria-roledescription="sequence" role="graphics-document document" viewBox="-50 -10 953 523" style="max-width: 953px; background-color: transparent;" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" width="100%" id="my-svg"><g><rect class="actor" ry="3" rx="3" height="65" width="150" stroke="#666" fill="#eaeaea" y="437" x="703"/><text style="text-anchor: middle; font-size: 16px; font-weight: 400;" class="actor" alignment-baseline="central" dominant-baseline="central" y="469.5" x="778"><tspan dy="0" x="778">APIServer</tspan></text></g><g><rect class="actor" ry="3" rx="3" height="65" width="150" stroke="#666" fill="#eaeaea" y="437" x="503"/><text style="text-anchor: middle; font-size: 16px; font-weight: 400;" class="actor" alignment-baseline="central" dominant-baseline="central" y="469.5" x="578"><tspan dy="0" x="578">Informers</tspan></text></g><g><rect class="actor" ry="3" rx="3" height="65" width="150" stroke="#666" fill="#eaeaea" y="437" x="303"/><text style="text-anchor: middle; font-size: 16px; font-weight: 400;" class="actor" alignment-baseline="central" dominant-baseline="central" y="469.5" x="378"><tspan dy="0" x="378">Cache</tspan></text></g><g><rect class="actor" ry="3" rx="3" height="65" width="150" stroke="#666" fill="#eaeaea" y="437" x="0"/><text style="text-anchor: middle; font-size: 16px; font-weight: 400;" class="actor" alignment-baseline="central" dominant-baseline="central" y="469.5" x="75"><tspan dy="0" x="75">User</tspan></text></g><g><line stroke="#999" stroke-width="0.5px" class="200" y2="437" x2="778" y1="5" x1="778" id="actor3"/><g id="root-3"><rect class="actor" ry="3" rx="3" height="65" width="150" stroke="#666" fill="#eaeaea" y="0" x="703"/><text style="text-anchor: middle; font-size: 16px; font-weight: 400;" class="actor" alignment-baseline="central" dominant-baseline="central" y="32.5" x="778"><tspan dy="0" x="778">APIServer</tspan></text></g></g><g><line stroke="#999" stroke-width="0.5px" class="200" y2="437" x2="578" y1="5" x1="578" id="actor2"/><g id="root-2"><rect class="actor" ry="3" rx="3" height="65" width="150" stroke="#666" fill="#eaeaea" y="0" x="503"/><text style="text-anchor: middle; font-size: 16px; font-weight: 400;" class="actor" alignment-baseline="central" dominant-baseline="central" y="32.5" x="578"><tspan dy="0" x="578">Informers</tspan></text></g></g><g><line stroke="#999" stroke-width="0.5px" class="200" y2="437" x2="378" y1="5" x1="378" id="actor1"/><g id="root-1"><rect class="actor" ry="3" rx="3" height="65" width="150" stroke="#666" fill="#eaeaea" y="0" x="303"/><text style="text-anchor: middle; font-size: 16px; font-weight: 400;" class="actor" alignment-baseline="central" dominant-baseline="central" y="32.5" x="378"><tspan dy="0" x="378">Cache</tspan></text></g></g><g><line stroke="#999" stroke-width="0.5px" class="200" y2="437" x2="75" y1="5" x1="75" id="actor0"/><g id="root-0"><rect class="actor" ry="3" rx="3" height="65" width="150" stroke="#666" fill="#eaeaea" y="0" x="0"/><text style="text-anchor: middle; font-size: 16px; font-weight: 400;" class="actor" alignment-baseline="central" dominant-baseline="central" y="32.5" x="75"><tspan dy="0" x="75">User</tspan></text></g></g><style>#my-svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}#my-svg .error-icon{fill:#552222;}#my-svg .error-text{fill:#552222;stroke:#552222;}#my-svg .edge-thickness-normal{stroke-width:2px;}#my-svg .edge-thickness-thick{stroke-width:3.5px;}#my-svg .edge-pattern-solid{stroke-dasharray:0;}#my-svg .edge-pattern-dashed{stroke-dasharray:3;}#my-svg .edge-pattern-dotted{stroke-dasharray:2;}#my-svg .marker{fill:#333333;stroke:#333333;}#my-svg .marker.cross{stroke:#333333;}#my-svg svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#my-svg .actor{stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:#ECECFF;}#my-svg text.actor&gt;tspan{fill:black;stroke:none;}#my-svg .actor-line{stroke:grey;}#my-svg .messageLine0{stroke-width:1.5;stroke-dasharray:none;stroke:#333;}#my-svg .messageLine1{stroke-width:1.5;stroke-dasharray:2,2;stroke:#333;}#my-svg #arrowhead path{fill:#333;stroke:#333;}#my-svg .sequenceNumber{fill:white;}#my-svg #sequencenumber{fill:#333;}#my-svg #crosshead path{fill:#333;stroke:#333;}#my-svg .messageText{fill:#333;stroke:none;}#my-svg .labelBox{stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:#ECECFF;}#my-svg .labelText,#my-svg .labelText&gt;tspan{fill:black;stroke:none;}#my-svg .loopText,#my-svg .loopText&gt;tspan{fill:black;stroke:none;}#my-svg .loopLine{stroke-width:2px;stroke-dasharray:2,2;stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);}#my-svg .note{stroke:#aaaa33;fill:#fff5ad;}#my-svg .noteText,#my-svg .noteText&gt;tspan{fill:black;stroke:none;}#my-svg .activation0{fill:#f4f4f4;stroke:#666;}#my-svg .activation1{fill:#f4f4f4;stroke:#666;}#my-svg .activation2{fill:#f4f4f4;stroke:#666;}#my-svg .actorPopupMenu{position:absolute;}#my-svg .actorPopupMenuPanel{position:absolute;fill:#ECECFF;box-shadow:0px 8px 16px 0px rgba(0,0,0,0.2);filter:drop-shadow(3px 5px 2px rgb(0 0 0 / 0.4));}#my-svg .actor-man line{stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:#ECECFF;}#my-svg .actor-man circle,#my-svg line{stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:#ECECFF;stroke-width:2px;}#my-svg :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}</style><g/><defs><symbol height="24" width="24" id="computer"><path d="M2 2v13h20v-13h-20zm18 11h-16v-9h16v9zm-10.228 6l.466-1h3.524l.467 1h-4.457zm14.228 3h-24l2-6h2.104l-1.33 4h18.45l-1.297-4h2.073l2 6zm-5-10h-14v-7h14v7z" transform="scale(.5)"/></symbol></defs><defs><symbol clip-rule="evenodd" fill-rule="evenodd" id="database"><path d="M12.258.001l.256.004.255.005.253.008.251.01.249.012.247.015.246.016.242.019.241.02.239.023.236.024.233.027.231.028.229.031.225.032.223.034.22.036.217.038.214.04.211.041.208.043.205.045.201.046.198.048.194.05.191.051.187.053.183.054.18.056.175.057.172.059.168.06.163.061.16.063.155.064.15.066.074.033.073.033.071.034.07.034.069.035.068.035.067.035.066.035.064.036.064.036.062.036.06.036.06.037.058.037.058.037.055.038.055.038.053.038.052.038.051.039.05.039.048.039.047.039.045.04.044.04.043.04.041.04.04.041.039.041.037.041.036.041.034.041.033.042.032.042.03.042.029.042.027.042.026.043.024.043.023.043.021.043.02.043.018.044.017.043.015.044.013.044.012.044.011.045.009.044.007.045.006.045.004.045.002.045.001.045v17l-.001.045-.002.045-.004.045-.006.045-.007.045-.009.044-.011.045-.012.044-.013.044-.015.044-.017.043-.018.044-.02.043-.021.043-.023.043-.024.043-.026.043-.027.042-.029.042-.03.042-.032.042-.033.042-.034.041-.036.041-.037.041-.039.041-.04.041-.041.04-.043.04-.044.04-.045.04-.047.039-.048.039-.05.039-.051.039-.052.038-.053.038-.055.038-.055.038-.058.037-.058.037-.06.037-.06.036-.062.036-.064.036-.064.036-.066.035-.067.035-.068.035-.069.035-.07.034-.071.034-.073.033-.074.033-.15.066-.155.064-.16.063-.163.061-.168.06-.172.059-.175.057-.18.056-.183.054-.187.053-.191.051-.194.05-.198.048-.201.046-.205.045-.208.043-.211.041-.214.04-.217.038-.22.036-.223.034-.225.032-.229.031-.231.028-.233.027-.236.024-.239.023-.241.02-.242.019-.246.016-.247.015-.249.012-.251.01-.253.008-.255.005-.256.004-.258.001-.258-.001-.256-.004-.255-.005-.253-.008-.251-.01-.249-.012-.247-.015-.245-.016-.243-.019-.241-.02-.238-.023-.236-.024-.234-.027-.231-.028-.228-.031-.226-.032-.223-.034-.22-.036-.217-.038-.214-.04-.211-.041-.208-.043-.204-.045-.201-.046-.198-.048-.195-.05-.19-.051-.187-.053-.184-.054-.179-.056-.176-.057-.172-.059-.167-.06-.164-.061-.159-.063-.155-.064-.151-.066-.074-.033-.072-.033-.072-.034-.07-.034-.069-.035-.068-.035-.067-.035-.066-.035-.064-.036-.063-.036-.062-.036-.061-.036-.06-.037-.058-.037-.057-.037-.056-.038-.055-.038-.053-.038-.052-.038-.051-.039-.049-.039-.049-.039-.046-.039-.046-.04-.044-.04-.043-.04-.041-.04-.04-.041-.039-.041-.037-.041-.036-.041-.034-.041-.033-.042-.032-.042-.03-.042-.029-.042-.027-.042-.026-.043-.024-.043-.023-.043-.021-.043-.02-.043-.018-.044-.017-.043-.015-.044-.013-.044-.012-.044-.011-.045-.009-.044-.007-.045-.006-.045-.004-.045-.002-.045-.001-.045v-17l.001-.045.002-.045.004-.045.006-.045.007-.045.009-.044.011-.045.012-.044.013-.044.015-.044.017-.043.018-.044.02-.043.021-.043.023-.043.024-.043.026-.043.027-.042.029-.042.03-.042.032-.042.033-.042.034-.041.036-.041.037-.041.039-.041.04-.041.041-.04.043-.04.044-.04.046-.04.046-.039.049-.039.049-.039.051-.039.052-.038.053-.038.055-.038.056-.038.057-.037.058-.037.06-.037.061-.036.062-.036.063-.036.064-.036.066-.035.067-.035.068-.035.069-.035.07-.034.072-.034.072-.033.074-.033.151-.066.155-.064.159-.063.164-.061.167-.06.172-.059.176-.057.179-.056.184-.054.187-.053.19-.051.195-.05.198-.048.201-.046.204-.045.208-.043.211-.041.214-.04.217-.038.22-.036.223-.034.226-.032.228-.031.231-.028.234-.027.236-.024.238-.023.241-.02.243-.019.245-.016.247-.015.249-.012.251-.01.253-.008.255-.005.256-.004.258-.001.258.001zm-9.258 20.499v.01l.001.021.003.021.004.022.005.021.006.022.007.022.009.023.01.022.011.023.012.023.013.023.015.023.016.024.017.023.018.024.019.024.021.024.022.025.023.024.024.025.052.049.056.05.061.051.066.051.07.051.075.051.079.052.084.052.088.052.092.052.097.052.102.051.105.052.11.052.114.051.119.051.123.051.127.05.131.05.135.05.139.048.144.049.147.047.152.047.155.047.16.045.163.045.167.043.171.043.176.041.178.041.183.039.187.039.19.037.194.035.197.035.202.033.204.031.209.03.212.029.216.027.219.025.222.024.226.021.23.02.233.018.236.016.24.015.243.012.246.01.249.008.253.005.256.004.259.001.26-.001.257-.004.254-.005.25-.008.247-.011.244-.012.241-.014.237-.016.233-.018.231-.021.226-.021.224-.024.22-.026.216-.027.212-.028.21-.031.205-.031.202-.034.198-.034.194-.036.191-.037.187-.039.183-.04.179-.04.175-.042.172-.043.168-.044.163-.045.16-.046.155-.046.152-.047.148-.048.143-.049.139-.049.136-.05.131-.05.126-.05.123-.051.118-.052.114-.051.11-.052.106-.052.101-.052.096-.052.092-.052.088-.053.083-.051.079-.052.074-.052.07-.051.065-.051.06-.051.056-.05.051-.05.023-.024.023-.025.021-.024.02-.024.019-.024.018-.024.017-.024.015-.023.014-.024.013-.023.012-.023.01-.023.01-.022.008-.022.006-.022.006-.022.004-.022.004-.021.001-.021.001-.021v-4.127l-.077.055-.08.053-.083.054-.085.053-.087.052-.09.052-.093.051-.095.05-.097.05-.1.049-.102.049-.105.048-.106.047-.109.047-.111.046-.114.045-.115.045-.118.044-.12.043-.122.042-.124.042-.126.041-.128.04-.13.04-.132.038-.134.038-.135.037-.138.037-.139.035-.142.035-.143.034-.144.033-.147.032-.148.031-.15.03-.151.03-.153.029-.154.027-.156.027-.158.026-.159.025-.161.024-.162.023-.163.022-.165.021-.166.02-.167.019-.169.018-.169.017-.171.016-.173.015-.173.014-.175.013-.175.012-.177.011-.178.01-.179.008-.179.008-.181.006-.182.005-.182.004-.184.003-.184.002h-.37l-.184-.002-.184-.003-.182-.004-.182-.005-.181-.006-.179-.008-.179-.008-.178-.01-.176-.011-.176-.012-.175-.013-.173-.014-.172-.015-.171-.016-.17-.017-.169-.018-.167-.019-.166-.02-.165-.021-.163-.022-.162-.023-.161-.024-.159-.025-.157-.026-.156-.027-.155-.027-.153-.029-.151-.03-.15-.03-.148-.031-.146-.032-.145-.033-.143-.034-.141-.035-.14-.035-.137-.037-.136-.037-.134-.038-.132-.038-.13-.04-.128-.04-.126-.041-.124-.042-.122-.042-.12-.044-.117-.043-.116-.045-.113-.045-.112-.046-.109-.047-.106-.047-.105-.048-.102-.049-.1-.049-.097-.05-.095-.05-.093-.052-.09-.051-.087-.052-.085-.053-.083-.054-.08-.054-.077-.054v4.127zm0-5.654v.011l.001.021.003.021.004.021.005.022.006.022.007.022.009.022.01.022.011.023.012.023.013.023.015.024.016.023.017.024.018.024.019.024.021.024.022.024.023.025.024.024.052.05.056.05.061.05.066.051.07.051.075.052.079.051.084.052.088.052.092.052.097.052.102.052.105.052.11.051.114.051.119.052.123.05.127.051.131.05.135.049.139.049.144.048.147.048.152.047.155.046.16.045.163.045.167.044.171.042.176.042.178.04.183.04.187.038.19.037.194.036.197.034.202.033.204.032.209.03.212.028.216.027.219.025.222.024.226.022.23.02.233.018.236.016.24.014.243.012.246.01.249.008.253.006.256.003.259.001.26-.001.257-.003.254-.006.25-.008.247-.01.244-.012.241-.015.237-.016.233-.018.231-.02.226-.022.224-.024.22-.025.216-.027.212-.029.21-.03.205-.032.202-.033.198-.035.194-.036.191-.037.187-.039.183-.039.179-.041.175-.042.172-.043.168-.044.163-.045.16-.045.155-.047.152-.047.148-.048.143-.048.139-.05.136-.049.131-.05.126-.051.123-.051.118-.051.114-.052.11-.052.106-.052.101-.052.096-.052.092-.052.088-.052.083-.052.079-.052.074-.051.07-.052.065-.051.06-.05.056-.051.051-.049.023-.025.023-.024.021-.025.02-.024.019-.024.018-.024.017-.024.015-.023.014-.023.013-.024.012-.022.01-.023.01-.023.008-.022.006-.022.006-.022.004-.021.004-.022.001-.021.001-.021v-4.139l-.077.054-.08.054-.083.054-.085.052-.087.053-.09.051-.093.051-.095.051-.097.05-.1.049-.102.049-.105.048-.106.047-.109.047-.111.046-.114.045-.115.044-.118.044-.12.044-.122.042-.124.042-.126.041-.128.04-.13.039-.132.039-.134.038-.135.037-.138.036-.139.036-.142.035-.143.033-.144.033-.147.033-.148.031-.15.03-.151.03-.153.028-.154.028-.156.027-.158.026-.159.025-.161.024-.162.023-.163.022-.165.021-.166.02-.167.019-.169.018-.169.017-.171.016-.173.015-.173.014-.175.013-.175.012-.177.011-.178.009-.179.009-.179.007-.181.007-.182.005-.182.004-.184.003-.184.002h-.37l-.184-.002-.184-.003-.182-.004-.182-.005-.181-.007-.179-.007-.179-.009-.178-.009-.176-.011-.176-.012-.175-.013-.173-.014-.172-.015-.171-.016-.17-.017-.169-.018-.167-.019-.166-.02-.165-.021-.163-.022-.162-.023-.161-.024-.159-.025-.157-.026-.156-.027-.155-.028-.153-.028-.151-.03-.15-.03-.148-.031-.146-.033-.145-.033-.143-.033-.141-.035-.14-.036-.137-.036-.136-.037-.134-.038-.132-.039-.13-.039-.128-.04-.126-.041-.124-.042-.122-.043-.12-.043-.117-.044-.116-.044-.113-.046-.112-.046-.109-.046-.106-.047-.105-.048-.102-.049-.1-.049-.097-.05-.095-.051-.093-.051-.09-.051-.087-.053-.085-.052-.083-.054-.08-.054-.077-.054v4.139zm0-5.666v.011l.001.02.003.022.004.021.005.022.006.021.007.022.009.023.01.022.011.023.012.023.013.023.015.023.016.024.017.024.018.023.019.024.021.025.022.024.023.024.024.025.052.05.056.05.061.05.066.051.07.051.075.052.079.051.084.052.088.052.092.052.097.052.102.052.105.051.11.052.114.051.119.051.123.051.127.05.131.05.135.05.139.049.144.048.147.048.152.047.155.046.16.045.163.045.167.043.171.043.176.042.178.04.183.04.187.038.19.037.194.036.197.034.202.033.204.032.209.03.212.028.216.027.219.025.222.024.226.021.23.02.233.018.236.017.24.014.243.012.246.01.249.008.253.006.256.003.259.001.26-.001.257-.003.254-.006.25-.008.247-.01.244-.013.241-.014.237-.016.233-.018.231-.02.226-.022.224-.024.22-.025.216-.027.212-.029.21-.03.205-.032.202-.033.198-.035.194-.036.191-.037.187-.039.183-.039.179-.041.175-.042.172-.043.168-.044.163-.045.16-.045.155-.047.152-.047.148-.048.143-.049.139-.049.136-.049.131-.051.126-.05.123-.051.118-.052.114-.051.11-.052.106-.052.101-.052.096-.052.092-.052.088-.052.083-.052.079-.052.074-.052.07-.051.065-.051.06-.051.056-.05.051-.049.023-.025.023-.025.021-.024.02-.024.019-.024.018-.024.017-.024.015-.023.014-.024.013-.023.012-.023.01-.022.01-.023.008-.022.006-.022.006-.022.004-.022.004-.021.001-.021.001-.021v-4.153l-.077.054-.08.054-.083.053-.085.053-.087.053-.09.051-.093.051-.095.051-.097.05-.1.049-.102.048-.105.048-.106.048-.109.046-.111.046-.114.046-.115.044-.118.044-.12.043-.122.043-.124.042-.126.041-.128.04-.13.039-.132.039-.134.038-.135.037-.138.036-.139.036-.142.034-.143.034-.144.033-.147.032-.148.032-.15.03-.151.03-.153.028-.154.028-.156.027-.158.026-.159.024-.161.024-.162.023-.163.023-.165.021-.166.02-.167.019-.169.018-.169.017-.171.016-.173.015-.173.014-.175.013-.175.012-.177.01-.178.01-.179.009-.179.007-.181.006-.182.006-.182.004-.184.003-.184.001-.185.001-.185-.001-.184-.001-.184-.003-.182-.004-.182-.006-.181-.006-.179-.007-.179-.009-.178-.01-.176-.01-.176-.012-.175-.013-.173-.014-.172-.015-.171-.016-.17-.017-.169-.018-.167-.019-.166-.02-.165-.021-.163-.023-.162-.023-.161-.024-.159-.024-.157-.026-.156-.027-.155-.028-.153-.028-.151-.03-.15-.03-.148-.032-.146-.032-.145-.033-.143-.034-.141-.034-.14-.036-.137-.036-.136-.037-.134-.038-.132-.039-.13-.039-.128-.041-.126-.041-.124-.041-.122-.043-.12-.043-.117-.044-.116-.044-.113-.046-.112-.046-.109-.046-.106-.048-.105-.048-.102-.048-.1-.05-.097-.049-.095-.051-.093-.051-.09-.052-.087-.052-.085-.053-.083-.053-.08-.054-.077-.054v4.153zm8.74-8.179l-.257.004-.254.005-.25.008-.247.011-.244.012-.241.014-.237.016-.233.018-.231.021-.226.022-.224.023-.22.026-.216.027-.212.028-.21.031-.205.032-.202.033-.198.034-.194.036-.191.038-.187.038-.183.04-.179.041-.175.042-.172.043-.168.043-.163.045-.16.046-.155.046-.152.048-.148.048-.143.048-.139.049-.136.05-.131.05-.126.051-.123.051-.118.051-.114.052-.11.052-.106.052-.101.052-.096.052-.092.052-.088.052-.083.052-.079.052-.074.051-.07.052-.065.051-.06.05-.056.05-.051.05-.023.025-.023.024-.021.024-.02.025-.019.024-.018.024-.017.023-.015.024-.014.023-.013.023-.012.023-.01.023-.01.022-.008.022-.006.023-.006.021-.004.022-.004.021-.001.021-.001.021.001.021.001.021.004.021.004.022.006.021.006.023.008.022.01.022.01.023.012.023.013.023.014.023.015.024.017.023.018.024.019.024.02.025.021.024.023.024.023.025.051.05.056.05.06.05.065.051.07.052.074.051.079.052.083.052.088.052.092.052.096.052.101.052.106.052.11.052.114.052.118.051.123.051.126.051.131.05.136.05.139.049.143.048.148.048.152.048.155.046.16.046.163.045.168.043.172.043.175.042.179.041.183.04.187.038.191.038.194.036.198.034.202.033.205.032.21.031.212.028.216.027.22.026.224.023.226.022.231.021.233.018.237.016.241.014.244.012.247.011.25.008.254.005.257.004.26.001.26-.001.257-.004.254-.005.25-.008.247-.011.244-.012.241-.014.237-.016.233-.018.231-.021.226-.022.224-.023.22-.026.216-.027.212-.028.21-.031.205-.032.202-.033.198-.034.194-.036.191-.038.187-.038.183-.04.179-.041.175-.042.172-.043.168-.043.163-.045.16-.046.155-.046.152-.048.148-.048.143-.048.139-.049.136-.05.131-.05.126-.051.123-.051.118-.051.114-.052.11-.052.106-.052.101-.052.096-.052.092-.052.088-.052.083-.052.079-.052.074-.051.07-.052.065-.051.06-.05.056-.05.051-.05.023-.025.023-.024.021-.024.02-.025.019-.024.018-.024.017-.023.015-.024.014-.023.013-.023.012-.023.01-.023.01-.022.008-.022.006-.023.006-.021.004-.022.004-.021.001-.021.001-.021-.001-.021-.001-.021-.004-.021-.004-.022-.006-.021-.006-.023-.008-.022-.01-.022-.01-.023-.012-.023-.013-.023-.014-.023-.015-.024-.017-.023-.018-.024-.019-.024-.02-.025-.021-.024-.023-.024-.023-.025-.051-.05-.056-.05-.06-.05-.065-.051-.07-.052-.074-.051-.079-.052-.083-.052-.088-.052-.092-.052-.096-.052-.101-.052-.106-.052-.11-.052-.114-.052-.118-.051-.123-.051-.126-.051-.131-.05-.136-.05-.139-.049-.143-.048-.148-.048-.152-.048-.155-.046-.16-.046-.163-.045-.168-.043-.172-.043-.175-.042-.179-.041-.183-.04-.187-.038-.191-.038-.194-.036-.198-.034-.202-.033-.205-.032-.21-.031-.212-.028-.216-.027-.22-.026-.224-.023-.226-.022-.231-.021-.233-.018-.237-.016-.241-.014-.244-.012-.247-.011-.25-.008-.254-.005-.257-.004-.26-.001-.26.001z" transform="scale(.5)"/></symbol></defs><defs><symbol height="24" width="24" id="clock"><path d="M12 2c5.514 0 10 4.486 10 10s-4.486 10-10 10-10-4.486-10-10 4.486-10 10-10zm0-2c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm5.848 12.459c.202.038.202.333.001.372-1.907.361-6.045 1.111-6.547 1.111-.719 0-1.301-.582-1.301-1.301 0-.512.77-5.447 1.125-7.445.034-.192.312-.181.343.014l.985 6.238 5.394 1.011z" transform="scale(.5)"/></symbol></defs><defs><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="7.9" id="arrowhead"><path d="M 0 0 L 10 5 L 0 10 z"/></marker></defs><defs><marker refY="4.5" refX="4" orient="auto" markerHeight="8" markerWidth="15" id="crosshead"><path style="stroke-dasharray: 0, 0;" d="M 1,2 L 6,7 M 6,2 L 1,7" stroke-width="1pt" stroke="#000000" fill="none"/></marker></defs><defs><marker orient="auto" markerHeight="28" markerWidth="20" refY="7" refX="15.5" id="filled-head"><path d="M 18,7 L9,13 L14,7 L9,1 Z"/></marker></defs><defs><marker orient="auto" markerHeight="40" markerWidth="60" refY="15" refX="15" id="sequencenumber"><circle r="6" cy="15" cx="15"/></marker></defs><text style="font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="80" x="225">Start(ctx)</text><line style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" y2="111" x2="374" y1="111" x1="76"/><text style="font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="126" x="477">Start all informers</text><line style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" y2="157" x2="574" y1="157" x1="379"/><text style="font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="172" x="677">List &amp; Watch</text><line style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" y2="203" x2="774" y1="203" x1="579"/><text style="font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="218" x="680">Initial objects</text><line style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" y2="249" x2="582" y1="249" x1="777"/><text style="font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="264" x="480">Populate store</text><line style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" y2="295" x2="382" y1="295" x1="577"/><text style="font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="310" x="379">Mark as synced</text><path style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" d="M 379,341 C 439,331 439,371 379,361"/><text style="font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="386" x="228">Running (blocks until ctx cancelled)</text><line style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" y2="417" x2="79" y1="417" x1="377"/></svg>
</div>

### Waiting for Sync

```go
// Start cache
go func() {
    if err := cache.Start(ctx); err != nil {
        log.Error(err, "cache start failed")
    }
}()

// Wait for cache to sync (with timeout)
syncCtx, cancel := context.WithTimeout(ctx, 2*time.Minute)
defer cancel()

if !cache.WaitForCacheSync(syncCtx) {
    log.Error(nil, "cache sync timeout")
}
```

## Multi-Namespace Cache

For watching specific namespaces:

```go
cache.Options{
    DefaultNamespaces: map[string]cache.Config{
        "namespace1": {},
        "namespace2": {},
        "namespace3": {},
    },
}
```

### All Namespaces

```go
// Watch all namespaces
cache.Options{
    DefaultNamespaces: map[string]cache.Config{
        cache.AllNamespaces: {},
    },
}

// Or simply don't specify DefaultNamespaces
```

## Cache Patterns

### 1. Namespace-Scoped Cache

```go
mgr, err := ctrl.NewManager(cfg, ctrl.Options{
    Cache: cache.Options{
        DefaultNamespaces: map[string]cache.Config{
            "my-namespace": {},
        },
    },
})
```

### 2. Label-Filtered Cache

```go
mgr, err := ctrl.NewManager(cfg, ctrl.Options{
    Cache: cache.Options{
        DefaultLabelSelector: labels.SelectorFromSet(labels.Set{
            "managed-by": "my-controller",
        }),
    },
})
```

### 3. Resource-Specific Configuration

```go
mgr, err := ctrl.NewManager(cfg, ctrl.Options{
    Cache: cache.Options{
        ByObject: map[client.Object]cache.ByObject{
            &corev1.Pod{}: {
                Label: labels.SelectorFromSet(labels.Set{"app": "myapp"}),
                Namespaces: map[string]cache.Config{
                    "namespace1": {},
                    "namespace2": {},
                },
            },
            &corev1.ConfigMap{}: {
                Transform: func(obj interface{}) (interface{}, error) {
                    // Remove data to save memory
                    if cm, ok := obj.(*corev1.ConfigMap); ok {
                        cm.Data = nil
                        cm.BinaryData = nil
                    }
                    return obj, nil
                },
            },
        },
    },
})
```

### 4. Memory-Optimized Cache

```go
mgr, err := ctrl.NewManager(cfg, ctrl.Options{
    Cache: cache.Options{
        DefaultTransform: func(obj interface{}) (interface{}, error) {
            // Remove unnecessary fields to reduce memory
            if accessor, err := meta.Accessor(obj); err == nil {
                accessor.SetManagedFields(nil)
                // Remove other unnecessary fields
            }
            return obj, nil
        },
    },
})
```

## Cache Consistency

### Read-After-Write Consistency

The cache does NOT guarantee read-after-write consistency:

```go
// Create a Pod
err := client.Create(ctx, &pod)

// This Get might not see the pod immediately!
err = client.Get(ctx, key, &pod)
```

**Solution**: Use the API reader for immediate consistency:

```go
// Create a Pod
err := client.Create(ctx, &pod)

// Read directly from API server
apiReader := mgr.GetAPIReader()
err = apiReader.Get(ctx, key, &pod) // Guaranteed to see the pod
```

### Cache Invalidation

The cache is eventually consistent with the API server:

- Updates from API server are reflected via watch events
- Periodic re-sync ensures consistency (default: 10 hours)
- No manual invalidation needed

## Best Practices

### 1. Use Namespace Filtering

Reduce memory usage by watching only needed namespaces:

```go
cache.Options{
    DefaultNamespaces: map[string]cache.Config{
        "my-namespace": {},
    },
}
```

### 2. Use Label Selectors

Filter objects at the cache level:

```go
cache.Options{
    DefaultLabelSelector: labels.SelectorFromSet(labels.Set{
        "managed-by": "my-controller",
    }),
}
```

### 3. Add Indexes for Frequent Lookups

```go
// Add index for efficient lookups
cache.IndexField(ctx, &corev1.Pod{}, "spec.nodeName", indexFunc)

// Use the index
cache.List(ctx, &podList, client.MatchingFields{"spec.nodeName": "node-1"})
```

### 4. Use Transform Functions

Reduce memory for large objects:

```go
cache.Options{
    DefaultTransform: func(obj interface{}) (interface{}, error) {
        // Remove unnecessary fields
        return obj, nil
    },
}
```

### 5. Wait for Cache Sync

Always wait for cache sync before using:

```go
if !cache.WaitForCacheSync(ctx) {
    return fmt.Errorf("cache sync failed")
}
```

### 6. Use API Reader for Critical Reads

When you need the latest data:

```go
// Use API reader instead of cache
apiReader := mgr.GetAPIReader()
err := apiReader.Get(ctx, key, &obj)
```

## Common Pitfalls

### 1. Not Waiting for Cache Sync

```go
// BAD - reading before cache is synced
cache.Start(ctx)
cache.Get(ctx, key, &obj) // May fail or return stale data

// GOOD - wait for sync
cache.Start(ctx)
cache.WaitForCacheSync(ctx)
cache.Get(ctx, key, &obj)
```

### 2. Expecting Immediate Consistency

```go
// BAD - expecting immediate consistency
client.Create(ctx, &obj)
client.Get(ctx, key, &obj) // May not see the object

// GOOD - use API reader
client.Create(ctx, &obj)
apiReader.Get(ctx, key, &obj) // Guaranteed to see it
```

### 3. Not Using Indexes

```go
// BAD - inefficient without index
cache.List(ctx, &podList)
for _, pod := range podList.Items {
    if pod.Spec.NodeName == "node-1" {
        // Process pod
    }
}

// GOOD - use index
cache.IndexField(ctx, &corev1.Pod{}, "spec.nodeName", indexFunc)
cache.List(ctx, &podList, client.MatchingFields{"spec.nodeName": "node-1"})
```

## Performance Considerations

### Memory Usage

- Each cached object consumes memory
- Use namespace filtering to reduce objects
- Use label selectors to filter objects
- Use transform functions to remove unnecessary fields
- Consider metadata-only watches for large objects

### CPU Usage

- Informers use CPU for processing watch events
- More informers = more CPU usage
- Sync period affects CPU (shorter = more CPU)

### Network Usage

- Initial list operation can be large
- Watch events are incremental
- Sync period affects network usage

## Related Packages

- [Client Package](/docs/05-client/) - Uses cache for reads
- [Manager Package](/docs/01-manager/) - Creates and manages cache
- [Controller Package](/docs/02-controller/) - Uses cache via sources
