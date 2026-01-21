---
title: "Manager"
weight: 1
---


## Overview

The `pkg/manager` package provides the Manager interface and implementation, which is the central component responsible for orchestrating all controllers, webhooks, and shared dependencies in a controller-runtime application.

## Package Location

```
pkg/manager/
├── manager.go          # Manager interface and implementation
├── doc.go              # Package documentation
├── runnable_group.go   # Runnable group management
├── internal/           # Internal implementation details
└── signals/            # Signal handling utilities
```

## Core Concepts

### Manager Interface

The Manager is the main entry point for controller-runtime applications. It provides:

<div class="mermaid-diagram">
<img src="/images/diagrams/diagram-159a145d07cd.svg" alt="Diagram" />
</div>


## Manager Interface Definition

The Manager interface extends the `cluster.Cluster` interface and provides the following methods:

### Core Methods

```go
type Manager interface {
    cluster.Cluster

    // Add registers a Runnable to be started by the manager
    Add(Runnable) error

    // Elected returns a channel that is closed when the manager is elected leader
    Elected() <-chan struct{}

    // Start starts all registered Controllers and blocks until the context is cancelled
    Start(ctx context.Context) error

    // GetWebhookServer returns the webhook server
    GetWebhookServer() webhook.Server

    // GetLogger returns the manager's logger
    GetLogger() logr.Logger

    // GetControllerOptions returns controller global configuration options
    GetControllerOptions() config.Controller

    // AddMetricsServerExtraHandler adds extra handlers to the metrics server
    AddMetricsServerExtraHandler(path string, handler http.Handler) error

    // AddHealthzCheck adds a healthz checker
    AddHealthzCheck(name string, check healthz.Checker) error

    // AddReadyzCheck adds a readyz checker
    AddReadyzCheck(name string, check healthz.Checker) error

    // GetConverterRegistry returns the conversion webhook registry
    GetConverterRegistry() conversion.Registry
}
```

## Manager Options

The Manager is configured using the `Options` struct:

### Key Configuration Options

```go
type Options struct {
    // Scheme for mapping objects to GroupVersionKinds
    Scheme *runtime.Scheme

    // MapperProvider for REST mapping
    MapperProvider func(c *rest.Config, httpClient *http.Client) (meta.RESTMapper, error)

    // Cache configuration
    Cache cache.Options

    // Client configuration
    Client client.Options

    // Logger for the manager
    Logger logr.Logger

    // Leader Election settings
    LeaderElection bool
    LeaderElectionResourceLock string
    LeaderElectionNamespace string
    LeaderElectionID string
    LeaderElectionConfig *rest.Config

    // Metrics server configuration
    Metrics metricsserver.Options

    // Health probe configuration
    HealthProbeBindAddress string

    // Webhook server configuration
    WebhookServer webhook.Server

    // Controller configuration
    Controller config.Controller

    // Graceful shutdown timeout
    GracefulShutdownTimeout *time.Duration
}
```

## Creating a Manager

### Basic Manager Creation

```go
import (
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/manager"
)

// Create a manager with default options
mgr, err := manager.New(ctrl.GetConfigOrDie(), manager.Options{})
if err != nil {
    // Handle error
}

// Or using the convenience function
mgr, err := ctrl.NewManager(ctrl.GetConfigOrDie(), ctrl.Options{})
```

### Manager with Custom Configuration

```go
mgr, err := ctrl.NewManager(cfg, ctrl.Options{
    Scheme: scheme,
    Metrics: metricsserver.Options{
        BindAddress: ":8080",
    },
    HealthProbeBindAddress: ":8081",
    LeaderElection: true,
    LeaderElectionID: "my-controller-lock",
    LeaderElectionNamespace: "default",
    Cache: cache.Options{
        DefaultNamespaces: map[string]cache.Config{
            "my-namespace": {},
        },
    },
    Logger: ctrl.Log.WithName("manager"),
})
```

## Runnable Interface

The Manager starts and manages Runnables. A Runnable is anything that can be started and stopped:

