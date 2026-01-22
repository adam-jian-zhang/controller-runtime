---
title: "Reconcile"
weight: 3
---


## Overview

The `pkg/reconcile` package defines the core Reconciler interface and types that implement the business logic of Kubernetes controllers. Reconcilers are where you implement the actual control loop logic.

## Package Location

```
pkg/reconcile/
├── reconcile.go        # Reconciler interface and types
└── doc.go              # Package documentation
```

## Core Concepts

### Reconciliation Pattern

Reconciliation is the process of making the actual state of a system match the desired state:

<div class="mermaid-diagram">
<svg aria-roledescription="flowchart-v2" role="graphics-document document" viewBox="-8 -8 790.1484375 103" style="max-width: 790.148px; background-color: transparent;" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" width="100%" id="my-svg"><style>#my-svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}#my-svg .error-icon{fill:#552222;}#my-svg .error-text{fill:#552222;stroke:#552222;}#my-svg .edge-thickness-normal{stroke-width:2px;}#my-svg .edge-thickness-thick{stroke-width:3.5px;}#my-svg .edge-pattern-solid{stroke-dasharray:0;}#my-svg .edge-pattern-dashed{stroke-dasharray:3;}#my-svg .edge-pattern-dotted{stroke-dasharray:2;}#my-svg .marker{fill:#333333;stroke:#333333;}#my-svg .marker.cross{stroke:#333333;}#my-svg svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#my-svg .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#333;}#my-svg .cluster-label text{fill:#333;}#my-svg .cluster-label span,#my-svg p{color:#333;}#my-svg .label text,#my-svg span,#my-svg p{fill:#333;color:#333;}#my-svg .node rect,#my-svg .node circle,#my-svg .node ellipse,#my-svg .node polygon,#my-svg .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#my-svg .flowchart-label text{text-anchor:middle;}#my-svg .node .label{text-align:center;}#my-svg .node.clickable{cursor:pointer;}#my-svg .arrowheadPath{fill:#333333;}#my-svg .edgePath .path{stroke:#333333;stroke-width:2.0px;}#my-svg .flowchart-link{stroke:#333333;fill:none;}#my-svg .edgeLabel{background-color:#e8e8e8;text-align:center;}#my-svg .edgeLabel rect{opacity:0.5;background-color:#e8e8e8;fill:#e8e8e8;}#my-svg .labelBkg{background-color:rgba(232, 232, 232, 0.5);}#my-svg .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#my-svg .cluster text{fill:#333;}#my-svg .cluster span,#my-svg p{color:#333;}#my-svg div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(80, 100%, 96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#my-svg .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#333;}#my-svg :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}</style><g><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="6" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointEnd"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 0 L 10 5 L 0 10 z"/></marker><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="4.5" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointStart"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 5 L 10 10 L 10 0 z"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="11" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleEnd"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="-1" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleStart"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="12" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossEnd"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="-1" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossStart"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><g class="root"><g class="clusters"/><g class="edgePaths"><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-DesiredState LE-Reconciler" id="L-DesiredState-Reconciler-0" d="M110.7734375,47.25L117.83268229166667,47.25C124.89192708333333,47.25,139.01041666666666,47.25,152.24557291666667,47.25C165.48072916666666,47.25,177.83255208333333,47.25,184.00846354166666,47.25L190.184375,47.25"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-ActualState LE-Reconciler" id="L-ActualState-Reconciler-0" d="M671.2421875,67.7765685673411L667.0755208333334,69.43880713945092C662.9088541666666,71.10104571156073,654.5755208333334,74.42552285578036,631.3665364583334,76.08776142789019C608.1575520833334,77.75,570.0729166666666,77.75,523.033203125,77.75C475.9934895833333,77.75,419.9986979166667,77.75,379.73717551513005,74.72427008833002C339.4756531135934,71.69854017666005,314.94739997718676,65.6470803533201,302.6832734089835,62.62135044165012L290.4191468407802,59.595620529980145"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Reconciler LE-Actions" id="L-Reconciler-Actions-0" d="M285.2734375,36.17389724469161L298.3951822916667,32.93658103724301C311.5169270833333,29.699264829794405,337.7604166666667,23.2246324148972,363.1205729166666,19.9873162074486C388.48072916666666,16.75,412.9575520833334,16.75,425.1959635416667,16.75L437.434375,16.75"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Actions LE-ActualState" id="L-Actions-ActualState-0" d="M621.2421875,16.75L625.4088541666666,16.75C629.5755208333334,16.75,637.9088541666666,16.75,645.4217327678656,18.08492861152809C652.9346113690644,19.41985722305618,659.627035238129,22.089714446112357,662.9732471726612,23.42464305764045L666.3194591071934,24.759571669168537"/></g><g class="edgeLabels"><g transform="translate(153.12890625, 47.25)" class="edgeLabel"><g transform="translate(-17.35546875, -9.25)" class="label"><foreignObject height="18.5" width="34.7109375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Read</span></div></foreignObject></g></g><g transform="translate(531.98828125, 77.75)" class="edgeLabel"><g transform="translate(-17.35546875, -9.25)" class="label"><foreignObject height="18.5" width="34.7109375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Read</span></div></foreignObject></g></g><g transform="translate(364.00390625, 16.75)" class="edgeLabel"><g transform="translate(-53.73046875, -9.25)" class="label"><foreignObject height="18.5" width="107.4609375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Compare &amp; Act</span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g></g><g class="nodes"><g transform="translate(55.38671875, 47.25)" id="flowchart-DesiredState-0" class="node default default flowchart-label"><rect height="52" width="110.7734375" y="-26" x="-55.38671875" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-47.88671875, -18.5)" style="" class="label"><rect/><foreignObject height="37" width="95.7734375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Desired State<br />in API Server</span></div></foreignObject></g></g><g transform="translate(722.6953125, 47.25)" id="flowchart-ActualState-1" class="node default default flowchart-label"><rect height="52" width="102.90625" y="-26" x="-51.453125" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-43.953125, -18.5)" style="" class="label"><rect/><foreignObject height="37" width="87.90625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Actual State<br />in Cluster</span></div></foreignObject></g></g><g transform="translate(240.37890625, 47.25)" id="flowchart-Reconciler-2" class="node default default flowchart-label"><rect height="33.5" width="89.7890625" y="-16.75" x="-44.89453125" ry="0" rx="0" style="fill:#e1f5ff;" class="basic label-container"/><g transform="translate(-37.39453125, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="74.7890625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Reconciler</span></div></foreignObject></g></g><g transform="translate(531.98828125, 16.75)" id="flowchart-Actions-8" class="node default default flowchart-label"><rect height="33.5" width="178.5078125" y="-16.75" x="-89.25390625" ry="0" rx="0" style="fill:#fff4e1;" class="basic label-container"/><g transform="translate(-81.75390625, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="163.5078125"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Create/Update/Delete</span></div></foreignObject></g></g></g></g></g></svg>
</div>

