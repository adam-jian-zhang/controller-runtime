---
title: "Architecture"
weight: -1
---


## Introduction

Controller-runtime is a set of Go libraries for building Kubernetes controllers. It provides a framework for creating custom controllers that watch and reconcile Kubernetes resources, following Kubernetes controller best practices. It is the foundation for tools like Kubebuilder and Operator SDK.

## Project Information

- **Module**: `sigs.k8s.io/controller-runtime`
- **Go Version**: 1.25.0
- **Kubernetes Version**: v0.35
- **License**: Apache License 2.0

## High-Level Architecture

The controller-runtime framework follows a layered architecture that abstracts common Kubernetes controller patterns:

<div class="mermaid-diagram">
<img src="/images/diagrams/diagram-c940f739c5fe.svg" alt="Diagram" />
</div>


## Core Components

### 1. Manager

The **Manager** is the central orchestrator that:
- Initializes and manages shared dependencies (caches, clients, schemes)
- Starts and stops controllers and webhooks
- Handles leader election for high availability
- Manages graceful shutdown
- Provides health and readiness checks
- Serves metrics endpoints

**Key Responsibilities**:
- Lifecycle management of all controllers and webhooks
- Dependency injection for shared resources
- Signal handling for graceful termination

### 2. Controller

A **Controller** is responsible for:
- Watching Kubernetes resources for changes
- Enqueueing reconciliation requests
- Processing work items from a queue
- Invoking reconcilers with appropriate rate limiting and error handling

**Key Features**:
- Configurable concurrency (MaxConcurrentReconciles)
- Built-in rate limiting and exponential backoff
- Support for priority queues
- Panic recovery
- Leader election awareness

### 3. Reconciler

The **Reconciler** contains the business logic that:
- Receives reconciliation requests (namespace/name)
- Reads the current state from the API server
- Compares desired state vs actual state
- Takes actions to converge to desired state
- Returns results indicating success, requeue, or error

**Reconciliation Pattern**:
- Level-based (not edge-triggered)
- Idempotent operations
- Error handling with automatic retry

### 4. Cache

The **Cache** provides:
- Local in-memory cache of Kubernetes objects
- Automatic population via informers
- Watch capabilities for resource changes
- Field indexing for efficient lookups
- Namespace filtering and label/field selectors

**Benefits**:
- Reduces load on API server
- Improves controller performance
- Provides consistent read semantics

### 5. Client

The **Client** offers a unified interface for:
- **Reading**: Get and List operations (typically from cache)
- **Writing**: Create, Update, Delete, Patch operations (directly to API server)
- **Status updates**: Separate subresource client
- **Typed and unstructured access**: Support for both typed objects and unstructured data

**Client Types**:
- Default split client (reads from cache, writes to API)
- Direct client (all operations to API server)
- Fake client (for testing)

### 6. Builder

The **Builder** provides a fluent API for:
- Constructing controllers with minimal boilerplate
- Configuring watch sources (For, Owns, Watches)
- Setting up event handlers and predicates
- Wiring controllers to the manager

**Builder Pattern Benefits**:
- Declarative controller setup
- Type-safe configuration
- Reduced boilerplate code

### 7. Webhook

The **Webhook** subsystem supports:
- **Admission webhooks**: Validating and mutating webhooks
- **Conversion webhooks**: CRD version conversion
- **Authentication webhooks**: Token review
- Certificate management with automatic rotation

## Event Flow

<div class="mermaid-diagram">
<img src="/images/diagrams/diagram-6e0bc6fdff2e.svg" alt="Diagram" />
</div>


## Data Flow

<div class="mermaid-diagram">
<img src="/images/diagrams/diagram-4d961c181f8a.svg" alt="Diagram" />
</div>


## Package Organization

The controller-runtime project is organized into the following main packages:

| Package | Purpose |
|---------|---------|
| `pkg/manager` | Manager implementation and options |
| `pkg/controller` | Controller implementation and interfaces |
| `pkg/reconcile` | Reconciler interface and types |
| `pkg/builder` | Builder for constructing controllers |
| `pkg/client` | Kubernetes client interfaces and implementations |
| `pkg/cache` | Cache implementation using informers |
| `pkg/source` | Event sources for controllers |
| `pkg/handler` | Event handlers for processing events |
| `pkg/predicate` | Filters for events |
| `pkg/webhook` | Webhook server and admission handlers |
| `pkg/envtest` | Testing utilities for integration tests |
| `pkg/log` | Logging interfaces and implementations |
| `pkg/metrics` | Metrics collection and serving |
| `pkg/scheme` | Scheme utilities for type registration |
| `pkg/leaderelection` | Leader election support |

## Key Design Principles

### 1. Level-Based Reconciliation
Controllers reconcile based on the current state, not individual events. This makes controllers resilient to missed events and ensures eventual consistency.

### 2. Shared Dependencies
The Manager provides shared caches and clients to all controllers, reducing memory usage and API server load.

### 3. Declarative Configuration
The Builder pattern allows controllers to be configured declaratively, making the code more readable and maintainable.

### 4. Separation of Concerns
- **Source**: Where events come from
- **Handler**: How to transform events into reconcile requests
- **Predicate**: Which events to process
- **Reconciler**: What to do with the request

### 5. Testability
The framework provides testing utilities (`envtest`, fake clients) to facilitate unit and integration testing.

## Common Usage Pattern

```go
// 1. Create a manager
mgr, err := ctrl.NewManager(ctrl.GetConfigOrDie(), ctrl.Options{})

// 2. Define a reconciler
type MyReconciler struct {
    client.Client
    Scheme *runtime.Scheme
}

func (r *MyReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // Business logic here
    return ctrl.Result{}, nil
}

// 3. Build and register the controller
err = ctrl.NewControllerManagedBy(mgr).
    For(&myv1.MyResource{}).
    Owns(&corev1.Pod{}).
    Complete(&MyReconciler{
        Client: mgr.GetClient(),
        Scheme: mgr.GetScheme(),
    })

// 4. Start the manager
if err := mgr.Start(ctrl.SetupSignalHandler()); err != nil {
    // Handle error
}
```

## Advanced Features

### Leader Election
Controllers can be configured to run in a leader-elected mode, ensuring only one instance is active at a time.

### Priority Queues
Controllers support priority queues for processing high-priority items first.

### Field Indexing
Caches support field indexing for efficient lookups based on object fields.

### Namespace Filtering
Caches can be configured to watch specific namespaces, reducing memory usage.

### Webhook Support
The framework includes a webhook server for implementing admission and conversion webhooks.

### Metrics and Observability
Built-in Prometheus metrics for controller performance and health monitoring.

## Next Steps

For detailed information about each package, refer to the individual package documentation:

- [Manager Package](/docs/01-manager/)
- [Controller Package](/docs/02-controller/)
- [Reconciler Package](/docs/03-reconcile/)
- [Builder Package](/docs/04-builder/)
- [Client Package](/docs/05-client/)
- [Cache Package](/docs/06-cache/)
- [Source Package](/docs/07-source/)
- [Handler Package](/docs/08-handler/)
- [Predicate Package](/docs/09-predicate/)
- [Webhook Package](/docs/10-webhook/)
- [Additional Packages](/docs/11-additional-packages/)