```go
type Runnable interface {
    Start(context.Context) error
}
```

### Runnable Types

<div class="mermaid-diagram">
<img src="/images/diagrams/diagram-72643b7e3774.svg" alt="Diagram" />
</div>


### LeaderElectionRunnable Interface

Runnables can implement this interface to control leader election behavior:

```go
type LeaderElectionRunnable interface {
    NeedLeaderElection() bool
}
```

## Manager Lifecycle

### Startup Sequence

<div class="mermaid-diagram">
<img src="/images/diagrams/diagram-c7764cd53dbd.svg" alt="Diagram" />
</div>


### Graceful Shutdown

The Manager handles graceful shutdown automatically:

1. Receives shutdown signal (SIGTERM, SIGINT)
2. Cancels the context passed to all Runnables
3. Waits for all Runnables to complete (up to GracefulShutdownTimeout)
4. Exits

```go
// Setup signal handler for graceful shutdown
ctx := ctrl.SetupSignalHandler()

// Start the manager (blocks until shutdown)
if err := mgr.Start(ctx); err != nil {
    log.Error(err, "problem running manager")
    os.Exit(1)
}
```

## Cluster Interface

The Manager implements the `cluster.Cluster` interface, providing access to shared resources:

```go
type Cluster interface {
    // GetScheme returns the scheme
    GetScheme() *runtime.Scheme

    // GetConfig returns the REST config
    GetConfig() *rest.Config

    // GetClient returns the client
    GetClient() client.Client

    // GetFieldIndexer returns the field indexer
    GetFieldIndexer() client.FieldIndexer

    // GetCache returns the cache
    GetCache() cache.Cache

    // GetEventRecorderFor returns an event recorder
    GetEventRecorderFor(name string) record.EventRecorder

    // GetRESTMapper returns the REST mapper
    GetRESTMapper() meta.RESTMapper

    // GetAPIReader returns a reader that reads directly from the API server
    GetAPIReader() client.Reader

    // Start starts the cluster
    Start(ctx context.Context) error
}
```

## Leader Election

### Configuration

```go
mgr, err := ctrl.NewManager(cfg, ctrl.Options{
    LeaderElection: true,
    LeaderElectionID: "my-controller-lock",
    LeaderElectionNamespace: "kube-system",
    LeaderElectionResourceLock: "leases", // Default
    LeaseDuration: ptr.To(15 * time.Second),
    RenewDeadline: ptr.To(10 * time.Second),
    RetryPeriod: ptr.To(2 * time.Second),
})
```

### Leader Election Flow

<div class="mermaid-diagram">
<img src="/images/diagrams/diagram-f7b0e230a29c.svg" alt="Diagram" />
</div>


### Checking Leader Status

```go
// Wait for leader election
<-mgr.Elected()

// Now we are the leader
log.Info("Became leader")
```

## Health and Readiness Checks

### Adding Health Checks

```go
import "sigs.k8s.io/controller-runtime/pkg/healthz"

// Add a simple ping check
err = mgr.AddHealthzCheck("ping", healthz.Ping)

// Add a custom check
err = mgr.AddHealthzCheck("custom", func(req *http.Request) error {
    // Custom health check logic
    if !isHealthy() {
        return fmt.Errorf("not healthy")
    }
    return nil
})

// Add readiness checks
err = mgr.AddReadyzCheck("cache", func(req *http.Request) error {
    if !mgr.GetCache().WaitForCacheSync(req.Context()) {
        return fmt.Errorf("cache not synced")
    }
    return nil
})
```

### Health Check Endpoints

When `HealthProbeBindAddress` is set, the manager exposes:
- `/healthz` - Liveness probe endpoint
- `/readyz` - Readiness probe endpoint

## Metrics Server

### Configuration

```go
import metricsserver "sigs.k8s.io/controller-runtime/pkg/metrics/server"

mgr, err := ctrl.NewManager(cfg, ctrl.Options{
    Metrics: metricsserver.Options{
        BindAddress: ":8080",
        SecureServing: true,
        CertDir: "/tmp/k8s-metrics-server/serving-certs",
    },
})
```