### Level-Based vs Edge-Based

Controller-runtime uses **level-based** reconciliation:

<div class="mermaid-diagram">
<svg aria-roledescription="flowchart-v2" role="graphics-document document" viewBox="-7.5 -8 1366.7421875 286.5" style="max-width: 1366.74px; background-color: transparent;" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" width="100%" id="my-svg"><style>#my-svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}#my-svg .error-icon{fill:#552222;}#my-svg .error-text{fill:#552222;stroke:#552222;}#my-svg .edge-thickness-normal{stroke-width:2px;}#my-svg .edge-thickness-thick{stroke-width:3.5px;}#my-svg .edge-pattern-solid{stroke-dasharray:0;}#my-svg .edge-pattern-dashed{stroke-dasharray:3;}#my-svg .edge-pattern-dotted{stroke-dasharray:2;}#my-svg .marker{fill:#333333;stroke:#333333;}#my-svg .marker.cross{stroke:#333333;}#my-svg svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#my-svg .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#333;}#my-svg .cluster-label text{fill:#333;}#my-svg .cluster-label span,#my-svg p{color:#333;}#my-svg .label text,#my-svg span,#my-svg p{fill:#333;color:#333;}#my-svg .node rect,#my-svg .node circle,#my-svg .node ellipse,#my-svg .node polygon,#my-svg .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#my-svg .flowchart-label text{text-anchor:middle;}#my-svg .node .label{text-align:center;}#my-svg .node.clickable{cursor:pointer;}#my-svg .arrowheadPath{fill:#333333;}#my-svg .edgePath .path{stroke:#333333;stroke-width:2.0px;}#my-svg .flowchart-link{stroke:#333333;fill:none;}#my-svg .edgeLabel{background-color:#e8e8e8;text-align:center;}#my-svg .edgeLabel rect{opacity:0.5;background-color:#e8e8e8;fill:#e8e8e8;}#my-svg .labelBkg{background-color:rgba(232, 232, 232, 0.5);}#my-svg .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#my-svg .cluster text{fill:#333;}#my-svg .cluster span,#my-svg p{color:#333;}#my-svg div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(80, 100%, 96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#my-svg .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#333;}#my-svg :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}</style><g><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="6" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointEnd"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 0 L 10 5 L 0 10 z"/></marker><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="4.5" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointStart"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 5 L 10 10 L 10 0 z"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="11" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleEnd"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="-1" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleStart"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="12" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossEnd"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="-1" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossStart"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><g class="root"><g class="clusters"/><g class="edgePaths"/><g class="edgeLabels"/><g class="nodes"><g transform="translate(-7.5, 75.5)" class="root"><g class="clusters"><g id="subGraph1" class="cluster default flowchart-label"><rect height="103.5" width="864.265625" y="8" x="8" ry="0" rx="0" style=""/><g transform="translate(320.2890625, 8)" class="cluster-label"><foreignObject height="18.5" width="239.6875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Level-Based (Controller-Runtime)</span></div></foreignObject></g></g></g><g class="edgePaths"><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-L1 LE-L2" id="L-L1-L2-0" d="M177.984375,59.75L182.15104166666666,59.75C186.31770833333334,59.75,194.65104166666666,59.75,202.10104166666667,59.75C209.5510416666667,59.75,216.11770833333333,59.75,219.40104166666666,59.75L222.684375,59.75"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-L2 LE-L3" id="L-L2-L3-0" d="M379.4140625,59.75L383.5807291666667,59.75C387.7473958333333,59.75,396.0807291666667,59.75,403.5307291666666,59.75C410.98072916666666,59.75,417.5473958333334,59.75,420.8307291666667,59.75L424.1140625,59.75"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-L3 LE-L4" id="L-L3-L4-0" d="M602.75,59.75L606.9166666666666,59.75C611.0833333333334,59.75,619.4166666666666,59.75,626.8666666666667,59.75C634.3166666666667,59.75,640.8833333333333,59.75,644.1666666666666,59.75L647.45,59.75"/></g><g class="edgeLabels"><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g></g><g class="nodes"><g transform="translate(303.69921875, 59.75)" id="flowchart-L2-7" class="node default default flowchart-label"><rect height="33.5" width="151.4296875" y="-16.75" x="-75.71484375" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-68.21484375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="136.4296875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Read Current State</span></div></foreignObject></g></g><g transform="translate(105.4921875, 59.75)" id="flowchart-L1-6" class="node default default flowchart-label"><rect height="33.5" width="144.984375" y="-16.75" x="-72.4921875" ry="0" rx="0" style="fill:#e1f5ff;" class="basic label-container"/><g transform="translate(-64.9921875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="129.984375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Reconcile Request</span></div></foreignObject></g></g><g transform="translate(516.08203125, 59.75)" id="flowchart-L3-9" class="node default default flowchart-label"><rect height="33.5" width="173.3359375" y="-16.75" x="-86.66796875" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-79.16796875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="158.3359375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Compare with Desired</span></div></foreignObject></g></g><g transform="translate(750.0078125, 59.75)" id="flowchart-L4-11" class="node default default flowchart-label"><rect height="33.5" width="194.515625" y="-16.75" x="-97.2578125" ry="0" rx="0" style="fill:#fff4e1;" class="basic label-container"/><g transform="translate(-89.7578125, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="179.515625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Take Actions to Converge</span></div></foreignObject></g></g></g></g><g transform="translate(906.765625, -8)" class="root"><g class="clusters"><g id="subGraph0" class="cluster default flowchart-label"><rect height="270.5" width="436.4765625" y="8" x="8" ry="0" rx="0" style=""/><g transform="translate(144.87890625, 8)" class="cluster-label"><foreignObject height="18.5" width="162.71875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Edge-Based (Not Used)</span></div></foreignObject></g></g></g><g class="edgePaths"><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-E1 LE-E2" id="L-E1-E2-0" d="M188.15625,59.75L192.63020833333334,59.75C197.10416666666666,59.75,206.05208333333334,59.75,214.11666666666667,59.75C222.18125,59.75,229.36249999999998,59.75,232.953125,59.75L236.54375,59.75"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-E3 LE-E4" id="L-E3-E4-0" d="M190,143.25L194.16666666666666,143.25C198.33333333333334,143.25,206.66666666666666,143.25,214.11666666666667,143.25C221.5666666666667,143.25,228.13333333333333,143.25,231.41666666666666,143.25L234.7,143.25"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-E5 LE-E6" id="L-E5-E6-0" d="M187.6875,226.75L192.23958333333334,226.75C196.79166666666666,226.75,205.89583333333334,226.75,214.11666666666667,226.75C222.3375,226.75,229.67499999999998,226.75,233.34375,226.75L237.0125,226.75"/></g><g class="edgeLabels"><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g></g><g class="nodes"><g transform="translate(329.73828125, 59.75)" id="flowchart-E2-1" class="node default default flowchart-label"><rect height="33.5" width="175.7890625" y="-16.75" x="-87.89453125" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-80.39453125, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="160.7890625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Action: Create Service</span></div></foreignObject></g></g><g transform="translate(111.5, 59.75)" id="flowchart-E1-0" class="node default default flowchart-label"><rect height="33.5" width="153.3125" y="-16.75" x="-76.65625" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-69.15625, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="138.3125"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Event: Pod Created</span></div></foreignObject></g></g><g transform="translate(111.5, 143.25)" id="flowchart-E3-2" class="node default default flowchart-label"><rect height="33.5" width="157" y="-16.75" x="-78.5" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-71, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="142"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Event: Pod Updated</span></div></foreignObject></g></g><g transform="translate(329.73828125, 143.25)" id="flowchart-E4-3" class="node default default flowchart-label"><rect height="33.5" width="179.4765625" y="-16.75" x="-89.73828125" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-82.23828125, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="164.4765625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Action: Update Service</span></div></foreignObject></g></g><g transform="translate(111.5, 226.75)" id="flowchart-E5-4" class="node default default flowchart-label"><rect height="33.5" width="152.375" y="-16.75" x="-76.1875" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-68.6875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="137.375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Event: Pod Deleted</span></div></foreignObject></g></g><g transform="translate(329.73828125, 226.75)" id="flowchart-E6-5" class="node default default flowchart-label"><rect height="33.5" width="174.8515625" y="-16.75" x="-87.42578125" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-79.92578125, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="159.8515625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Action: Delete Service</span></div></foreignObject></g></g></g></g></g></g></g></svg>
</div>

