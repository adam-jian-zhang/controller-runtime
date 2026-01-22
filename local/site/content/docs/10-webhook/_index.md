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
<svg aria-roledescription="flowchart-v2" role="graphics-document document" viewBox="-8 -8 894.166015625 300" style="max-width: 894.166px; background-color: transparent;" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" width="100%" id="my-svg"><style>#my-svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}#my-svg .error-icon{fill:#552222;}#my-svg .error-text{fill:#552222;stroke:#552222;}#my-svg .edge-thickness-normal{stroke-width:2px;}#my-svg .edge-thickness-thick{stroke-width:3.5px;}#my-svg .edge-pattern-solid{stroke-dasharray:0;}#my-svg .edge-pattern-dashed{stroke-dasharray:3;}#my-svg .edge-pattern-dotted{stroke-dasharray:2;}#my-svg .marker{fill:#333333;stroke:#333333;}#my-svg .marker.cross{stroke:#333333;}#my-svg svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#my-svg .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#333;}#my-svg .cluster-label text{fill:#333;}#my-svg .cluster-label span,#my-svg p{color:#333;}#my-svg .label text,#my-svg span,#my-svg p{fill:#333;color:#333;}#my-svg .node rect,#my-svg .node circle,#my-svg .node ellipse,#my-svg .node polygon,#my-svg .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#my-svg .flowchart-label text{text-anchor:middle;}#my-svg .node .label{text-align:center;}#my-svg .node.clickable{cursor:pointer;}#my-svg .arrowheadPath{fill:#333333;}#my-svg .edgePath .path{stroke:#333333;stroke-width:2.0px;}#my-svg .flowchart-link{stroke:#333333;fill:none;}#my-svg .edgeLabel{background-color:#e8e8e8;text-align:center;}#my-svg .edgeLabel rect{opacity:0.5;background-color:#e8e8e8;fill:#e8e8e8;}#my-svg .labelBkg{background-color:rgba(232, 232, 232, 0.5);}#my-svg .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#my-svg .cluster text{fill:#333;}#my-svg .cluster span,#my-svg p{color:#333;}#my-svg div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(80, 100%, 96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#my-svg .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#333;}#my-svg :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}</style><g><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="6" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointEnd"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 0 L 10 5 L 0 10 z"/></marker><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="4.5" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-pointStart"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 5 L 10 10 L 10 0 z"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="11" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleEnd"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="-1" viewBox="0 0 10 10" class="marker flowchart" id="my-svg_flowchart-circleStart"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="12" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossEnd"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="-1" viewBox="0 0 11 11" class="marker cross flowchart" id="my-svg_flowchart-crossStart"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><g class="root"><g class="clusters"/><g class="edgePaths"><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Webhooks LE-Admission" id="L-Webhooks-Admission-0" d="M503.708984375,25.085914969256162L474.9817708333333,30.654929141046804C446.2545572916667,36.22394331283744,388.8001302083333,47.36197165641872,360.0729166666667,56.2143191615427C331.345703125,65.06666666666666,331.345703125,71.63333333333334,331.345703125,74.91666666666667L331.345703125,78.2"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Webhooks LE-Conversion" id="L-Webhooks-Conversion-0" d="M546.708984375,33.5L546.708984375,37.666666666666664C546.708984375,41.833333333333336,546.708984375,50.166666666666664,546.708984375,57.61666666666667C546.708984375,65.06666666666666,546.708984375,71.63333333333334,546.708984375,74.91666666666667L546.708984375,78.2"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Webhooks LE-Authentication" id="L-Webhooks-Authentication-0" d="M589.708984375,24.456744474628568L621.3665364583334,30.130620395523806C653.0240885416666,35.80449631641904,716.3391927083334,47.152248158209524,747.9967447916666,56.1094574124381C779.654296875,65.06666666666666,779.654296875,71.63333333333334,779.654296875,74.91666666666667L779.654296875,78.2"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Admission LE-Mutating" id="L-Admission-Mutating-0" d="M258.5212855538922,117L240.40575879491016,121.16666666666667C222.29023203592814,125.33333333333333,186.05917851796406,133.66666666666666,167.94365175898204,141.11666666666667C149.828125,148.56666666666666,149.828125,155.13333333333333,149.828125,158.41666666666666L149.828125,161.7"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Admission LE-Validating" id="L-Admission-Validating-0" d="M405.89009870883234,117L424.4334806948603,121.16666666666667C442.9768626808882,125.33333333333333,480.0636266529441,133.66666666666666,498.60700863897205,141.11666666666667C517.150390625,148.56666666666666,517.150390625,155.13333333333333,517.150390625,158.41666666666666L517.150390625,161.7"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Mutating LE-Default" id="L-Mutating-Default-0" d="M113.32697885479041,200.5L104.24709175399202,204.66666666666666C95.16720465319361,208.83333333333334,77.0074304515968,217.16666666666666,67.9275433507984,224.61666666666667C58.84765625,232.0666666666667,58.84765625,238.63333333333333,58.84765625,241.91666666666666L58.84765625,245.2"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Mutating LE-Transform" id="L-Mutating-Transform-0" d="M186.3292711452096,200.5L195.409158246008,204.66666666666666C204.4890453468064,208.83333333333334,222.64881954840317,217.16666666666666,231.7287066492016,224.61666666666667C240.80859375,232.0666666666667,240.80859375,238.63333333333333,240.80859375,241.91666666666666L240.80859375,245.2"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Validating LE-Validate" id="L-Validating-Validate-0" d="M482.36922249251495,200.5L473.71719061876246,204.66666666666666C465.06515874500997,208.83333333333334,447.7610949975049,217.16666666666666,439.1090631237525,224.61666666666667C430.45703125,232.0666666666667,430.45703125,238.63333333333333,430.45703125,241.91666666666666L430.45703125,245.2"/><path marker-end="url(#my-svg_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-Validating LE-Reject" id="L-Validating-Reject-0" d="M551.931558757485,200.5L560.5835906312376,204.66666666666666C569.23562250499,208.83333333333334,586.539686252495,217.16666666666666,595.1917181262476,224.61666666666667C603.84375,232.0666666666667,603.84375,238.63333333333333,603.84375,241.91666666666666L603.84375,245.2"/></g><g class="edgeLabels"><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g></g><g class="nodes"><g transform="translate(546.708984375, 16.75)" id="flowchart-Webhooks-0" class="node default default flowchart-label"><rect height="33.5" width="86" y="-16.75" x="-43" ry="0" rx="0" style="fill:#e1f5ff;" class="basic label-container"/><g transform="translate(-35.5, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="71"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Webhooks</span></div></foreignObject></g></g><g transform="translate(331.345703125, 100.25)" id="flowchart-Admission-2" class="node default default flowchart-label"><rect height="33.5" width="161.859375" y="-16.75" x="-80.9296875" ry="0" rx="0" style="fill:#fff4e1;" class="basic label-container"/><g transform="translate(-73.4296875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="146.859375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Admission Webhooks</span></div></foreignObject></g></g><g transform="translate(546.708984375, 100.25)" id="flowchart-Conversion-4" class="node default default flowchart-label"><rect height="33.5" width="168.8671875" y="-16.75" x="-84.43359375" ry="0" rx="0" style="fill:#f0f0f0;" class="basic label-container"/><g transform="translate(-76.93359375, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="153.8671875"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Conversion Webhooks</span></div></foreignObject></g></g><g transform="translate(779.654296875, 100.25)" id="flowchart-Authentication-6" class="node default default flowchart-label"><rect height="33.5" width="197.0234375" y="-16.75" x="-98.51171875" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-91.01171875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="182.0234375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Authentication Webhooks</span></div></foreignObject></g></g><g transform="translate(149.828125, 183.75)" id="flowchart-Mutating-8" class="node default default flowchart-label"><rect height="33.5" width="153.34375" y="-16.75" x="-76.671875" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-69.171875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="138.34375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Mutating Webhooks</span></div></foreignObject></g></g><g transform="translate(517.150390625, 183.75)" id="flowchart-Validating-10" class="node default default flowchart-label"><rect height="33.5" width="161.6484375" y="-16.75" x="-80.82421875" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-73.32421875, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="146.6484375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Validating Webhooks</span></div></foreignObject></g></g><g transform="translate(58.84765625, 267.25)" id="flowchart-Default-12" class="node default default flowchart-label"><rect height="33.5" width="117.6953125" y="-16.75" x="-58.84765625" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-51.34765625, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="102.6953125"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Default Values</span></div></foreignObject></g></g><g transform="translate(240.80859375, 267.25)" id="flowchart-Transform-14" class="node default default flowchart-label"><rect height="33.5" width="146.2265625" y="-16.75" x="-73.11328125" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-65.61328125, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="131.2265625"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Transform Objects</span></div></foreignObject></g></g><g transform="translate(430.45703125, 267.25)" id="flowchart-Validate-16" class="node default default flowchart-label"><rect height="33.5" width="133.0703125" y="-16.75" x="-66.53515625" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-59.03515625, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="118.0703125"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Validate Objects</span></div></foreignObject></g></g><g transform="translate(603.84375, 267.25)" id="flowchart-Reject-18" class="node default default flowchart-label"><rect height="33.5" width="113.703125" y="-16.75" x="-56.8515625" ry="0" rx="0" style="" class="basic label-container"/><g transform="translate(-49.3515625, -9.25)" style="" class="label"><rect/><foreignObject height="18.5" width="98.703125"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Reject Invalid</span></div></foreignObject></g></g></g></g></g></svg>
</div>

## Admission Webhooks

### Webhook Flow

<div class="mermaid-diagram">
<svg aria-roledescription="sequence" role="graphics-document document" viewBox="-50 -10 741 653" style="max-width: 741px; background-color: transparent;" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" width="100%" id="my-svg"><g><rect class="actor" ry="3" rx="3" height="65" width="150" stroke="#666" fill="#eaeaea" y="567" x="454"/><text style="text-anchor: middle; font-size: 16px; font-weight: 400;" class="actor" alignment-baseline="central" dominant-baseline="central" y="599.5" x="529"><tspan dy="0" x="529">Webhook Handler</tspan></text></g><g><rect class="actor" ry="3" rx="3" height="65" width="150" stroke="#666" fill="#eaeaea" y="567" x="254"/><text style="text-anchor: middle; font-size: 16px; font-weight: 400;" class="actor" alignment-baseline="central" dominant-baseline="central" y="599.5" x="329"><tspan dy="0" x="329">Webhook Server</tspan></text></g><g><rect class="actor" ry="3" rx="3" height="65" width="150" stroke="#666" fill="#eaeaea" y="567" x="0"/><text style="text-anchor: middle; font-size: 16px; font-weight: 400;" class="actor" alignment-baseline="central" dominant-baseline="central" y="599.5" x="75"><tspan dy="0" x="75">API Server</tspan></text></g><g><line stroke="#999" stroke-width="0.5px" class="200" y2="567" x2="529" y1="5" x1="529" id="actor2"/><g id="root-2"><rect class="actor" ry="3" rx="3" height="65" width="150" stroke="#666" fill="#eaeaea" y="0" x="454"/><text style="text-anchor: middle; font-size: 16px; font-weight: 400;" class="actor" alignment-baseline="central" dominant-baseline="central" y="32.5" x="529"><tspan dy="0" x="529">Webhook Handler</tspan></text></g></g><g><line stroke="#999" stroke-width="0.5px" class="200" y2="567" x2="329" y1="5" x1="329" id="actor1"/><g id="root-1"><rect class="actor" ry="3" rx="3" height="65" width="150" stroke="#666" fill="#eaeaea" y="0" x="254"/><text style="text-anchor: middle; font-size: 16px; font-weight: 400;" class="actor" alignment-baseline="central" dominant-baseline="central" y="32.5" x="329"><tspan dy="0" x="329">Webhook Server</tspan></text></g></g><g><line stroke="#999" stroke-width="0.5px" class="200" y2="567" x2="75" y1="5" x1="75" id="actor0"/><g id="root-0"><rect class="actor" ry="3" rx="3" height="65" width="150" stroke="#666" fill="#eaeaea" y="0" x="0"/><text style="text-anchor: middle; font-size: 16px; font-weight: 400;" class="actor" alignment-baseline="central" dominant-baseline="central" y="32.5" x="75"><tspan dy="0" x="75">API Server</tspan></text></g></g><style>#my-svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}#my-svg .error-icon{fill:#552222;}#my-svg .error-text{fill:#552222;stroke:#552222;}#my-svg .edge-thickness-normal{stroke-width:2px;}#my-svg .edge-thickness-thick{stroke-width:3.5px;}#my-svg .edge-pattern-solid{stroke-dasharray:0;}#my-svg .edge-pattern-dashed{stroke-dasharray:3;}#my-svg .edge-pattern-dotted{stroke-dasharray:2;}#my-svg .marker{fill:#333333;stroke:#333333;}#my-svg .marker.cross{stroke:#333333;}#my-svg svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#my-svg .actor{stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:#ECECFF;}#my-svg text.actor&gt;tspan{fill:black;stroke:none;}#my-svg .actor-line{stroke:grey;}#my-svg .messageLine0{stroke-width:1.5;stroke-dasharray:none;stroke:#333;}#my-svg .messageLine1{stroke-width:1.5;stroke-dasharray:2,2;stroke:#333;}#my-svg #arrowhead path{fill:#333;stroke:#333;}#my-svg .sequenceNumber{fill:white;}#my-svg #sequencenumber{fill:#333;}#my-svg #crosshead path{fill:#333;stroke:#333;}#my-svg .messageText{fill:#333;stroke:none;}#my-svg .labelBox{stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:#ECECFF;}#my-svg .labelText,#my-svg .labelText&gt;tspan{fill:black;stroke:none;}#my-svg .loopText,#my-svg .loopText&gt;tspan{fill:black;stroke:none;}#my-svg .loopLine{stroke-width:2px;stroke-dasharray:2,2;stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);}#my-svg .note{stroke:#aaaa33;fill:#fff5ad;}#my-svg .noteText,#my-svg .noteText&gt;tspan{fill:black;stroke:none;}#my-svg .activation0{fill:#f4f4f4;stroke:#666;}#my-svg .activation1{fill:#f4f4f4;stroke:#666;}#my-svg .activation2{fill:#f4f4f4;stroke:#666;}#my-svg .actorPopupMenu{position:absolute;}#my-svg .actorPopupMenuPanel{position:absolute;fill:#ECECFF;box-shadow:0px 8px 16px 0px rgba(0,0,0,0.2);filter:drop-shadow(3px 5px 2px rgb(0 0 0 / 0.4));}#my-svg .actor-man line{stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:#ECECFF;}#my-svg .actor-man circle,#my-svg line{stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:#ECECFF;stroke-width:2px;}#my-svg :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}</style><g/><defs><symbol height="24" width="24" id="computer"><path d="M2 2v13h20v-13h-20zm18 11h-16v-9h16v9zm-10.228 6l.466-1h3.524l.467 1h-4.457zm14.228 3h-24l2-6h2.104l-1.33 4h18.45l-1.297-4h2.073l2 6zm-5-10h-14v-7h14v7z" transform="scale(.5)"/></symbol></defs><defs><symbol clip-rule="evenodd" fill-rule="evenodd" id="database"><path d="M12.258.001l.256.004.255.005.253.008.251.01.249.012.247.015.246.016.242.019.241.02.239.023.236.024.233.027.231.028.229.031.225.032.223.034.22.036.217.038.214.04.211.041.208.043.205.045.201.046.198.048.194.05.191.051.187.053.183.054.18.056.175.057.172.059.168.06.163.061.16.063.155.064.15.066.074.033.073.033.071.034.07.034.069.035.068.035.067.035.066.035.064.036.064.036.062.036.06.036.06.037.058.037.058.037.055.038.055.038.053.038.052.038.051.039.05.039.048.039.047.039.045.04.044.04.043.04.041.04.04.041.039.041.037.041.036.041.034.041.033.042.032.042.03.042.029.042.027.042.026.043.024.043.023.043.021.043.02.043.018.044.017.043.015.044.013.044.012.044.011.045.009.044.007.045.006.045.004.045.002.045.001.045v17l-.001.045-.002.045-.004.045-.006.045-.007.045-.009.044-.011.045-.012.044-.013.044-.015.044-.017.043-.018.044-.02.043-.021.043-.023.043-.024.043-.026.043-.027.042-.029.042-.03.042-.032.042-.033.042-.034.041-.036.041-.037.041-.039.041-.04.041-.041.04-.043.04-.044.04-.045.04-.047.039-.048.039-.05.039-.051.039-.052.038-.053.038-.055.038-.055.038-.058.037-.058.037-.06.037-.06.036-.062.036-.064.036-.064.036-.066.035-.067.035-.068.035-.069.035-.07.034-.071.034-.073.033-.074.033-.15.066-.155.064-.16.063-.163.061-.168.06-.172.059-.175.057-.18.056-.183.054-.187.053-.191.051-.194.05-.198.048-.201.046-.205.045-.208.043-.211.041-.214.04-.217.038-.22.036-.223.034-.225.032-.229.031-.231.028-.233.027-.236.024-.239.023-.241.02-.242.019-.246.016-.247.015-.249.012-.251.01-.253.008-.255.005-.256.004-.258.001-.258-.001-.256-.004-.255-.005-.253-.008-.251-.01-.249-.012-.247-.015-.245-.016-.243-.019-.241-.02-.238-.023-.236-.024-.234-.027-.231-.028-.228-.031-.226-.032-.223-.034-.22-.036-.217-.038-.214-.04-.211-.041-.208-.043-.204-.045-.201-.046-.198-.048-.195-.05-.19-.051-.187-.053-.184-.054-.179-.056-.176-.057-.172-.059-.167-.06-.164-.061-.159-.063-.155-.064-.151-.066-.074-.033-.072-.033-.072-.034-.07-.034-.069-.035-.068-.035-.067-.035-.066-.035-.064-.036-.063-.036-.062-.036-.061-.036-.06-.037-.058-.037-.057-.037-.056-.038-.055-.038-.053-.038-.052-.038-.051-.039-.049-.039-.049-.039-.046-.039-.046-.04-.044-.04-.043-.04-.041-.04-.04-.041-.039-.041-.037-.041-.036-.041-.034-.041-.033-.042-.032-.042-.03-.042-.029-.042-.027-.042-.026-.043-.024-.043-.023-.043-.021-.043-.02-.043-.018-.044-.017-.043-.015-.044-.013-.044-.012-.044-.011-.045-.009-.044-.007-.045-.006-.045-.004-.045-.002-.045-.001-.045v-17l.001-.045.002-.045.004-.045.006-.045.007-.045.009-.044.011-.045.012-.044.013-.044.015-.044.017-.043.018-.044.02-.043.021-.043.023-.043.024-.043.026-.043.027-.042.029-.042.03-.042.032-.042.033-.042.034-.041.036-.041.037-.041.039-.041.04-.041.041-.04.043-.04.044-.04.046-.04.046-.039.049-.039.049-.039.051-.039.052-.038.053-.038.055-.038.056-.038.057-.037.058-.037.06-.037.061-.036.062-.036.063-.036.064-.036.066-.035.067-.035.068-.035.069-.035.07-.034.072-.034.072-.033.074-.033.151-.066.155-.064.159-.063.164-.061.167-.06.172-.059.176-.057.179-.056.184-.054.187-.053.19-.051.195-.05.198-.048.201-.046.204-.045.208-.043.211-.041.214-.04.217-.038.22-.036.223-.034.226-.032.228-.031.231-.028.234-.027.236-.024.238-.023.241-.02.243-.019.245-.016.247-.015.249-.012.251-.01.253-.008.255-.005.256-.004.258-.001.258.001zm-9.258 20.499v.01l.001.021.003.021.004.022.005.021.006.022.007.022.009.023.01.022.011.023.012.023.013.023.015.023.016.024.017.023.018.024.019.024.021.024.022.025.023.024.024.025.052.049.056.05.061.051.066.051.07.051.075.051.079.052.084.052.088.052.092.052.097.052.102.051.105.052.11.052.114.051.119.051.123.051.127.05.131.05.135.05.139.048.144.049.147.047.152.047.155.047.16.045.163.045.167.043.171.043.176.041.178.041.183.039.187.039.19.037.194.035.197.035.202.033.204.031.209.03.212.029.216.027.219.025.222.024.226.021.23.02.233.018.236.016.24.015.243.012.246.01.249.008.253.005.256.004.259.001.26-.001.257-.004.254-.005.25-.008.247-.011.244-.012.241-.014.237-.016.233-.018.231-.021.226-.021.224-.024.22-.026.216-.027.212-.028.21-.031.205-.031.202-.034.198-.034.194-.036.191-.037.187-.039.183-.04.179-.04.175-.042.172-.043.168-.044.163-.045.16-.046.155-.046.152-.047.148-.048.143-.049.139-.049.136-.05.131-.05.126-.05.123-.051.118-.052.114-.051.11-.052.106-.052.101-.052.096-.052.092-.052.088-.053.083-.051.079-.052.074-.052.07-.051.065-.051.06-.051.056-.05.051-.05.023-.024.023-.025.021-.024.02-.024.019-.024.018-.024.017-.024.015-.023.014-.024.013-.023.012-.023.01-.023.01-.022.008-.022.006-.022.006-.022.004-.022.004-.021.001-.021.001-.021v-4.127l-.077.055-.08.053-.083.054-.085.053-.087.052-.09.052-.093.051-.095.05-.097.05-.1.049-.102.049-.105.048-.106.047-.109.047-.111.046-.114.045-.115.045-.118.044-.12.043-.122.042-.124.042-.126.041-.128.04-.13.04-.132.038-.134.038-.135.037-.138.037-.139.035-.142.035-.143.034-.144.033-.147.032-.148.031-.15.03-.151.03-.153.029-.154.027-.156.027-.158.026-.159.025-.161.024-.162.023-.163.022-.165.021-.166.02-.167.019-.169.018-.169.017-.171.016-.173.015-.173.014-.175.013-.175.012-.177.011-.178.01-.179.008-.179.008-.181.006-.182.005-.182.004-.184.003-.184.002h-.37l-.184-.002-.184-.003-.182-.004-.182-.005-.181-.006-.179-.008-.179-.008-.178-.01-.176-.011-.176-.012-.175-.013-.173-.014-.172-.015-.171-.016-.17-.017-.169-.018-.167-.019-.166-.02-.165-.021-.163-.022-.162-.023-.161-.024-.159-.025-.157-.026-.156-.027-.155-.027-.153-.029-.151-.03-.15-.03-.148-.031-.146-.032-.145-.033-.143-.034-.141-.035-.14-.035-.137-.037-.136-.037-.134-.038-.132-.038-.13-.04-.128-.04-.126-.041-.124-.042-.122-.042-.12-.044-.117-.043-.116-.045-.113-.045-.112-.046-.109-.047-.106-.047-.105-.048-.102-.049-.1-.049-.097-.05-.095-.05-.093-.052-.09-.051-.087-.052-.085-.053-.083-.054-.08-.054-.077-.054v4.127zm0-5.654v.011l.001.021.003.021.004.021.005.022.006.022.007.022.009.022.01.022.011.023.012.023.013.023.015.024.016.023.017.024.018.024.019.024.021.024.022.024.023.025.024.024.052.05.056.05.061.05.066.051.07.051.075.052.079.051.084.052.088.052.092.052.097.052.102.052.105.052.11.051.114.051.119.052.123.05.127.051.131.05.135.049.139.049.144.048.147.048.152.047.155.046.16.045.163.045.167.044.171.042.176.042.178.04.183.04.187.038.19.037.194.036.197.034.202.033.204.032.209.03.212.028.216.027.219.025.222.024.226.022.23.02.233.018.236.016.24.014.243.012.246.01.249.008.253.006.256.003.259.001.26-.001.257-.003.254-.006.25-.008.247-.01.244-.012.241-.015.237-.016.233-.018.231-.02.226-.022.224-.024.22-.025.216-.027.212-.029.21-.03.205-.032.202-.033.198-.035.194-.036.191-.037.187-.039.183-.039.179-.041.175-.042.172-.043.168-.044.163-.045.16-.045.155-.047.152-.047.148-.048.143-.048.139-.05.136-.049.131-.05.126-.051.123-.051.118-.051.114-.052.11-.052.106-.052.101-.052.096-.052.092-.052.088-.052.083-.052.079-.052.074-.051.07-.052.065-.051.06-.05.056-.051.051-.049.023-.025.023-.024.021-.025.02-.024.019-.024.018-.024.017-.024.015-.023.014-.023.013-.024.012-.022.01-.023.01-.023.008-.022.006-.022.006-.022.004-.021.004-.022.001-.021.001-.021v-4.139l-.077.054-.08.054-.083.054-.085.052-.087.053-.09.051-.093.051-.095.051-.097.05-.1.049-.102.049-.105.048-.106.047-.109.047-.111.046-.114.045-.115.044-.118.044-.12.044-.122.042-.124.042-.126.041-.128.04-.13.039-.132.039-.134.038-.135.037-.138.036-.139.036-.142.035-.143.033-.144.033-.147.033-.148.031-.15.03-.151.03-.153.028-.154.028-.156.027-.158.026-.159.025-.161.024-.162.023-.163.022-.165.021-.166.02-.167.019-.169.018-.169.017-.171.016-.173.015-.173.014-.175.013-.175.012-.177.011-.178.009-.179.009-.179.007-.181.007-.182.005-.182.004-.184.003-.184.002h-.37l-.184-.002-.184-.003-.182-.004-.182-.005-.181-.007-.179-.007-.179-.009-.178-.009-.176-.011-.176-.012-.175-.013-.173-.014-.172-.015-.171-.016-.17-.017-.169-.018-.167-.019-.166-.02-.165-.021-.163-.022-.162-.023-.161-.024-.159-.025-.157-.026-.156-.027-.155-.028-.153-.028-.151-.03-.15-.03-.148-.031-.146-.033-.145-.033-.143-.033-.141-.035-.14-.036-.137-.036-.136-.037-.134-.038-.132-.039-.13-.039-.128-.04-.126-.041-.124-.042-.122-.043-.12-.043-.117-.044-.116-.044-.113-.046-.112-.046-.109-.046-.106-.047-.105-.048-.102-.049-.1-.049-.097-.05-.095-.051-.093-.051-.09-.051-.087-.053-.085-.052-.083-.054-.08-.054-.077-.054v4.139zm0-5.666v.011l.001.02.003.022.004.021.005.022.006.021.007.022.009.023.01.022.011.023.012.023.013.023.015.023.016.024.017.024.018.023.019.024.021.025.022.024.023.024.024.025.052.05.056.05.061.05.066.051.07.051.075.052.079.051.084.052.088.052.092.052.097.052.102.052.105.051.11.052.114.051.119.051.123.051.127.05.131.05.135.05.139.049.144.048.147.048.152.047.155.046.16.045.163.045.167.043.171.043.176.042.178.04.183.04.187.038.19.037.194.036.197.034.202.033.204.032.209.03.212.028.216.027.219.025.222.024.226.021.23.02.233.018.236.017.24.014.243.012.246.01.249.008.253.006.256.003.259.001.26-.001.257-.003.254-.006.25-.008.247-.01.244-.013.241-.014.237-.016.233-.018.231-.02.226-.022.224-.024.22-.025.216-.027.212-.029.21-.03.205-.032.202-.033.198-.035.194-.036.191-.037.187-.039.183-.039.179-.041.175-.042.172-.043.168-.044.163-.045.16-.045.155-.047.152-.047.148-.048.143-.049.139-.049.136-.049.131-.051.126-.05.123-.051.118-.052.114-.051.11-.052.106-.052.101-.052.096-.052.092-.052.088-.052.083-.052.079-.052.074-.052.07-.051.065-.051.06-.051.056-.05.051-.049.023-.025.023-.025.021-.024.02-.024.019-.024.018-.024.017-.024.015-.023.014-.024.013-.023.012-.023.01-.022.01-.023.008-.022.006-.022.006-.022.004-.022.004-.021.001-.021.001-.021v-4.153l-.077.054-.08.054-.083.053-.085.053-.087.053-.09.051-.093.051-.095.051-.097.05-.1.049-.102.048-.105.048-.106.048-.109.046-.111.046-.114.046-.115.044-.118.044-.12.043-.122.043-.124.042-.126.041-.128.04-.13.039-.132.039-.134.038-.135.037-.138.036-.139.036-.142.034-.143.034-.144.033-.147.032-.148.032-.15.03-.151.03-.153.028-.154.028-.156.027-.158.026-.159.024-.161.024-.162.023-.163.023-.165.021-.166.02-.167.019-.169.018-.169.017-.171.016-.173.015-.173.014-.175.013-.175.012-.177.01-.178.01-.179.009-.179.007-.181.006-.182.006-.182.004-.184.003-.184.001-.185.001-.185-.001-.184-.001-.184-.003-.182-.004-.182-.006-.181-.006-.179-.007-.179-.009-.178-.01-.176-.01-.176-.012-.175-.013-.173-.014-.172-.015-.171-.016-.17-.017-.169-.018-.167-.019-.166-.02-.165-.021-.163-.023-.162-.023-.161-.024-.159-.024-.157-.026-.156-.027-.155-.028-.153-.028-.151-.03-.15-.03-.148-.032-.146-.032-.145-.033-.143-.034-.141-.034-.14-.036-.137-.036-.136-.037-.134-.038-.132-.039-.13-.039-.128-.041-.126-.041-.124-.041-.122-.043-.12-.043-.117-.044-.116-.044-.113-.046-.112-.046-.109-.046-.106-.048-.105-.048-.102-.048-.1-.05-.097-.049-.095-.051-.093-.051-.09-.052-.087-.052-.085-.053-.083-.053-.08-.054-.077-.054v4.153zm8.74-8.179l-.257.004-.254.005-.25.008-.247.011-.244.012-.241.014-.237.016-.233.018-.231.021-.226.022-.224.023-.22.026-.216.027-.212.028-.21.031-.205.032-.202.033-.198.034-.194.036-.191.038-.187.038-.183.04-.179.041-.175.042-.172.043-.168.043-.163.045-.16.046-.155.046-.152.048-.148.048-.143.048-.139.049-.136.05-.131.05-.126.051-.123.051-.118.051-.114.052-.11.052-.106.052-.101.052-.096.052-.092.052-.088.052-.083.052-.079.052-.074.051-.07.052-.065.051-.06.05-.056.05-.051.05-.023.025-.023.024-.021.024-.02.025-.019.024-.018.024-.017.023-.015.024-.014.023-.013.023-.012.023-.01.023-.01.022-.008.022-.006.023-.006.021-.004.022-.004.021-.001.021-.001.021.001.021.001.021.004.021.004.022.006.021.006.023.008.022.01.022.01.023.012.023.013.023.014.023.015.024.017.023.018.024.019.024.02.025.021.024.023.024.023.025.051.05.056.05.06.05.065.051.07.052.074.051.079.052.083.052.088.052.092.052.096.052.101.052.106.052.11.052.114.052.118.051.123.051.126.051.131.05.136.05.139.049.143.048.148.048.152.048.155.046.16.046.163.045.168.043.172.043.175.042.179.041.183.04.187.038.191.038.194.036.198.034.202.033.205.032.21.031.212.028.216.027.22.026.224.023.226.022.231.021.233.018.237.016.241.014.244.012.247.011.25.008.254.005.257.004.26.001.26-.001.257-.004.254-.005.25-.008.247-.011.244-.012.241-.014.237-.016.233-.018.231-.021.226-.022.224-.023.22-.026.216-.027.212-.028.21-.031.205-.032.202-.033.198-.034.194-.036.191-.038.187-.038.183-.04.179-.041.175-.042.172-.043.168-.043.163-.045.16-.046.155-.046.152-.048.148-.048.143-.048.139-.049.136-.05.131-.05.126-.051.123-.051.118-.051.114-.052.11-.052.106-.052.101-.052.096-.052.092-.052.088-.052.083-.052.079-.052.074-.051.07-.052.065-.051.06-.05.056-.05.051-.05.023-.025.023-.024.021-.024.02-.025.019-.024.018-.024.017-.023.015-.024.014-.023.013-.023.012-.023.01-.023.01-.022.008-.022.006-.023.006-.021.004-.022.004-.021.001-.021.001-.021-.001-.021-.001-.021-.004-.021-.004-.022-.006-.021-.006-.023-.008-.022-.01-.022-.01-.023-.012-.023-.013-.023-.014-.023-.015-.024-.017-.023-.018-.024-.019-.024-.02-.025-.021-.024-.023-.024-.023-.025-.051-.05-.056-.05-.06-.05-.065-.051-.07-.052-.074-.051-.079-.052-.083-.052-.088-.052-.092-.052-.096-.052-.101-.052-.106-.052-.11-.052-.114-.052-.118-.051-.123-.051-.126-.051-.131-.05-.136-.05-.139-.049-.143-.048-.148-.048-.152-.048-.155-.046-.16-.046-.163-.045-.168-.043-.172-.043-.175-.042-.179-.041-.183-.04-.187-.038-.191-.038-.194-.036-.198-.034-.202-.033-.205-.032-.21-.031-.212-.028-.216-.027-.22-.026-.224-.023-.226-.022-.231-.021-.233-.018-.237-.016-.241-.014-.244-.012-.247-.011-.25-.008-.254-.005-.257-.004-.26-.001-.26.001z" transform="scale(.5)"/></symbol></defs><defs><symbol height="24" width="24" id="clock"><path d="M12 2c5.514 0 10 4.486 10 10s-4.486 10-10 10-10-4.486-10-10 4.486-10 10-10zm0-2c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm5.848 12.459c.202.038.202.333.001.372-1.907.361-6.045 1.111-6.547 1.111-.719 0-1.301-.582-1.301-1.301 0-.512.77-5.447 1.125-7.445.034-.192.312-.181.343.014l.985 6.238 5.394 1.011z" transform="scale(.5)"/></symbol></defs><defs><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="7.9" id="arrowhead"><path d="M 0 0 L 10 5 L 0 10 z"/></marker></defs><defs><marker refY="4.5" refX="4" orient="auto" markerHeight="8" markerWidth="15" id="crosshead"><path style="stroke-dasharray: 0, 0;" d="M 1,2 L 6,7 M 6,2 L 1,7" stroke-width="1pt" stroke="#000000" fill="none"/></marker></defs><defs><marker orient="auto" markerHeight="28" markerWidth="20" refY="7" refX="15.5" id="filled-head"><path d="M 18,7 L9,13 L14,7 L9,1 Z"/></marker></defs><defs><marker orient="auto" markerHeight="40" markerWidth="60" refY="15" refX="15" id="sequencenumber"><circle r="6" cy="15" cx="15"/></marker></defs><g><line class="loopLine" y2="167" x2="641" y1="167" x1="318"/><line class="loopLine" y2="501" x2="641" y1="167" x1="641"/><line class="loopLine" y2="501" x2="641" y1="501" x1="318"/><line class="loopLine" y2="501" x2="318" y1="167" x1="318"/><line style="stroke-dasharray: 3, 3;" class="loopLine" y2="339" x2="641" y1="339" x1="318"/><polygon class="labelBox" points="318,167 368,167 368,180 359.6,187 318,187"/><text style="font-size: 16px; font-weight: 400;" class="labelText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="180" x="343">alt</text><text style="font-size: 16px; font-weight: 400;" class="loopText" text-anchor="middle" y="185" x="504.5"><tspan x="504.5">[Mutating Webhook]</tspan></text><text style="font-size: 16px; font-weight: 400;" class="loopText" text-anchor="middle" y="357" x="479.5">[Validating Webhook]</text></g><text style="font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="80" x="201">AdmissionReview Request</text><line style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" y2="111" x2="325" y1="111" x1="76"/><text style="font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="126" x="428">Decode &amp; Route</text><line style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" y2="157" x2="525" y1="157" x1="330"/><text style="font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="217" x="530">Default()</text><path style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" d="M 530,248 C 590,238 590,278 530,268"/><text style="font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="293" x="431">Patches</text><line style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" y2="324" x2="333" y1="324" x1="528"/><text style="font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="384" x="530">ValidateCreate/Update/Delete()</text><path style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" d="M 530,415 C 590,405 590,445 530,435"/><text style="font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="460" x="431">Allowed/Denied</text><line style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" y2="491" x2="333" y1="491" x1="528"/><text style="font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="516" x="204">AdmissionReview Response</text><line style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" y2="547" x2="79" y1="547" x1="328"/></svg>
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
