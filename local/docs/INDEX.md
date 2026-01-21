# Controller-Runtime Documentation Index

## Overview

This documentation provides a comprehensive guide to the Kubernetes controller-runtime project. The documentation is organized into 13 files covering all major aspects of the framework.

**Total Documentation**: ~7,600 lines across 13 markdown files

## Documentation Files

### Getting Started

1. **[README.md](./README.md)** (362 lines)
   - Quick start guide
   - Basic examples
   - Key concepts overview
   - Common use cases
   - Troubleshooting tips

2. **[00-overview.md](./00-overview.md)** (303 lines)
   - High-level architecture
   - Core components
   - Design principles
   - Event flow diagrams
   - Package organization

### Core Components

3. **[01-manager.md](./01-manager.md)** (573 lines)
   - Manager interface and implementation
   - Lifecycle management
   - Leader election
   - Health checks
   - Metrics server
   - Runnable interface

4. **[02-controller.md](./02-controller.md)** (672 lines)
   - Controller interface
   - Work queue management
   - Concurrency control
   - Rate limiting
   - Error handling
   - Controller utilities

5. **[03-reconcile.md](./03-reconcile.md)** (653 lines)
   - Reconciler interface
   - Reconciliation patterns
   - Request and Result types
   - Error handling strategies
   - Common patterns
   - Best practices

6. **[04-builder.md](./04-builder.md)** (584 lines)
   - Builder pattern
   - For/Owns/Watches methods
   - Controller configuration
   - Webhook builder
   - Options and predicates

### Data Access

7. **[05-client.md](./05-client.md)** (676 lines)
   - Client interface
   - Reader and Writer operations
   - Status subresource
   - Patch operations
   - Field indexing
   - Client types (split, direct, fake)

8. **[06-cache.md](./06-cache.md)** (670 lines)
   - Cache interface
   - Informers
   - Field indexing
   - Namespace filtering
   - Label/field selectors
   - Transform functions
   - Cache lifecycle

### Event Processing

9. **[07-source.md](./07-source.md)** (648 lines)
   - Source interface
   - Kind source (Kubernetes resources)
   - Channel source (external events)
   - Custom sources
   - Source lifecycle

10. **[08-handler.md](./08-handler.md)** (577 lines)
    - EventHandler interface
    - EnqueueRequestForObject
    - EnqueueRequestForOwner
    - EnqueueRequestsFromMapFunc
    - Custom handlers
    - Mapping patterns

11. **[09-predicate.md](./09-predicate.md)** (582 lines)
    - Predicate interface
    - Built-in predicates
    - Custom predicates
    - Predicate combinators (And/Or/Not)
    - Filtering patterns
    - Performance considerations

### Advanced Features

12. **[10-webhook.md](./10-webhook.md)** (663 lines)
    - Webhook server
    - Admission webhooks (mutating/validating)
    - Defaulter interface
    - Validator interface
    - Conversion webhooks
    - Webhook configuration

13. **[11-additional-packages.md](./11-additional-packages.md)** (623 lines)
    - envtest (integration testing)
    - log (structured logging)
    - metrics (Prometheus metrics)
    - scheme (type registration)
    - leaderelection
    - healthz (health checks)
    - finalizer utilities
    - event types
    - cluster interface
    - recorder (event recording)

## Documentation Statistics

- **Total Files**: 13 markdown files
- **Total Lines**: ~7,600 lines
- **Total Size**: ~170 KB
- **Diagrams**: 40+ Mermaid diagrams
- **Code Examples**: 200+ code examples
- **Patterns**: 50+ common patterns documented

## Documentation Features

### Comprehensive Coverage

- ✅ All major packages documented
- ✅ Architecture diagrams with Mermaid
- ✅ Real-world code examples
- ✅ Common patterns and anti-patterns
- ✅ Best practices and pitfalls
- ✅ Performance considerations
- ✅ Testing strategies

### Visual Documentation

