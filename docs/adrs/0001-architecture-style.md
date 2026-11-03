# ADR 0001: Architecture Style

**Status:** Proposed

**Purpose:** Explain why SmartHire uses separate services.

## Options

| Style | Structure | Main Tradeoff |
| --- | --- | --- |
| Monolith | One application. | Simple deployment, but capabilities share runtime resources. |
| Modular monolith | One application with separate business modules. | Clear code boundaries, but modules still share runtime resources. |
| Microservices | Separate applications own business responsibilities and data. | Independent resource allocation, with more deployment and communication work. |

All three can use API replicas and background workers. Background work alone does not require microservices.

## Decision and Reasons

Propose a small number of business services, with separate API and worker runtimes.

| Force | Effect |
| --- | --- |
| Different workloads and overload containment | Favor separate runtimes and resource allocation. |
| Related changes must remain consistent | Favor keeping one business rule within one service. |
| One owner operates the system | Favor fewer deployments and fewer cross-service interactions. |

Richardson calls separation forces **dark energy** and grouping forces **dark matter**. Here, isolation favors separation; consistency and operating cost favor grouping.
Tenant isolation still requires controls within each shared service.

## Consequences

Services add operational work and network dependencies. Isolation must be tested, including failures in shared infrastructure.
A modular monolith remains an alternative if it meets the isolation requirements more simply.

Next: [Service boundaries](0002-service-boundaries.md).
