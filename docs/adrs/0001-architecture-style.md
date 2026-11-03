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

Use a small number of business services, with separate API and worker processes.

- Separate services allow independent resource allocation and scaling for workloads such as job browsing, application submission and reporting.
- Separate worker processes keep background processing from consuming API capacity.
- Keep related business rules and data within one service to maintain consistency and reduce calls between services.
- Keep the number of services small to limit deployment and maintenance work for a single owner.

## Consequences

Services add deployments and network dependencies. Separate services do not guarantee isolation.
Test overload and failures in services and shared infrastructure. Apply resource limits within each service so one organization cannot exhaust capacity needed by others.

Next: [Service boundaries](0002-service-boundaries.md).