- **Architecture Diagrams**: High-level system architecture
- **Flow Diagrams**: Event flow, reconciliation flow, lifecycle
- **Sequence Diagrams**: Component interactions
- **State Diagrams**: State transitions
- **Graph Diagrams**: Relationships and dependencies

### Practical Examples

- **Basic Examples**: Simple, straightforward usage
- **Advanced Examples**: Complex scenarios and patterns
- **Anti-Patterns**: What not to do and why
- **Performance Tips**: Optimization strategies
- **Testing Examples**: Unit and integration tests

## How to Use This Documentation

### For Beginners

1. Start with [README.md](./README.md) for quick start
2. Read [00-overview.md](./00-overview.md) for architecture understanding
3. Follow the [01-manager.md](./01-manager.md) → [02-controller.md](./02-controller.md) → [03-reconcile.md](./03-reconcile.md) path
4. Study examples in each document

### For Intermediate Users

1. Review specific packages you're working with
2. Study the patterns and best practices sections
3. Check common pitfalls to avoid mistakes
4. Explore advanced features in later chapters

### For Advanced Users

1. Deep dive into specific packages
2. Study performance considerations
3. Review advanced patterns
4. Explore custom implementations

### For Troubleshooting

1. Check the troubleshooting section in README.md
2. Review common pitfalls in relevant package docs
3. Study error handling patterns
4. Check performance considerations

## Key Concepts Covered

### Architecture
- Manager-Controller-Reconciler pattern
- Event-driven architecture
- Shared dependencies
- Leader election
- Graceful shutdown

### Reconciliation
- Level-based reconciliation
- Idempotent operations
- Error handling and retry
- Finalizers for cleanup
- Status updates

### Event Processing
- Sources generate events
- Handlers transform events to requests
- Predicates filter events
- Queue manages requests
- Workers process reconciliations

### Data Access
- Split client (cache + API)
- Direct API access
- Field indexing
- Namespace filtering
- Transform functions

### Testing
- Fake client for unit tests
- envtest for integration tests
- Test patterns and examples

## Cross-References

Each document includes cross-references to related packages:

- Manager → Controller, Cache, Client, Webhook
- Controller → Reconciler, Source, Handler, Predicate
- Builder → Controller, Source, Handler, Predicate
- Client → Cache, Manager
- Cache → Client, Manager
- Source → Handler, Predicate
- Handler → Source, Predicate
- Webhook → Manager, Builder

## Contributing

To contribute to this documentation:

1. Follow the existing structure and style
2. Include code examples for all concepts
3. Add Mermaid diagrams where helpful
4. Document both what to do and what not to do
5. Include performance considerations
6. Add cross-references to related packages

## Maintenance

This documentation is based on controller-runtime version 0.22 (Kubernetes 0.35).

To update:
1. Review changes in new controller-runtime versions
2. Update code examples if APIs change
3. Add new features and packages
4. Update diagrams if architecture changes
5. Keep cross-references accurate

## Additional Resources

### Official Documentation
- [Kubebuilder Book](https://book.kubebuilder.io/)
- [Controller-Runtime GoDoc](https://pkg.go.dev/sigs.k8s.io/controller-runtime)
- [GitHub Repository](https://github.com/kubernetes-sigs/controller-runtime)

### Examples
- [Built-in Resources Example](../../examples/builtins/)
- [CRD Example](../../examples/crd/)
- [Typed Controller Example](../../examples/typed/)

### Community
- [Kubernetes Slack #controller-runtime](https://kubernetes.slack.com/archives/C02MRBMN00Z)
- [Kubebuilder Google Group](https://groups.google.com/forum/#!forum/kubebuilder)

## License

This documentation follows the same Apache License 2.0 as the controller-runtime project.

---

**Generated**: January 2026  
**Version**: Based on controller-runtime v0.22 (Kubernetes v0.35)  
**Format**: Markdown with Mermaid diagrams  
**Purpose**: Comprehensive technical documentation for controller-runtime