**Benefits of Level-Based**:
- Resilient to missed events
- Self-healing
- Idempotent operations
- Easier to reason about

## Reconciler Interface

### Basic Reconciler

```go
type Reconciler interface {
    Reconcile(context.Context, Request) (Result, error)
}
```

### Typed Reconciler

```go
type TypedReconciler[request comparable] interface {
    Reconcile(context.Context, request) (Result, error)
}
```

The typed reconciler allows custom request types for advanced use cases.

## Request Type

The Request contains the minimal information needed to identify an object:

```go
type Request struct {
    types.NamespacedName
}

// NamespacedName contains:
// - Namespace string
// - Name string
```

**Important**: The Request does NOT contain:
- The actual object
- The event type (Create/Update/Delete)
- The old object state

This is intentional - reconcilers should read the current state from the API server.

## Result Type

The Result tells the controller what to do after reconciliation:

```go
type Result struct {
    // Requeue tells the controller to requeue with rate limiting
    // Deprecated: Use RequeueAfter instead
    Requeue bool

    // RequeueAfter requeues the request after the specified duration
    RequeueAfter time.Duration

    // Priority sets the priority for the requeued item
    // Only used with priority queues
    Priority *int
}
```

### Result Patterns

<div class="mermaid-diagram">
<svg aria-roledescription="flowchart-v2" role="graphics-document document" viewBox="-8 -8 1102.75 299.546875" style="max-width: 1102.75px; background-color: transparent;" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" width="100%" id="my-svg"><style>#my-svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}#my-svg .error-icon{fill:#552222;}#my-svg .error-text{fill:#552222;stroke:#552222;}#my-svg .edge-thickness-normal{stroke-width:2px;}#my-svg .edge-thickness-thick{stroke-width:3.5px;}#my-svg .edge-pattern-solid{stroke-dasharray:0;}#my-svg .edge-pattern-dashed{stroke-dasharray:3;}#my-svg .edge-pattern-dotted{stroke-dasharray:2;}#my-svg .marker{fill:#333333;stroke:#333333;}#my-svg .marker.cross{stroke:#333333;}#my-svg svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#my-svg .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#333;}#my-svg .cluster-label text{fill:#333;}#my-svg .cluster-label span,#my-svg p{color:#333;}#my-svg .label text,#my-svg span,#my-svg p{fill:#333;color:#333;}#my-svg .node rect,#my-svg .node circle,#my-svg .node ellipse,#my-svg .node polygon,#my-svg .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#my-svg .flowchart-label text{text-anchor:middle;}#my-svg .node .label{text-align:center;}#my-svg .node.clickable{cursor:pointer;}#my-svg .arrowheadPath{fill:#333333;}#my-svg .edgePath .path{stroke:#333333;stroke-width:2.0px;}#my-svg .flowchart-link{stroke:#333333;fill:none;}#my-svg .edgeLabel{background-color:#e8e8e8;text-align:center;}#my-svg .edgeLabel rect{opacity:0.5;background-color:#e8e8e8;fill:#e8e8e8;}#my-svg .labelBkg{background-color:rgba(232, 232, 232, 0.5);}#my-svg .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#my-svg .cluster text{fill:#333;}#my-svg .cluster span,#my-svg p{color:#333;}#my-svg div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(80, 100%, 96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#my-svg .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#333;}#my-svg :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}</style><g><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="6" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointEnd"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 0 L 10 5 L 0 10 z"/></marker><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="4.5" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointStart"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 5 L 10 10 L 10 0 z"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="11" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleEnd"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="-1" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleStart"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="12" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossEnd"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="-1" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossStart"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><g class="root"><g class="clusters"/><g class="edgePaths"><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Reconcile LE-Success" id="L-Reconcile-Success-0" d="M538.9296875,33.5L538.9296875,37.666666666666664C538.9296875,41.833333333333336,538.9296875,50.166666666666664,538.9957039004745,57.700169757536564C539.0617203009491,65.23367284840646,539.1937531018983,71.9673456968129,539.2597695023728,75.33418212101613L539.3257859028474,78.70101854521936"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Success LE-Done" id="L-Success-Done-0" d="M497.8751200419868,140.49230754198678L427.49944899332235,153.04306878498898C357.12377794465783,165.59383002799117,216.37243584732892,190.69535251399557,145.99676479866446,208.0711137569978C75.62109375,225.446875,75.62109375,235.09687499999998,75.62109375,239.921875L75.62109375,244.746875"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Success LE-RateLimited" id="L-Success-RateLimited-0" d="M502.9668745042246,145.58406200422462L468.6709631285205,157.28619750352053C434.37505175281643,168.9883330028164,365.7832290014082,192.39260400140822,331.48731762570407,208.91973950070408C297.19140625,225.446875,297.19140625,235.09687499999998,297.19140625,239.921875L297.19140625,244.746875"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Success LE-Delayed" id="L-Success-Delayed-0" d="M539.4296875,182.046875L539.3463541666666,187.671875C539.2630208333334,193.296875,539.0963541666666,204.546875,539.0130208333334,214.99687500000002C538.9296875,225.446875,538.9296875,235.09687499999998,538.9296875,239.921875L538.9296875,244.746875"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Success LE-Error" id="L-Success-Error-0" d="M575.4815405966463,145.99502190335372L607.9631327888719,157.6286640861281C640.4447249810975,169.26230626890248,705.4079093655488,192.52959063445124,737.8895015577745,208.98823281722562C770.37109375,225.446875,770.37109375,235.09687499999998,770.37109375,239.921875L770.37109375,244.746875"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Success LE-Terminal" id="L-Success-Terminal-0" d="M580.9034299215471,140.5731325784529L650.1506447262892,153.1104229820441C719.3978595310314,165.64771338563529,857.8922891405158,190.72229419281766,927.1395039452578,208.08458459640883C996.38671875,225.446875,996.38671875,235.09687499999998,996.38671875,239.921875L996.38671875,244.746875"/></g><g class="edgeLabels"><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g transform="translate(75.62109375, 215.796875)" class="edgeLabel"><g transform="translate(-42.0703125, -9.25)" class="label"><foreignObject height="18.5" width="84.140625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Result{}, nil</span></div></foreignObject></g></g><g transform="translate(297.19140625, 215.796875)" class="edgeLabel"><g transform="translate(-93.0546875, -9.25)" class="label"><foreignObject height="18.5" width="186.109375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Result{Requeue: true}, nil</span></div></foreignObject></g></g><g transform="translate(538.9296875, 215.796875)" class="edgeLabel"><g transform="translate(-107.1953125, -9.25)" class="label"><foreignObject height="18.5" width="214.390625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Result{RequeueAfter: 5m}, nil</span></div></foreignObject></g></g><g transform="translate(770.37109375, 215.796875)" class="edgeLabel"><g transform="translate(-51.04296875, -9.25)" class="label"><foreignObject height="18.5" width="102.0859375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Result{}, error</span></div></foreignObject></g></g><g transform="translate(996.38671875, 215.796875)" class="edgeLabel"><g transform="translate(-81.796875, -9.25)" class="label"><foreignObject height="18.5" width="163.59375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel">Result{}, TerminalError</span></div></foreignObject></g></g></g><g class="nodes"><g transform="translate(538.9296875, 16.75)" id="flowchart-Reconcile-0" class="node default default flowchart-label"><rect height="33.5" width="83.5703125" y="-16.75" x="-41.78515625" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-34.28515625, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="68.5703125"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Reconcile</span></div></foreignObject></g></g><g transform="translate(538.9296875, 132.5234375)" id="flowchart-Success-2" class="node default default flowchart-label"><polygon style="" transform="translate(-49.0234375,49.0234375)" class="label-container" points="49.0234375,0 98.046875,-49.0234375 49.0234375,-98.046875 0,-49.0234375"/><g transform="translate(-24.7734375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="49.546875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Result?</span></div></foreignObject></g></g><g transform="translate(75.62109375, 266.796875)" id="flowchart-Done-4" class="node default default flowchart-label"><rect height="33.5" width="151.2421875" y="-16.75" x="-75.62109375" ry="0" rx="0" style="fill:#c8e6c9;" class="basic label-container"/><g transform="translate(-68.12109375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="136.2421875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Done - No Requeue</span></div></foreignObject></g></g><g transform="translate(297.19140625, 266.796875)" id="flowchart-RateLimited-6" class="node default default flowchart-label"><rect height="33.5" width="191.8984375" y="-16.75" x="-95.94921875" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-88.44921875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="176.8984375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Requeue with Rate Limit</span></div></foreignObject></g></g><g transform="translate(538.9296875, 266.796875)" id="flowchart-Delayed-8" class="node default default flowchart-label"><rect height="33.5" width="191.578125" y="-16.75" x="-95.7890625" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-88.2890625, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="176.578125"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Requeue after 5 minutes</span></div></foreignObject></g></g><g transform="translate(770.37109375, 266.796875)" id="flowchart-Error-10" class="node default default flowchart-label"><rect height="33.5" width="171.3046875" y="-16.75" x="-85.65234375" ry="0" rx="0" style="fill:#ffcdd2;" class="basic label-container"/><g transform="translate(-78.15234375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="156.3046875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Requeue with Backoff</span></div></foreignObject></g></g><g transform="translate(996.38671875, 266.796875)" id="flowchart-Terminal-12" class="node default default flowchart-label"><rect height="33.5" width="180.7265625" y="-16.75" x="-90.36328125" ry="0" rx="0" style="fill:#ffcdd2;" class="basic label-container"/><g transform="translate(-82.86328125, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="165.7265625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">No Requeue - Log Error</span></div></foreignObject></g></g></g></g></g></svg>
</div>

## Implementing a Reconciler

### Basic Structure

```go
import (
    "context"
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/client"
    "sigs.k8s.io/controller-runtime/pkg/log"
)

type MyReconciler struct {
    client.Client
    Scheme *runtime.Scheme
}

func (r *MyReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := log.FromContext(ctx)
    
    // 1. Fetch the resource
    var obj MyResource
    if err := r.Get(ctx, req.NamespacedName, &obj); err != nil {
        if errors.IsNotFound(err) {
            // Object not found, could have been deleted
            return ctrl.Result{}, nil
        }
        // Error reading the object
        return ctrl.Result{}, err
    }
    
    // 2. Handle deletion (finalizers)
    if !obj.DeletionTimestamp.IsZero() {
        return r.handleDeletion(ctx, &obj)
    }
    
    // 3. Reconcile logic
    if err := r.reconcileResource(ctx, &obj); err != nil {
        return ctrl.Result{}, err
    }
    
    // 4. Update status
    if err := r.Status().Update(ctx, &obj); err != nil {
        return ctrl.Result{}, err
    }
    
    return ctrl.Result{}, nil
}
```

## Reconciliation Patterns

### 1. Read-Compare-Act Pattern

```go
func (r *MyReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // Read current state
    var desired MyResource
    if err := r.Get(ctx, req.NamespacedName, &desired); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    
    var actual corev1.Pod
    err := r.Get(ctx, types.NamespacedName{
        Name: desired.Name,
        Namespace: desired.Namespace,
    }, &actual)
    
    if errors.IsNotFound(err) {
        // Create the resource
        return ctrl.Result{}, r.createPod(ctx, &desired)
    } else if err != nil {
        return ctrl.Result{}, err
    }
    
    // Compare and update if needed
    if !reflect.DeepEqual(actual.Spec, desired.Spec) {
        actual.Spec = desired.Spec
        return ctrl.Result{}, r.Update(ctx, &actual)
    }
    
    return ctrl.Result{}, nil
}
```

### 2. Finalizer Pattern

```go
const myFinalizer = "myresource.example.com/finalizer"

func (r *MyReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    var obj MyResource
    if err := r.Get(ctx, req.NamespacedName, &obj); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    
    // Examine DeletionTimestamp to determine if object is under deletion
    if obj.DeletionTimestamp.IsZero() {
        // Object is not being deleted, add finalizer if not present
        if !controllerutil.ContainsFinalizer(&obj, myFinalizer) {
            controllerutil.AddFinalizer(&obj, myFinalizer)
            if err := r.Update(ctx, &obj); err != nil {
                return ctrl.Result{}, err
            }
        }
    } else {
        // Object is being deleted
        if controllerutil.ContainsFinalizer(&obj, myFinalizer) {
            // Perform cleanup
            if err := r.deleteExternalResources(ctx, &obj); err != nil {
                // If cleanup fails, return error to retry
                return ctrl.Result{}, err
            }
            
            // Remove finalizer to allow deletion
            controllerutil.RemoveFinalizer(&obj, myFinalizer)
            if err := r.Update(ctx, &obj); err != nil {
                return ctrl.Result{}, err
            }
        }
        
        // Stop reconciliation as the object is being deleted
        return ctrl.Result{}, nil
    }
    
    // Normal reconciliation logic
    return r.reconcileNormal(ctx, &obj)
}
```

### 3. Status Update Pattern

```go
func (r *MyReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    var obj MyResource
    if err := r.Get(ctx, req.NamespacedName, &obj); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    
    // Save original status
    originalStatus := obj.Status.DeepCopy()
    
    // Reconcile and update status fields
    if err := r.reconcile(ctx, &obj); err != nil {
        obj.Status.Conditions = append(obj.Status.Conditions, metav1.Condition{
            Type:    "Ready",
            Status:  metav1.ConditionFalse,
            Reason:  "ReconciliationFailed",
            Message: err.Error(),
        })
        // Update status even on error
        if statusErr := r.Status().Update(ctx, &obj); statusErr != nil {
            return ctrl.Result{}, utilerrors.NewAggregate([]error{err, statusErr})
        }
        return ctrl.Result{}, err
    }
    
    // Update status if changed
    if !reflect.DeepEqual(originalStatus, &obj.Status) {
        if err := r.Status().Update(ctx, &obj); err != nil {
            return ctrl.Result{}, err
        }
    }
    
    return ctrl.Result{}, nil
}
```

### 4. Periodic Reconciliation Pattern

```go
func (r *MyReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    var obj MyResource
    if err := r.Get(ctx, req.NamespacedName, &obj); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    
    // Perform reconciliation
    if err := r.reconcile(ctx, &obj); err != nil {
        return ctrl.Result{}, err
    }
    
    // Requeue after 5 minutes for periodic reconciliation
    return ctrl.Result{RequeueAfter: 5 * time.Minute}, nil
}
```

### 5. Conditional Requeue Pattern

```go
func (r *MyReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    var obj MyResource
    if err := r.Get(ctx, req.NamespacedName, &obj); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    
    // Check if resource is ready
    if !isReady(&obj) {
        // Not ready yet, check again in 30 seconds
        return ctrl.Result{RequeueAfter: 30 * time.Second}, nil
    }
    
    // Resource is ready, perform reconciliation
    return r.reconcile(ctx, &obj)
}
```

## Error Handling

### Error Types

<div class="mermaid-diagram">
<svg aria-roledescription="flowchart-v2" role="graphics-document document" viewBox="-8 -8 602.171875 216.5" style="max-width: 602.172px; background-color: transparent;" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" width="100%" id="my-svg"><style>#my-svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}#my-svg .error-icon{fill:#552222;}#my-svg .error-text{fill:#552222;stroke:#552222;}#my-svg .edge-thickness-normal{stroke-width:2px;}#my-svg .edge-thickness-thick{stroke-width:3.5px;}#my-svg .edge-pattern-solid{stroke-dasharray:0;}#my-svg .edge-pattern-dashed{stroke-dasharray:3;}#my-svg .edge-pattern-dotted{stroke-dasharray:2;}#my-svg .marker{fill:#333333;stroke:#333333;}#my-svg .marker.cross{stroke:#333333;}#my-svg svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#my-svg .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#333;}#my-svg .cluster-label text{fill:#333;}#my-svg .cluster-label span,#my-svg p{color:#333;}#my-svg .label text,#my-svg span,#my-svg p{fill:#333;color:#333;}#my-svg .node rect,#my-svg .node circle,#my-svg .node ellipse,#my-svg .node polygon,#my-svg .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#my-svg .flowchart-label text{text-anchor:middle;}#my-svg .node .label{text-align:center;}#my-svg .node.clickable{cursor:pointer;}#my-svg .arrowheadPath{fill:#333333;}#my-svg .edgePath .path{stroke:#333333;stroke-width:2.0px;}#my-svg .flowchart-link{stroke:#333333;fill:none;}#my-svg .edgeLabel{background-color:#e8e8e8;text-align:center;}#my-svg .edgeLabel rect{opacity:0.5;background-color:#e8e8e8;fill:#e8e8e8;}#my-svg .labelBkg{background-color:rgba(232, 232, 232, 0.5);}#my-svg .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#my-svg .cluster text{fill:#333;}#my-svg .cluster span,#my-svg p{color:#333;}#my-svg div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(80, 100%, 96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#my-svg .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#333;}#my-svg :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}</style><g><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="6" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointEnd"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 0 L 10 5 L 0 10 z"/></marker><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="4.5" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointStart"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 5 L 10 10 L 10 0 z"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="11" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleEnd"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="-1" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleStart"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="12" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossEnd"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="-1" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossStart"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><g class="root"><g class="clusters"/><g class="edgePaths"><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Error LE-Transient" id="L-Error-Transient-0" d="M196.390625,33.04012723982957L175.984375,37.28343936652465C155.578125,41.52675149321971,114.765625,50.01337574660986,94.359375,57.540021206638265C73.953125,65.06666666666666,73.953125,71.63333333333334,73.953125,74.91666666666667L73.953125,78.2"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Error LE-Terminal" id="L-Error-Terminal-0" d="M274.73046875,33.5L274.73046875,37.666666666666664C274.73046875,41.833333333333336,274.73046875,50.166666666666664,274.73046875,57.61666666666667C274.73046875,65.06666666666666,274.73046875,71.63333333333334,274.73046875,74.91666666666667L274.73046875,78.2"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Error LE-NotFound" id="L-Error-NotFound-0" d="M353.0703125,31.67559895183429L376.5358072916667,36.1463324598619C400.0013020833333,40.61706596788952,446.9322916666667,49.55853298394476,470.3977864583333,57.31259982530571C493.86328125,65.06666666666666,493.86328125,71.63333333333334,493.86328125,74.91666666666667L493.86328125,78.2"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Transient LE-Retry" id="L-Transient-Retry-0" d="M73.953125,117L73.953125,121.16666666666667C73.953125,125.33333333333333,73.953125,133.66666666666666,73.953125,141.11666666666667C73.953125,148.56666666666666,73.953125,155.13333333333333,73.953125,158.41666666666666L73.953125,161.7"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Terminal LE-NoRetry" id="L-Terminal-NoRetry-0" d="M274.73046875,117L274.73046875,121.16666666666667C274.73046875,125.33333333333333,274.73046875,133.66666666666666,274.73046875,141.11666666666667C274.73046875,148.56666666666666,274.73046875,155.13333333333333,274.73046875,158.41666666666666L274.73046875,161.7"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-NotFound LE-Ignore" id="L-NotFound-Ignore-0" d="M493.86328125,117L493.86328125,121.16666666666667C493.86328125,125.33333333333333,493.86328125,133.66666666666666,493.86328125,141.11666666666667C493.86328125,148.56666666666666,493.86328125,155.13333333333333,493.86328125,158.41666666666666L493.86328125,161.7"/></g><g class="edgeLabels"><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g></g><g class="nodes"><g transform="translate(274.73046875, 16.75)" id="flowchart-Error-0" class="node default default flowchart-label"><rect height="33.5" width="156.6796875" y="-16.75" x="-78.33984375" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-70.83984375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="141.6796875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Reconciliation Error</span></div></foreignObject></g></g><g transform="translate(73.953125, 100.25)" id="flowchart-Transient-2" class="node default default flowchart-label"><rect height="33.5" width="121.3828125" y="-16.75" x="-60.69140625" ry="0" rx="0" style="fill:#fff4e1;" class="basic label-container"/><g transform="translate(-53.19140625, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="106.3828125"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Transient Error</span></div></foreignObject></g></g><g transform="translate(274.73046875, 100.25)" id="flowchart-Terminal-4" class="node default default flowchart-label"><rect height="33.5" width="117.5859375" y="-16.75" x="-58.79296875" ry="0" rx="0" style="fill:#ffcdd2;" class="basic label-container"/><g transform="translate(-51.29296875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="102.5859375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Terminal Error</span></div></foreignObject></g></g><g transform="translate(493.86328125, 100.25)" id="flowchart-NotFound-6" class="node default default flowchart-label"><rect height="33.5" width="128.9765625" y="-16.75" x="-64.48828125" ry="0" rx="0" style="fill:#e0e0e0;" class="basic label-container"/><g transform="translate(-56.98828125, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="113.9765625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Not Found Error</span></div></foreignObject></g></g><g transform="translate(73.953125, 183.75)" id="flowchart-Retry-8" class="node default default flowchart-label"><rect height="33.5" width="147.90625" y="-16.75" x="-73.953125" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-66.453125, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="132.90625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Retry with Backoff</span></div></foreignObject></g></g><g transform="translate(274.73046875, 183.75)" id="flowchart-NoRetry-10" class="node default default flowchart-label"><rect height="33.5" width="153.6484375" y="-16.75" x="-76.82421875" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-69.32421875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="138.6484375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">No Retry - Log Only</span></div></foreignObject></g></g><g transform="translate(493.86328125, 183.75)" id="flowchart-Ignore-12" class="node default default flowchart-label"><rect height="33.5" width="184.6171875" y="-16.75" x="-92.30859375" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-84.80859375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="169.6171875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Ignore - Object Deleted</span></div></foreignObject></g></g></g></g></g></svg>
</div>

### Handling Transient Errors

```go
func (r *MyReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // Transient error - will be retried with exponential backoff
    if err := r.doSomething(); err != nil {
        return ctrl.Result{}, err
    }
    
    return ctrl.Result{}, nil
}
```

### Handling Terminal Errors

```go
import "sigs.k8s.io/controller-runtime/pkg/reconcile"

func (r *MyReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    var obj MyResource
    if err := r.Get(ctx, req.NamespacedName, &obj); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    
    // Validate the resource
    if err := validate(&obj); err != nil {
        // Validation error - no point in retrying
        return ctrl.Result{}, reconcile.TerminalError(
            fmt.Errorf("validation failed: %w", err),
        )
    }
    
    return ctrl.Result{}, nil
}
```

### Handling Not Found Errors

```go
import (
    apierrors "k8s.io/apimachinery/pkg/api/errors"
    "sigs.k8s.io/controller-runtime/pkg/client"
)

func (r *MyReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    var obj MyResource
    if err := r.Get(ctx, req.NamespacedName, &obj); err != nil {
        if apierrors.IsNotFound(err) {
            // Object not found, could have been deleted
            // Don't requeue
            return ctrl.Result{}, nil
        }
        // Other error
        return ctrl.Result{}, err
    }
    
    // Or use the helper
    if err := r.Get(ctx, req.NamespacedName, &obj); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    
    return ctrl.Result{}, nil
}
```

## ObjectReconciler

For simpler use cases, you can use `ObjectReconciler` which receives the full object:

```go
type MyObjectReconciler struct {
    client.Client
}

func (r *MyObjectReconciler) Reconcile(ctx context.Context, obj *MyResource) (ctrl.Result, error) {
    // Object is already fetched and passed in
    // No need to Get it from the API server
    
    // Reconcile logic
    return ctrl.Result{}, nil
}

// Register with builder
err := ctrl.NewControllerManagedBy(mgr).
    For(&MyResource{}).
    Complete(reconcile.AsReconciler(mgr.GetClient(), &MyObjectReconciler{
        Client: mgr.GetClient(),
    }))
```

## Function Reconciler

You can use a function as a reconciler:

```go
reconcileFunc := func(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // Reconciliation logic
    return ctrl.Result{}, nil
}

err := ctrl.NewControllerManagedBy(mgr).
    For(&corev1.Pod{}).
    Complete(reconcile.Func(reconcileFunc))
```

## Best Practices

### 1. Always Handle Deletion

```go
if !obj.DeletionTimestamp.IsZero() {
    // Handle deletion with finalizers
    return r.handleDeletion(ctx, &obj)
}
```

### 2. Use client.IgnoreNotFound

```go
if err := r.Get(ctx, req.NamespacedName, &obj); err != nil {
    return ctrl.Result{}, client.IgnoreNotFound(err)
}
```

### 3. Update Status Separately

```go
// Update spec
if err := r.Update(ctx, &obj); err != nil {
    return ctrl.Result{}, err
}

// Update status
if err := r.Status().Update(ctx, &obj); err != nil {
    return ctrl.Result{}, err
}
```

### 4. Be Idempotent

```go
// Check if work is already done
if isAlreadyDone(&obj) {
    return ctrl.Result{}, nil
}

// Do work
if err := doWork(ctx, &obj); err != nil {
    return ctrl.Result{}, err
}
```

### 5. Use Appropriate Requeue Strategy

```go
// Success - no requeue
return ctrl.Result{}, nil

// Transient error - requeue with backoff
return ctrl.Result{}, err

// Wait for external condition - requeue after delay
return ctrl.Result{RequeueAfter: 30 * time.Second}, nil

// Permanent error - don't requeue
return ctrl.Result{}, reconcile.TerminalError(err)
```

### 6. Log Appropriately

```go
func (r *MyReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := log.FromContext(ctx)
    
    log.Info("Starting reconciliation")
    
    // Reconciliation logic
    
    log.Info("Reconciliation complete")
    return ctrl.Result{}, nil
}
```

### 7. Handle Context Cancellation

```go
func (r *MyReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    select {
    case <-ctx.Done():
        // Context cancelled, stop reconciliation
        return ctrl.Result{}, ctx.Err()
    default:
    }
    
    // Reconciliation logic
    return ctrl.Result{}, nil
}
```

## Common Pitfalls

### 1. Don't Store State in Reconciler

```go
// BAD - state is not preserved across reconciliations
type BadReconciler struct {
    client.Client
    counter int // This will be reset
}

// GOOD - read state from API server
type GoodReconciler struct {
    client.Client
}

func (r *GoodReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    var obj MyResource
    if err := r.Get(ctx, req.NamespacedName, &obj); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    
    // Use obj.Status.Counter instead
    obj.Status.Counter++
    return ctrl.Result{}, r.Status().Update(ctx, &obj)
}
```

### 2. Don't Rely on Event Order

```go
// BAD - assuming events come in order
func (r *BadReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // Don't assume this is a Create event
    return r.handleCreate(ctx, req)
}

// GOOD - read current state
func (r *GoodReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    var obj MyResource
    if err := r.Get(ctx, req.NamespacedName, &obj); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    
    // Reconcile based on current state
    return r.reconcile(ctx, &obj)
}
```

### 3. Don't Forget to Update Status

```go
// BAD - status not updated
func (r *BadReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    var obj MyResource
    if err := r.Get(ctx, req.NamespacedName, &obj); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    
    obj.Status.Ready = true
    // Missing: r.Status().Update(ctx, &obj)
    
    return ctrl.Result{}, nil
}

// GOOD - status updated
func (r *GoodReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    var obj MyResource
    if err := r.Get(ctx, req.NamespacedName, &obj); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    
    obj.Status.Ready = true
    if err := r.Status().Update(ctx, &obj); err != nil {
        return ctrl.Result{}, err
    }
    
    return ctrl.Result{}, nil
}
```

## Related Packages

- [Controller Package](/docs/02-controller/) - Invokes reconcilers
- [Builder Package](/docs/04-builder/) - Builds controllers with reconcilers
- [Client Package](/docs/05-client/) - Used by reconcilers to interact with API server
