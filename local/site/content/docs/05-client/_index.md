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
<svg aria-roledescription="flowchart-v2" role="graphics-document document" viewBox="-8 -8 968.39453125 216.5" style="max-width: 968.395px; background-color: transparent;" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" width="100%" id="my-svg"><style>#my-svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}#my-svg .error-icon{fill:#552222;}#my-svg .error-text{fill:#552222;stroke:#552222;}#my-svg .edge-thickness-normal{stroke-width:2px;}#my-svg .edge-thickness-thick{stroke-width:3.5px;}#my-svg .edge-pattern-solid{stroke-dasharray:0;}#my-svg .edge-pattern-dashed{stroke-dasharray:3;}#my-svg .edge-pattern-dotted{stroke-dasharray:2;}#my-svg .marker{fill:#333333;stroke:#333333;}#my-svg .marker.cross{stroke:#333333;}#my-svg svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#my-svg .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#333;}#my-svg .cluster-label text{fill:#333;}#my-svg .cluster-label span,#my-svg p{color:#333;}#my-svg .label text,#my-svg span,#my-svg p{fill:#333;color:#333;}#my-svg .node rect,#my-svg .node circle,#my-svg .node ellipse,#my-svg .node polygon,#my-svg .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#my-svg .flowchart-label text{text-anchor:middle;}#my-svg .node .label{text-align:center;}#my-svg .node.clickable{cursor:pointer;}#my-svg .arrowheadPath{fill:#333333;}#my-svg .edgePath .path{stroke:#333333;stroke-width:2.0px;}#my-svg .flowchart-link{stroke:#333333;fill:none;}#my-svg .edgeLabel{background-color:#e8e8e8;text-align:center;}#my-svg .edgeLabel rect{opacity:0.5;background-color:#e8e8e8;fill:#e8e8e8;}#my-svg .labelBkg{background-color:rgba(232, 232, 232, 0.5);}#my-svg .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#my-svg .cluster text{fill:#333;}#my-svg .cluster span,#my-svg p{color:#333;}#my-svg div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(80, 100%, 96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#my-svg .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#333;}#my-svg :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}</style><g><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="6" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointEnd"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 0 L 10 5 L 0 10 z"/></marker><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="4.5" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointStart"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 5 L 10 10 L 10 0 z"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="11" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleEnd"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="-1" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleStart"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="12" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossEnd"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="-1" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossStart"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><g class="root"><g class="clusters"/><g class="edgePaths"><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Client LE-Reader" id="L-Client-Reader-0" d="M388.859375,23.68033156619667L335.2936197916667,29.483609638497228C281.7278645833333,35.28688771079778,174.59635416666666,46.89344385539889,121.03059895833333,55.98005526103278C67.46484375,65.06666666666666,67.46484375,71.63333333333334,67.46484375,74.91666666666667L67.46484375,78.2"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Client LE-Writer" id="L-Client-Writer-0" d="M452.828125,33.5L452.828125,37.666666666666664C452.828125,41.833333333333336,452.828125,50.166666666666664,452.828125,57.61666666666667C452.828125,65.06666666666666,452.828125,71.63333333333334,452.828125,74.91666666666667L452.828125,78.2"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Client LE-StatusClient" id="L-Client-StatusClient-0" d="M516.796875,23.207291273139404L575.0677083333334,29.089409394282836C633.3385416666666,34.97152751542627,749.8802083333334,46.73576375771313,808.1510416666666,55.901215212189896C866.421875,65.06666666666666,866.421875,71.63333333333334,866.421875,74.91666666666667L866.421875,78.2"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Reader LE-Get" id="L-Reader-Get-0" d="M54.413384169161674,117L51.16675243263472,121.16666666666667C47.92012069610778,125.33333333333333,41.426857223053894,133.66666666666666,38.18022548652694,141.11666666666667C34.93359375,148.56666666666666,34.93359375,155.13333333333333,34.93359375,158.41666666666666L34.93359375,161.7"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Reader LE-List" id="L-Reader-List-0" d="M90.79699195359282,117L96.60100891966069,121.16666666666667C102.40502588572855,125.33333333333333,114.01305981786429,133.66666666666666,119.81707678393214,141.11666666666667C125.62109375,148.56666666666666,125.62109375,155.13333333333333,125.62109375,158.41666666666666L125.62109375,161.7"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Writer LE-Create" id="L-Writer-Create-0" d="M387.7421875,112.30194906444906L361.01171875,117.25162422037421C334.28125,122.20129937629936,280.8203125,132.10064968814967,254.08984375,140.33365817740818C227.359375,148.56666666666666,227.359375,155.13333333333333,227.359375,158.41666666666666L227.359375,161.7"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Writer LE-Update" id="L-Writer-Update-0" d="M408.4425056137725,117L397.4013067614771,121.16666666666667C386.36010790918164,125.33333333333333,364.27771020459085,133.66666666666666,353.2365113522954,141.11666666666667C342.1953125,148.56666666666666,342.1953125,155.13333333333333,342.1953125,158.41666666666666L342.1953125,161.7"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Writer LE-Patch" id="L-Writer-Patch-0" d="M452.828125,117L452.828125,121.16666666666667C452.828125,125.33333333333333,452.828125,133.66666666666666,452.828125,141.11666666666667C452.828125,148.56666666666666,452.828125,155.13333333333333,452.828125,158.41666666666666L452.828125,161.7"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Writer LE-Delete" id="L-Writer-Delete-0" d="M496.28597492514973,117L507.09638535429144,121.16666666666667C517.9067957834332,125.33333333333333,539.5276166417166,133.66666666666666,550.3380270708583,141.11666666666667C561.1484375,148.56666666666666,561.1484375,155.13333333333333,561.1484375,158.41666666666666L561.1484375,161.7"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Writer LE-DeleteAllOf" id="L-Writer-DeleteAllOf-0" d="M517.9140625,111.65970821237022L546.759765625,116.71642351030852C575.60546875,121.77313880824681,633.296875,131.8865694041234,662.142578125,140.22661803539503C690.98828125,148.56666666666666,690.98828125,155.13333333333333,690.98828125,158.41666666666666L690.98828125,161.7"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-StatusClient LE-StatusWriter" id="L-StatusClient-StatusWriter-0" d="M866.421875,117L866.421875,121.16666666666667C866.421875,125.33333333333333,866.421875,133.66666666666666,866.421875,141.11666666666667C866.421875,148.56666666666666,866.421875,155.13333333333333,866.421875,158.41666666666666L866.421875,161.7"/></g><g class="edgeLabels"><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g></g><g class="nodes"><g transform="translate(452.828125, 16.75)" id="flowchart-Client-0" class="node default default flowchart-label"><rect height="33.5" width="127.9375" y="-16.75" x="-63.96875" ry="0" rx="0" style="fill:#e1f5ff;" class="basic label-container"/><g transform="translate(-56.46875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="112.9375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Client Interface</span></div></foreignObject></g></g><g transform="translate(67.46484375, 100.25)" id="flowchart-Reader-2" class="node default default flowchart-label"><rect height="33.5" width="134.9296875" y="-16.75" x="-67.46484375" ry="0" rx="0" style="fill:#fff4e1;" class="basic label-container"/><g transform="translate(-59.96484375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="119.9296875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Reader Interface</span></div></foreignObject></g></g><g transform="translate(452.828125, 100.25)" id="flowchart-Writer-4" class="node default default flowchart-label"><rect height="33.5" width="130.171875" y="-16.75" x="-65.0859375" ry="0" rx="0" style="fill:#fff4e1;" class="basic label-container"/><g transform="translate(-57.5859375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="115.171875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Writer Interface</span></div></foreignObject></g></g><g transform="translate(866.421875, 100.25)" id="flowchart-StatusClient-6" class="node default default flowchart-label"><rect height="33.5" width="171.9453125" y="-16.75" x="-85.97265625" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-78.47265625, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="156.9453125"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">StatusClient Interface</span></div></foreignObject></g></g><g transform="translate(34.93359375, 183.75)" id="flowchart-Get-8" class="node default default flowchart-label"><rect height="33.5" width="40.890625" y="-16.75" x="-20.4453125" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-12.9453125, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="25.890625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Get</span></div></foreignObject></g></g><g transform="translate(125.62109375, 183.75)" id="flowchart-List-10" class="node default default flowchart-label"><rect height="33.5" width="40.484375" y="-16.75" x="-20.2421875" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-12.7421875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="25.484375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">List</span></div></foreignObject></g></g><g transform="translate(227.359375, 183.75)" id="flowchart-Create-12" class="node default default flowchart-label"><rect height="33.5" width="62.9921875" y="-16.75" x="-31.49609375" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-23.99609375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="47.9921875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Create</span></div></foreignObject></g></g><g transform="translate(342.1953125, 183.75)" id="flowchart-Update-14" class="node default default flowchart-label"><rect height="33.5" width="66.6796875" y="-16.75" x="-33.33984375" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-25.83984375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="51.6796875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Update</span></div></foreignObject></g></g><g transform="translate(452.828125, 183.75)" id="flowchart-Patch-16" class="node default default flowchart-label"><rect height="33.5" width="54.5859375" y="-16.75" x="-27.29296875" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-19.79296875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="39.5859375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Patch</span></div></foreignObject></g></g><g transform="translate(561.1484375, 183.75)" id="flowchart-Delete-18" class="node default default flowchart-label"><rect height="33.5" width="62.0546875" y="-16.75" x="-31.02734375" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-23.52734375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="47.0546875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Delete</span></div></foreignObject></g></g><g transform="translate(690.98828125, 183.75)" id="flowchart-DeleteAllOf-20" class="node default default flowchart-label"><rect height="33.5" width="97.625" y="-16.75" x="-48.8125" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-41.3125, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="82.625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">DeleteAllOf</span></div></foreignObject></g></g><g transform="translate(866.421875, 183.75)" id="flowchart-StatusWriter-22" class="node default default flowchart-label"><rect height="33.5" width="153.2421875" y="-16.75" x="-76.62109375" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-69.12109375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="138.2421875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Status SubResource</span></div></foreignObject></g></g></g></g></g></svg>
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
<svg aria-roledescription="flowchart-v2" role="graphics-document document" viewBox="-8 -8 424.1015625 103" style="max-width: 424.102px; background-color: transparent;" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" width="100%" id="my-svg"><style>#my-svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}#my-svg .error-icon{fill:#552222;}#my-svg .error-text{fill:#552222;stroke:#552222;}#my-svg .edge-thickness-normal{stroke-width:2px;}#my-svg .edge-thickness-thick{stroke-width:3.5px;}#my-svg .edge-pattern-solid{stroke-dasharray:0;}#my-svg .edge-pattern-dashed{stroke-dasharray:3;}#my-svg .edge-pattern-dotted{stroke-dasharray:2;}#my-svg .marker{fill:#333333;stroke:#333333;}#my-svg .marker.cross{stroke:#333333;}#my-svg svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#my-svg .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#333;}#my-svg .cluster-label text{fill:#333;}#my-svg .cluster-label span,#my-svg p{color:#333;}#my-svg .label text,#my-svg span,#my-svg p{fill:#333;color:#333;}#my-svg .node rect,#my-svg .node circle,#my-svg .node ellipse,#my-svg .node polygon,#my-svg .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#my-svg .flowchart-label text{text-anchor:middle;}#my-svg .node .label{text-align:center;}#my-svg .node.clickable{cursor:pointer;}#my-svg .arrowheadPath{fill:#333333;}#my-svg .edgePath .path{stroke:#333333;stroke-width:2.0px;}#my-svg .flowchart-link{stroke:#333333;fill:none;}#my-svg .edgeLabel{background-color:#e8e8e8;text-align:center;}#my-svg .edgeLabel rect{opacity:0.5;background-color:#e8e8e8;fill:#e8e8e8;}#my-svg .labelBkg{background-color:rgba(232, 232, 232, 0.5);}#my-svg .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#my-svg .cluster text{fill:#333;}#my-svg .cluster span,#my-svg p{color:#333;}#my-svg div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(80, 100%, 96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#my-svg .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#333;}#my-svg :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}</style><g><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="6" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointEnd"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 0 L 10 5 L 0 10 z"/></marker><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="4.5" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointStart"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 5 L 10 10 L 10 0 z"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="11" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleEnd"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="-1" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleStart"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="12" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossEnd"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="-1" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossStart"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><g class="root"><g class="clusters"/><g class="edgePaths"><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Client LE-Cache" id="L-Client-Cache-0" d="M94.71875,55.85057909174032L101.77799479166667,58.250482576450274C108.83723958333333,60.65038606116021,122.95572916666667,65.45019303058011,136.19088541666667,67.85009651529005C149.42604166666666,70.25,161.77786458333333,70.25,167.95377604166666,70.25L174.1296875,70.25"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Client LE-API" id="L-Client-API-0" d="M94.71875,23.64942090825968L101.77799479166667,21.249517423549733C108.83723958333333,18.849613938839784,122.95572916666667,14.049806969419892,141.93815104166666,11.649903484709947C160.92057291666666,9.25,184.76692708333334,9.25,208.408203125,9.25C232.04947916666666,9.25,255.48567708333334,9.25,273.2263446377817,11.407173062914188C290.96701219223013,13.564346125828372,303.0121493844602,17.878692251656744,309.0347179805753,20.03586531457093L315.05728657669033,22.193038377485117"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Cache LE-API" id="L-Cache-API-0" d="M237.796875,70.25L244.65104166666666,70.25C251.50520833333334,70.25,265.2135416666667,70.25,278.0902769294484,68.09282693708582C290.96701219223013,65.93565387417162,303.0121493844602,61.62130774834325,309.0347179805753,59.464134685429066L315.05728657669033,57.30696162251488"/></g><g class="edgeLabels"><g transform="translate(137.07421875, 70.25)" class="edgeLabel"><g transform="translate(-17.35546875, -9.25)" class="label"><foreignObject height="18.5" width="34.7109375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Read</span></div></foreignObject></g></g><g transform="translate(208.61328125, 9.25)" class="edgeLabel"><g transform="translate(-19.33984375, -9.25)" class="label"><foreignObject height="18.5" width="38.6796875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Write</span></div></foreignObject></g></g><g transform="translate(278.921875, 70.25)" class="edgeLabel"><g transform="translate(-16.125, -9.25)" class="label"><foreignObject height="18.5" width="32.25"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Sync</span></div></foreignObject></g></g></g><g class="nodes"><g transform="translate(47.359375, 39.75)" id="flowchart-Client-0" class="node default default flowchart-label"><rect height="33.5" width="94.71875" y="-16.75" x="-47.359375" ry="0" rx="0" style="fill:#e1f5ff;" class="basic label-container"/><g transform="translate(-39.859375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="79.71875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Split Client</span></div></foreignObject></g></g><g transform="translate(208.61328125, 70.25)" id="flowchart-Cache-2" class="node default default flowchart-label"><rect height="33.5" width="58.3671875" y="-16.75" x="-29.18359375" ry="0" rx="0" style="fill:#fff4e1;" class="basic label-container"/><g transform="translate(-21.68359375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="43.3671875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Cache</span></div></foreignObject></g></g><g transform="translate(364.07421875, 39.75)" id="flowchart-API-4" class="node default default flowchart-label"><rect height="33.5" width="88.0546875" y="-16.75" x="-44.02734375" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-36.52734375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="73.0546875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">API Server</span></div></foreignObject></g></g></g></g></g></svg>
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
