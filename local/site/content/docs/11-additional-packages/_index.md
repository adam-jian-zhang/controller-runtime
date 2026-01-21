---
title: "Additional Packages"
weight: 11
---


## Overview

This document covers additional packages in controller-runtime that provide supporting functionality for controllers, webhooks, and testing.

## Package Overview

| Package | Purpose |
|---------|---------|
| `pkg/envtest` | Integration testing with real API server |
| `pkg/log` | Structured logging interfaces |
| `pkg/metrics` | Prometheus metrics |
| `pkg/scheme` | Scheme utilities |
| `pkg/leaderelection` | Leader election support |
| `pkg/healthz` | Health check handlers |
| `pkg/finalizer` | Finalizer utilities |
| `pkg/event` | Event types |
| `pkg/cluster` | Cluster interface |
| `pkg/recorder` | Event recorder |

## envtest Package

### Overview

The `envtest` package provides a test environment with a real Kubernetes API server and etcd for integration testing.

### Location

```
pkg/envtest/
├── envtest.go          # Test environment
├── server.go           # API server management
├── komega/             # Gomega matchers for Kubernetes
└── testdata/           # Test data and CRDs
```

### Basic Usage

```go
import (
    "testing"
    "sigs.k8s.io/controller-runtime/pkg/envtest"
)

func TestController(t *testing.T) {
    // Create test environment
    testEnv := &envtest.Environment{
        CRDDirectoryPaths: []string{"./config/crd"},
        ErrorIfCRDPathMissing: true,
    }
    
    // Start the environment
    cfg, err := testEnv.Start()
    if err != nil {
        t.Fatal(err)
    }
    defer testEnv.Stop()
    
    // Create client
    k8sClient, err := client.New(cfg, client.Options{Scheme: scheme})
    if err != nil {
        t.Fatal(err)
    }
    
    // Run tests
    // ...
}
```

### With Ginkgo

```go
import (
    . "github.com/onsi/ginkgo/v2"
    . "github.com/onsi/gomega"
    "sigs.k8s.io/controller-runtime/pkg/envtest"
)

var (
    testEnv   *envtest.Environment
    k8sClient client.Client
)

var _ = BeforeSuite(func() {
    testEnv = &envtest.Environment{
        CRDDirectoryPaths: []string{"./config/crd"},
    }
    
    cfg, err := testEnv.Start()
    Expect(err).NotTo(HaveOccurred())
    
    k8sClient, err = client.New(cfg, client.Options{Scheme: scheme})
    Expect(err).NotTo(HaveOccurred())
})

var _ = AfterSuite(func() {
    Expect(testEnv.Stop()).To(Succeed())
})
```

### Environment Options

```go
testEnv := &envtest.Environment{
    // CRD paths
    CRDDirectoryPaths: []string{"./config/crd"},
    ErrorIfCRDPathMissing: true,
    
    // Webhook configuration
    WebhookInstallOptions: envtest.WebhookInstallOptions{
        Paths: []string{"./config/webhook"},
    },
    
    // Binary assets path
    BinaryAssetsDirectory: "./testbin/bin",
    
    // Attach control plane output
    AttachControlPlaneOutput: true,
}
```

## log Package

### Overview

The `log` package provides structured logging interfaces using logr.

### Location

```
pkg/log/
├── log.go              # Log interface
├── deleg.go            # Delegating logger
├── null.go             # Null logger
├── warning_handler.go  # Warning handler
└── zap/                # Zap logger implementation
```

### Basic Usage

```go
import (
    "sigs.k8s.io/controller-runtime/pkg/log"
    "sigs.k8s.io/controller-runtime/pkg/log/zap"
)

// Set global logger
ctrl.SetLogger(zap.New())

// Get logger from context
func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := log.FromContext(ctx)
    log.Info("Reconciling", "request", req)
    return ctrl.Result{}, nil
}

// Create logger with values
log := ctrl.Log.WithName("controller").WithValues("namespace", "default")
log.Info("Starting controller")
```

### Zap Logger

```go
import "sigs.k8s.io/controller-runtime/pkg/log/zap"

// Development mode (human-readable)
logger := zap.New(zap.UseDevMode(true))

// Production mode (JSON)
logger := zap.New(zap.UseDevMode(false))

// With options
logger := zap.New(
    zap.UseDevMode(true),
    zap.Level(zapcore.DebugLevel),
    zap.StacktraceLevel(zapcore.ErrorLevel),
)

ctrl.SetLogger(logger)
```

## metrics Package

### Overview

