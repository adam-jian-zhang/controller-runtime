---
title: "Controller-Runtime Documentation"
weight: 100
---


This directory contains comprehensive documentation for the Kubernetes controller-runtime project.

## Documentation Structure

### Core Documentation

1. **[Architecture Overview](/docs/00-overview/)** - High-level architecture and design principles
2. **[Manager Package](/docs/01-manager/)** - Central orchestrator for controllers and webhooks
3. **[Controller Package](/docs/02-controller/)** - Controller implementation and work queue management
4. **[Reconcile Package](/docs/03-reconcile/)** - Reconciler interface and reconciliation patterns
5. **[Builder Package](/docs/04-builder/)** - Fluent API for building controllers
6. **[Client Package](/docs/05-client/)** - Kubernetes API client interface
7. **[Cache Package](/docs/06-cache/)** - Object caching with informers
8. **[Source Package](/docs/07-source/)** - Event sources for controllers
9. **[Handler Package](/docs/08-handler/)** - Event handlers for processing events
10. **[Predicate Package](/docs/09-predicate/)** - Event filtering predicates
11. **[Webhook Package](/docs/10-webhook/)** - Admission and conversion webhooks
12. **[Additional Packages](/docs/11-additional-packages/)** - Supporting packages

## Quick Start

### Basic Controller Example

```go
package main

import (
    "context"
    "os"
    
    corev1 "k8s.io/api/core/v1"
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/client"
    "sigs.k8s.io/controller-runtime/pkg/log"
    "sigs.k8s.io/controller-runtime/pkg/log/zap"
)

type PodReconciler struct {
    client.Client
}

func (r *PodReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := log.FromContext(ctx)
    
    var pod corev1.Pod
    if err := r.Get(ctx, req.NamespacedName, &pod); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    
    log.Info("Reconciling Pod", "name", pod.Name)
    
    return ctrl.Result{}, nil
}

func main() {
    ctrl.SetLogger(zap.New())
    
    mgr, err := ctrl.NewManager(ctrl.GetConfigOrDie(), ctrl.Options{})
    if err != nil {
        os.Exit(1)
    }
    
    err = ctrl.NewControllerManagedBy(mgr).
        For(&corev1.Pod{}).
        Complete(&PodReconciler{
            Client: mgr.GetClient(),
        })
    if err != nil {
        os.Exit(1)
    }
    
    if err := mgr.Start(ctrl.SetupSignalHandler()); err != nil {
        os.Exit(1)
    }
}
```

## Key Concepts

### Level-Based Reconciliation

Controller-runtime uses level-based reconciliation, meaning controllers reconcile based on the current state of the system, not individual events. This makes controllers:

- **Resilient**: Missed events don't cause problems
- **Self-healing**: Controllers continuously converge to desired state
- **Idempotent**: Multiple reconciliations produce the same result

### Separation of Concerns

The framework separates different aspects of controller logic:

- **Source**: Where events come from (e.g., Kubernetes API)
- **Handler**: How to transform events into reconcile requests
- **Predicate**: Which events to process
- **Reconciler**: What to do with the reconcile request

### Shared Dependencies

The Manager provides shared dependencies to all controllers:

- **Cache**: Shared in-memory cache of Kubernetes objects
- **Client**: Unified client for API operations
- **Scheme**: Type registration for serialization
- **REST Mapper**: Mapping between Go types and API resources

## Architecture Diagram

