# ADR 0001: Architecture Style

Status: Proposed

## Options

| Architecture | Structure |
| --- | --- |
| Monolith | Core capabilities run as one application. Internal structure may be simple or layered. |
| Modular monolith | One application organized into business modules with clear interfaces. |
| Microservices | Independently deployable services, each responsible for its own business data. |

All three can run multiple API instances and separate background workers.

## Principles Behind the Choice

| Principle | Effect on the Choice |
| --- | --- |
| Simple deployment and operation | One owner benefits from fewer deployments. This favors a monolith or modular monolith. |
| Clear business responsibilities | Explicit capability boundaries favor a modular monolith or services organized by business responsibility. |
| Consistent updates | Keep related changes together. Local transactions are simpler than coordinating changes across services. |
| Efficient collaboration | Keep frequently interacting responsibilities together to reduce network calls and coordinated releases. |
| Independent scaling | Separate services allow capacity to grow for one capability without replicating the whole application. |
| Overload and failure isolation | Separate runtimes and resource budgets can protect unrelated capabilities. Module boundaries alone provide limited runtime isolation. |
| Independent releases | Services can change separately when their contracts allow it. This has less weight with one owner. |
| Common identity and tenant isolation | Every option needs shared account rules and organization access controls. Microservices do not automatically isolate tenants. |
| Background processing | Every option can use workers for scoring, notifications and reporting. Background work alone does not require another service. |

Independent scaling, isolation and releases are **dark-energy forces** that encourage separation. Consistent updates and simple interactions are **dark-matter forces** that encourage grouping.

## Proposed Direction

Use **a small number of services organized around business responsibilities**, with separate background workers where needed.

SmartHire's scaling and overload-isolation needs favor services. A single owner and related hiring updates favor keeping the service count small.

- Group operations and data that must change together.
- Separate capabilities where independent capacity or failure isolation provides clear value.
- Keep account and membership management common to candidates and recruiters.

The cost is more deployment and communication work. Shared infrastructure and service dependencies still need protection. A modular monolith remains an alternative if it meets the same isolation needs more simply. Capacity and availability remain to be validated.