The `metrics` package provides Prometheus metrics integration.

### Location

```
pkg/metrics/
├── registry.go         # Metrics registry
├── client_go_adapter.go # Client-go metrics
├── server/             # Metrics server
└── filters/            # Metrics filters
```

### Built-in Metrics

Controller-runtime automatically exports:

- `controller_runtime_reconcile_total` - Total reconciliations
- `controller_runtime_reconcile_errors_total` - Total errors
- `controller_runtime_reconcile_time_seconds` - Reconciliation duration
- `workqueue_depth` - Work queue depth
- `workqueue_adds_total` - Total adds to queue
- `workqueue_retries_total` - Total retries

### Custom Metrics

```go
import (
    "github.com/prometheus/client_golang/prometheus"
    "sigs.k8s.io/controller-runtime/pkg/metrics"
)

var (
    myMetric = prometheus.NewCounter(prometheus.CounterOpts{
        Name: "my_controller_operations_total",
        Help: "Total number of operations",
    })
)

func init() {
    // Register custom metric
    metrics.Registry.MustRegister(myMetric)
}

func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    myMetric.Inc()
    return ctrl.Result{}, nil
}
```

### Metrics Server

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

## scheme Package

### Overview

The `scheme` package provides utilities for working with runtime.Scheme.

### Location

```
pkg/scheme/
└── scheme.go           # Scheme utilities
```

### Basic Usage

```go
import (
    "k8s.io/apimachinery/pkg/runtime"
    clientgoscheme "k8s.io/client-go/kubernetes/scheme"
    "sigs.k8s.io/controller-runtime/pkg/scheme"
)

// Create a new scheme
scheme := runtime.NewScheme()

// Add built-in types
_ = clientgoscheme.AddToScheme(scheme)

// Add custom types
_ = myv1.AddToScheme(scheme)
```

## leaderelection Package

### Overview

The `leaderelection` package provides leader election support.

### Location

```
pkg/leaderelection/
├── leader_election.go  # Leader election interface
└── fake/               # Fake leader election for testing
```

### Basic Usage

Leader election is typically configured through the Manager:

```go
mgr, err := ctrl.NewManager(cfg, ctrl.Options{
    LeaderElection: true,
    LeaderElectionID: "my-controller-lock",
    LeaderElectionNamespace: "default",
    LeaderElectionResourceLock: "leases",
    LeaseDuration: ptr.To(15 * time.Second),
    RenewDeadline: ptr.To(10 * time.Second),
    RetryPeriod: ptr.To(2 * time.Second),
})

// Wait for leader election
<-mgr.Elected()
log.Info("Became leader")
```

## healthz Package

### Overview

The `healthz` package provides health check handlers.

### Location

```
pkg/healthz/
├── healthz.go          # Health check interface
└── doc.go              # Package documentation
```

### Basic Usage

```go
import "sigs.k8s.io/controller-runtime/pkg/healthz"

// Add health checks
err := mgr.AddHealthzCheck("ping", healthz.Ping)

// Add readiness checks
err = mgr.AddReadyzCheck("cache", func(req *http.Request) error {
    if !mgr.GetCache().WaitForCacheSync(req.Context()) {
        return fmt.Errorf("cache not synced")
    }
    return nil
})

// Custom health check
err = mgr.AddHealthzCheck("custom", func(req *http.Request) error {
    if !isHealthy() {
        return fmt.Errorf("not healthy")
    }
    return nil
})
```

### Health Check Endpoints

When `HealthProbeBindAddress` is set:

- `/healthz` - Liveness probe
- `/readyz` - Readiness probe

```go
mgr, err := ctrl.NewManager(cfg, ctrl.Options{
    HealthProbeBindAddress: ":8081",
})
```

## finalizer Package

### Overview

The `finalizer` package provides utilities for managing finalizers.

### Location

```
pkg/finalizer/
└── finalizers.go       # Finalizer utilities
```

### Basic Usage

```go
import (
    "sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
    "sigs.k8s.io/controller-runtime/pkg/finalizer"
)

const myFinalizer = "myresource.example.com/finalizer"

// Using controllerutil (recommended)
if obj.DeletionTimestamp.IsZero() {
    if !controllerutil.ContainsFinalizer(obj, myFinalizer) {
        controllerutil.AddFinalizer(obj, myFinalizer)
        return ctrl.Result{}, r.Update(ctx, obj)
    }
} else {
    if controllerutil.ContainsFinalizer(obj, myFinalizer) {
        // Cleanup
        if err := cleanup(); err != nil {
            return ctrl.Result{}, err
        }
        controllerutil.RemoveFinalizer(obj, myFinalizer)
        return ctrl.Result{}, r.Update(ctx, obj)
    }
}

// Using finalizer package
finalizers := finalizer.NewFinalizers()
if err := finalizers.Register(myFinalizer, &MyFinalizer{}); err != nil {
    return err
}
```