### Adding Custom Metrics Handlers

```go
// Add pprof handlers
err = mgr.AddMetricsServerExtraHandler("/debug/pprof/", http.DefaultServeMux)
```

## Webhook Server

### Accessing the Webhook Server

```go
// Get the webhook server
webhookServer := mgr.GetWebhookServer()

// Register a webhook
webhookServer.Register("/mutate-v1-pod", &webhook.Admission{
    Handler: &podMutator{},
})
```

## Event Recorders

The Manager provides event recorders for publishing Kubernetes events:

```go
// Get an event recorder
recorder := mgr.GetEventRecorderFor("my-controller")

// Record an event
recorder.Event(obj, corev1.EventTypeNormal, "Created", "Created pod successfully")

// Record an event with annotations
recorder.AnnotatedEventf(obj, annotations, corev1.EventTypeWarning, "Failed", "Failed to create pod: %v", err)
```

## Custom Runnables

### Adding Custom Runnables

```go
type MyRunnable struct {
    // fields
}

func (r *MyRunnable) Start(ctx context.Context) error {
    // Start logic
    <-ctx.Done()
    // Cleanup logic
    return nil
}

func (r *MyRunnable) NeedLeaderElection() bool {
    return true // Run only when elected leader
}

// Add to manager
err = mgr.Add(&MyRunnable{})
```

### Runnable Groups

Runnables are organized into groups:

<div class="mermaid-diagram">
<img src="/images/diagrams/diagram-f88840eff980.svg" alt="Diagram" />
</div>


## Best Practices

### 1. Single Manager Per Process

Create one Manager per process and register all controllers with it:

```go
mgr, err := ctrl.NewManager(cfg, ctrl.Options{})

// Register multiple controllers
ctrl.NewControllerManagedBy(mgr).For(&v1.Pod{}).Complete(reconciler1)
ctrl.NewControllerManagedBy(mgr).For(&v1.Service{}).Complete(reconciler2)

mgr.Start(ctx)
```

### 2. Use Leader Election for HA

Enable leader election for high availability:

```go
mgr, err := ctrl.NewManager(cfg, ctrl.Options{
    LeaderElection: true,
    LeaderElectionID: "unique-lock-name",
})
```

### 3. Configure Health Checks

Always configure health and readiness checks:

```go
mgr.AddHealthzCheck("ping", healthz.Ping)
mgr.AddReadyzCheck("cache", mgr.GetCache().WaitForCacheSync)
```

### 4. Handle Signals Properly

Use the provided signal handler:

```go
ctx := ctrl.SetupSignalHandler()
mgr.Start(ctx)
```

### 5. Configure Graceful Shutdown

Set an appropriate graceful shutdown timeout:

```go
mgr, err := ctrl.NewManager(cfg, ctrl.Options{
    GracefulShutdownTimeout: ptr.To(30 * time.Second),
})
```

## Common Patterns

### Multi-Cluster Manager

```go
// Create managers for multiple clusters
primaryMgr, err := ctrl.NewManager(primaryConfig, ctrl.Options{})
secondaryMgr, err := ctrl.NewManager(secondaryConfig, ctrl.Options{})

// Start both managers
go primaryMgr.Start(ctx)
go secondaryMgr.Start(ctx)
```

### Namespace-Scoped Manager

```go
mgr, err := ctrl.NewManager(cfg, ctrl.Options{
    Cache: cache.Options{
        DefaultNamespaces: map[string]cache.Config{
            "my-namespace": {},
        },
    },
})
```

## Related Packages

- [Controller Package](/docs/02-controller/) - Controllers managed by the Manager
- [Cache Package](/docs/06-cache/) - Cache provided by the Manager
- [Client Package](/docs/05-client/) - Client provided by the Manager
- [Webhook Package](/docs/10-webhook/) - Webhooks managed by the Manager