<div class="mermaid-diagram">
<svg aria-roledescription="flowchart-v2" role="graphics-document document" viewBox="-8 -8 443.376953125 700.5" style="max-width: 443.377px; background-color: transparent;" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" width="100%" id="my-svg"><style>#my-svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}#my-svg .error-icon{fill:#552222;}#my-svg .error-text{fill:#552222;stroke:#552222;}#my-svg .edge-thickness-normal{stroke-width:2px;}#my-svg .edge-thickness-thick{stroke-width:3.5px;}#my-svg .edge-pattern-solid{stroke-dasharray:0;}#my-svg .edge-pattern-dashed{stroke-dasharray:3;}#my-svg .edge-pattern-dotted{stroke-dasharray:2;}#my-svg .marker{fill:#333333;stroke:#333333;}#my-svg .marker.cross{stroke:#333333;}#my-svg svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#my-svg .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#333;}#my-svg .cluster-label text{fill:#333;}#my-svg .cluster-label span,#my-svg p{color:#333;}#my-svg .label text,#my-svg span,#my-svg p{fill:#333;color:#333;}#my-svg .node rect,#my-svg .node circle,#my-svg .node ellipse,#my-svg .node polygon,#my-svg .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#my-svg .flowchart-label text{text-anchor:middle;}#my-svg .node .label{text-align:center;}#my-svg .node.clickable{cursor:pointer;}#my-svg .arrowheadPath{fill:#333333;}#my-svg .edgePath .path{stroke:#333333;stroke-width:2.0px;}#my-svg .flowchart-link{stroke:#333333;fill:none;}#my-svg .edgeLabel{background-color:#e8e8e8;text-align:center;}#my-svg .edgeLabel rect{opacity:0.5;background-color:#e8e8e8;fill:#e8e8e8;}#my-svg .labelBkg{background-color:rgba(232, 232, 232, 0.5);}#my-svg .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#my-svg .cluster text{fill:#333;}#my-svg .cluster span,#my-svg p{color:#333;}#my-svg div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(80, 100%, 96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#my-svg .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#333;}#my-svg :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}</style><g><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="6" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointEnd"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 0 L 10 5 L 0 10 z"/></marker><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="4.5" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointStart"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 5 L 10 10 L 10 0 z"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="11" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleEnd"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="-1" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleStart"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="12" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossEnd"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="-1" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossStart"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><g class="root"><g class="clusters"><g id="subGraph2" class="cluster default flowchart-label"><rect height="167" width="385.1875" y="517.5" x="0" ry="0" rx="0" style=""/><g transform="translate(139.0546875, 517.5)" class="cluster-label"><foreignObject height="18.5" width="107.078125"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Kubernetes API</span></div></foreignObject></g></g><g id="subGraph1" class="cluster default flowchart-label"><rect height="334" width="421.57421875" y="133.5" x="5.802734375" ry="0" rx="0" style=""/><g transform="translate(105.49609375, 133.5)" class="cluster-label"><foreignObject height="18.5" width="222.1875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Controller-Runtime Framework</span></div></foreignObject></g></g><g id="subGraph0" class="cluster default flowchart-label"><rect height="83.5" width="278.4375" y="0" x="43.23828125" ry="0" rx="0" style=""/><g transform="translate(146.25, 0)" class="cluster-label"><foreignObject height="18.5" width="72.4140625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">User Code</span></div></foreignObject></g></g></g><g class="edgePaths"><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Reconciler LE-Builder" id="L-Reconciler-Builder-0" d="M182.45703125,58.5L182.45703125,62.666666666666664C182.45703125,66.83333333333333,182.45703125,75.16666666666667,182.45703125,83.5C182.45703125,91.83333333333333,182.45703125,100.16666666666667,182.45703125,108.5C182.45703125,116.83333333333333,182.45703125,125.16666666666667,182.45703125,132.61666666666667C182.45703125,140.06666666666666,182.45703125,146.63333333333333,182.45703125,149.91666666666666L182.45703125,153.2"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Builder LE-Controller" id="L-Builder-Controller-0" d="M182.45703125,192L182.45703125,196.16666666666666C182.45703125,200.33333333333334,182.45703125,208.66666666666666,182.45703125,216.11666666666667C182.45703125,223.5666666666667,182.45703125,230.13333333333333,182.45703125,233.41666666666666L182.45703125,236.7"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Controller LE-Manager" id="L-Controller-Manager-0" d="M182.45703125,275.5L182.45703125,279.6666666666667C182.45703125,283.8333333333333,182.45703125,292.1666666666667,182.45703125,299.6166666666667C182.45703125,307.06666666666666,182.45703125,313.6333333333333,182.45703125,316.9166666666667L182.45703125,320.2"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Manager LE-Cache" id="L-Manager-Cache-0" d="M182.84647501871257,359L182.94335157809383,363.1666666666667C183.04022813747505,367.3333333333333,183.2339812562375,375.6666666666667,183.33085781561877,383.1166666666666C183.427734375,390.56666666666666,183.427734375,397.1333333333334,183.427734375,400.4166666666667L183.427734375,403.7"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Manager LE-Client" id="L-Manager-Client-0" d="M145.015625,356.10523240716697L132.4521484375,360.75436033930583C119.888671875,365.4034882714447,94.76171875,374.7017441357223,82.1982421875,382.6342054011945C69.634765625,390.56666666666666,69.634765625,397.1333333333334,69.634765625,400.4166666666667L69.634765625,403.7"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Manager LE-Webhook" id="L-Manager-Webhook-0" d="M219.8984375,353.0277845109684L237.8310546875,358.189820425807C255.763671875,363.35185634064555,291.62890625,373.6759281703228,309.5615234375,382.12129741849475C327.494140625,390.56666666666666,327.494140625,397.1333333333334,327.494140625,400.4166666666667L327.494140625,403.7"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Cache LE-Informers" id="L-Cache-Informers-0" d="M183.427734375,442.5L183.427734375,446.6666666666667C183.427734375,450.8333333333333,183.427734375,459.1666666666667,183.427734375,467.5C183.427734375,475.8333333333333,183.427734375,484.1666666666667,183.427734375,492.5C183.427734375,500.8333333333333,183.427734375,509.1666666666667,183.427734375,516.6166666666667C183.427734375,524.0666666666667,183.427734375,530.6333333333333,183.427734375,533.9166666666666L183.427734375,537.2"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Client LE-APIServer" id="L-Client-APIServer-0" d="M69.634765625,442.5L69.634765625,446.6666666666667C69.634765625,450.8333333333333,69.634765625,459.1666666666667,69.634765625,467.5C69.634765625,475.8333333333333,69.634765625,484.1666666666667,69.634765625,492.5C69.634765625,500.8333333333333,69.634765625,509.1666666666667,69.634765625,520.2916666666666C69.634765625,531.4166666666666,69.634765625,545.3333333333334,69.634765625,559.25C69.634765625,573.1666666666666,69.634765625,587.0833333333334,81.05614098171488,597.9240443342366C92.47751633842977,608.76475533514,115.32026705185955,616.5295106702798,126.74164240857442,620.4118883378497L138.1630177652893,624.2942660054198"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Informers LE-APIServer" id="L-Informers-APIServer-0" d="M183.427734375,576L183.427734375,580.1666666666666C183.427734375,584.3333333333334,183.427734375,592.6666666666666,184.1421396646905,600.1366271841713C184.85654495438098,607.6065877016758,186.28535553376193,614.2131754033516,186.99976082345242,617.5164692541895L187.71416611314288,620.8197631050274"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Webhook LE-APIServer" id="L-Webhook-APIServer-0" d="M327.494140625,442.5L327.494140625,446.6666666666667C327.494140625,450.8333333333333,327.494140625,459.1666666666667,327.494140625,467.5C327.494140625,475.8333333333333,327.494140625,484.1666666666667,327.494140625,492.5C327.494140625,500.8333333333333,327.494140625,509.1666666666667,327.494140625,520.2916666666666C327.494140625,531.4166666666666,327.494140625,545.3333333333334,327.494140625,559.25C327.494140625,573.1666666666666,327.494140625,587.0833333333334,314.8613023506749,597.9474152449217C302.22846407634984,608.81149715651,276.9627875276997,616.6229943130201,264.3299492533746,620.5287428912751L251.69711097904954,624.43449146953"/></g><g class="edgeLabels"><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g></g><g class="nodes"><g transform="translate(192.45703125, 642.75)" id="flowchart-APIServer-7" class="node default default flowchart-label"><rect height="33.5" width="172.3203125" y="-16.75" x="-86.16015625" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-78.66015625, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="157.3203125"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Kubernetes API Server</span></div></foreignObject></g></g><g transform="translate(183.427734375, 559.25)" id="flowchart-Informers-8" class="node default default flowchart-label"><rect height="33.5" width="157.5859375" y="-16.75" x="-78.79296875" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-71.29296875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="142.5859375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Informers/Watchers</span></div></foreignObject></g></g><g transform="translate(182.45703125, 342.25)" id="flowchart-Manager-1" class="node default default flowchart-label"><rect height="33.5" width="74.8828125" y="-16.75" x="-37.44140625" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-29.94140625, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="59.8828125"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Manager</span></div></foreignObject></g></g><g transform="translate(182.45703125, 175.25)" id="flowchart-Builder-2" class="node default default flowchart-label"><rect height="33.5" width="65.9375" y="-16.75" x="-32.96875" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-25.46875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="50.9375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Builder</span></div></foreignObject></g></g><g transform="translate(182.45703125, 258.75)" id="flowchart-Controller-3" class="node default default flowchart-label"><rect height="33.5" width="87.4296875" y="-16.75" x="-43.71484375" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-36.21484375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="72.4296875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Controller</span></div></foreignObject></g></g><g transform="translate(183.427734375, 425.75)" id="flowchart-Cache-4" class="node default default flowchart-label"><rect height="33.5" width="58.3671875" y="-16.75" x="-29.18359375" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-21.68359375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="43.3671875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Cache</span></div></foreignObject></g></g><g transform="translate(69.634765625, 425.75)" id="flowchart-Client-5" class="node default default flowchart-label"><rect height="33.5" width="57.6640625" y="-16.75" x="-28.83203125" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-21.33203125, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="42.6640625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Client</span></div></foreignObject></g></g><g transform="translate(327.494140625, 425.75)" id="flowchart-Webhook-6" class="node default default flowchart-label"><rect height="33.5" width="129.765625" y="-16.75" x="-64.8828125" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-57.3828125, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="114.765625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Webhook Server</span></div></foreignObject></g></g><g transform="translate(182.45703125, 41.75)" id="flowchart-Reconciler-0" class="node default default flowchart-label"><rect height="33.5" width="208.4375" y="-16.75" x="-104.21875" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-96.71875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="193.4375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Reconciler Implementation</span></div></foreignObject></g></g></g></g></g></svg>
</div>