## event Package

### Overview

The `event` package defines event types used by sources and handlers.

### Location

```
pkg/event/
├── event.go            # Event types
└── doc.go              # Package documentation
```

### Event Types

```go
// CreateEvent is generated when an object is created
type CreateEvent struct {
    Object client.Object
}

// UpdateEvent is generated when an object is updated
type UpdateEvent struct {
    ObjectOld client.Object
    ObjectNew client.Object
}

// DeleteEvent is generated when an object is deleted
type DeleteEvent struct {
    Object client.Object
}

// GenericEvent is generated for synthetic events
type GenericEvent struct {
    Object client.Object
}
```

## cluster Package

### Overview

The `cluster` package defines the Cluster interface implemented by Manager.

### Location

```
pkg/cluster/
├── cluster.go          # Cluster interface
└── internal.go         # Internal implementation
```

### Cluster Interface

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
    
    // GetAPIReader returns a reader that reads from API server
    GetAPIReader() client.Reader
    
    // Start starts the cluster
    Start(ctx context.Context) error
}
```

## recorder Package

### Overview

The `recorder` package provides event recorder utilities.

### Location

```
pkg/recorder/
└── recorder.go         # Event recorder
```

### Basic Usage

```go
// Get event recorder from manager
recorder := mgr.GetEventRecorderFor("my-controller")

// Record normal event
recorder.Event(obj, corev1.EventTypeNormal, "Created", "Created pod successfully")

// Record warning event
recorder.Event(obj, corev1.EventTypeWarning, "Failed", "Failed to create pod")

// Record event with formatted message
recorder.Eventf(obj, corev1.EventTypeNormal, "Scaled", "Scaled to %d replicas", replicas)

// Record annotated event
annotations := map[string]string{
    "controller": "my-controller",
}
recorder.AnnotatedEventf(obj, annotations, corev1.EventTypeNormal, "Updated", "Updated successfully")
```

## Testing Utilities

### Fake Client

```go
import "sigs.k8s.io/controller-runtime/pkg/client/fake"

// Create fake client
fakeClient := fake.NewClientBuilder().
    WithScheme(scheme).
    WithObjects(&pod1, &pod2).
    WithStatusSubresource(&pod1).
    WithIndex(&corev1.Pod{}, "spec.nodeName", indexFunc).
    Build()

// Use like real client
err := fakeClient.Get(ctx, key, &pod)
err = fakeClient.Create(ctx, &pod)
err = fakeClient.Update(ctx, &pod)
```

### Fake Leader Election

```go
import "sigs.k8s.io/controller-runtime/pkg/leaderelection/fake"

// Create fake leader elector
fakeElector := &fake.LeaderElector{
    OnStartedLeading: func(ctx context.Context) {
        // Called when elected
    },
    OnStoppedLeading: func() {
        // Called when lost leadership
    },
}
```

## Best Practices

### 1. Use envtest for Integration Tests

```go
testEnv := &envtest.Environment{
    CRDDirectoryPaths: []string{"./config/crd"},
}
cfg, err := testEnv.Start()
defer testEnv.Stop()
```

### 2. Use Structured Logging

```go
log := log.FromContext(ctx)
log.Info("Processing", "resource", obj.Name, "namespace", obj.Namespace)
```

### 3. Export Custom Metrics

```go
metrics.Registry.MustRegister(myMetric)
```

### 4. Add Health Checks

```go
mgr.AddHealthzCheck("ping", healthz.Ping)
mgr.AddReadyzCheck("cache", cacheCheck)
```

### 5. Use Finalizers for Cleanup

```go
if !obj.DeletionTimestamp.IsZero() {
    if controllerutil.ContainsFinalizer(obj, myFinalizer) {
        // Cleanup
        controllerutil.RemoveFinalizer(obj, myFinalizer)
        return ctrl.Result{}, r.Update(ctx, obj)
    }
}
```

## Related Documentation

- [Manager Package](/docs/01-manager/) - Uses many of these packages
- [Controller Package](/docs/02-controller/) - Uses metrics and logging
- [Client Package](/docs/05-client/) - Uses scheme
- [Cache Package](/docs/06-cache/) - Uses logging