## Common Use Cases

### 1. Custom Resource Controller

Build a controller for your Custom Resource Definition (CRD):

```go
err := ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}).
    Owns(&corev1.Pod{}).
    Owns(&corev1.Service{}).
    Complete(&MyResourceReconciler{})
```

### 2. Built-in Resource Controller

Watch and react to built-in Kubernetes resources:

```go
err := ctrl.NewControllerManagedBy(mgr).
    For(&corev1.Pod{}).
    Complete(&PodReconciler{})
```

### 3. Multi-Resource Controller

Watch multiple related resources:

```go
err := ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}).
    Watches(&corev1.ConfigMap{}, 
        handler.EnqueueRequestsFromMapFunc(mapFunc)).
    Watches(&corev1.Secret{},
        handler.EnqueueRequestsFromMapFunc(mapFunc)).
    Complete(&MyResourceReconciler{})
```

### 4. Admission Webhook

Implement validating and mutating webhooks:

```go
err := ctrl.NewWebhookManagedBy(mgr).
    For(&myv1.MyResource{}).
    WithDefaulter(&MyResourceDefaulter{}).
    WithValidator(&MyResourceValidator{}).
    Complete()
```

## Best Practices

### 1. Idempotent Reconciliation

Ensure your reconcile logic can be called multiple times safely:

```go
func (r *MyReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // Check if work is already done
    if isAlreadyDone() {
        return ctrl.Result{}, nil
    }
    
    // Do work
    return ctrl.Result{}, nil
}
```

### 2. Handle Deletion with Finalizers

Use finalizers for cleanup when objects are deleted:

```go
if !obj.DeletionTimestamp.IsZero() {
    if controllerutil.ContainsFinalizer(obj, myFinalizer) {
        // Perform cleanup
        if err := cleanup(); err != nil {
            return ctrl.Result{}, err
        }
        // Remove finalizer
        controllerutil.RemoveFinalizer(obj, myFinalizer)
        return ctrl.Result{}, r.Update(ctx, obj)
    }
    return ctrl.Result{}, nil
}

// Add finalizer if not present
if !controllerutil.ContainsFinalizer(obj, myFinalizer) {
    controllerutil.AddFinalizer(obj, myFinalizer)
    return ctrl.Result{}, r.Update(ctx, obj)
}
```

### 3. Update Status Separately

Always update status using the status subresource:

```go
// Update spec
if err := r.Update(ctx, obj); err != nil {
    return ctrl.Result{}, err
}

// Update status
if err := r.Status().Update(ctx, obj); err != nil {
    return ctrl.Result{}, err
}
```

### 4. Use Predicates to Filter Events

Reduce unnecessary reconciliations:

```go
err := ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}, builder.WithPredicates(
        predicate.GenerationChangedPredicate{},
    )).
    Complete(&MyResourceReconciler{})
```

### 5. Enable Leader Election for HA

Run multiple replicas with leader election:

```go
mgr, err := ctrl.NewManager(cfg, ctrl.Options{
    LeaderElection: true,
    LeaderElectionID: "my-controller-lock",
})
```

## Testing

### Unit Testing with Fake Client

```go
import "sigs.k8s.io/controller-runtime/pkg/client/fake"

func TestReconcile(t *testing.T) {
    scheme := runtime.NewScheme()
    _ = corev1.AddToScheme(scheme)
    
    fakeClient := fake.NewClientBuilder().
        WithScheme(scheme).
        WithObjects(&pod).
        Build()
    
    reconciler := &MyReconciler{
        Client: fakeClient,
    }
    
    result, err := reconciler.Reconcile(ctx, req)
    // Assert result and err
}
```

### Integration Testing with envtest

```go
import "sigs.k8s.io/controller-runtime/pkg/envtest"

func TestControllerIntegration(t *testing.T) {
    testEnv := &envtest.Environment{
        CRDDirectoryPaths: []string{"./config/crd"},
    }
    
    cfg, err := testEnv.Start()
    defer testEnv.Stop()
    
    // Create manager and controller
    // Run tests
}
```

## Troubleshooting

### Common Issues

1. **Cache not synced**: Increase `CacheSyncTimeout`
2. **High memory usage**: Use `OnlyMetadata` watches
3. **Slow reconciliation**: Increase `MaxConcurrentReconciles`
4. **Missed events**: Check predicates aren't too restrictive
5. **Conflicts on update**: Use `Patch` instead of `Update`

### Debugging

Enable verbose logging:

```go
import "sigs.k8s.io/controller-runtime/pkg/log/zap"

ctrl.SetLogger(zap.New(zap.UseDevMode(true)))
```

## Resources

### Official Documentation

- [Kubebuilder Book](https://book.kubebuilder.io/)
- [Controller-Runtime GoDoc](https://pkg.go.dev/sigs.k8s.io/controller-runtime)
- [GitHub Repository](https://github.com/kubernetes-sigs/controller-runtime)

### Examples

- [Built-in Resources Example](../examples/builtins/)
- [CRD Example](../examples/crd/)
- [Typed Controller Example](../examples/typed/)

### Community

- [Kubernetes Slack #controller-runtime](https://kubernetes.slack.com/archives/C02MRBMN00Z)
- [Kubebuilder Google Group](https://groups.google.com/forum/#!forum/kubebuilder)

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines on contributing to controller-runtime.

## License

Controller-runtime is licensed under the Apache License 2.0. See [LICENSE](../../LICENSE) for details.
