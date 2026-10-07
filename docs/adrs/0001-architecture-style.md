# ADR 0001: Architecture Style

Status: Proposed

## Purpose

Answers: **Which architecture style fits SmartHire's requirements, and why?**

## 1. Compare the Options

| Style | Structure | Main Tradeoff |
| --- | --- | --- |
| Monolith | One application contains the core capabilities. | Simple deployment; capabilities share application resources. |
| Modular monolith | One application contains separate business modules. | Clear code boundaries; modules still share application resources. |
| Microservices | Separate services own business responsibilities and data. | Separate resources; more deployments and communication. |

Every option can use API replicas and background workers. Replicas are additional instances of the same application.

## 2. Apply the Requirements

| Requirement or Constraint | Effect on the Choice |
| --- | --- |
| One owner operates the system. | Fewer deployments favor a monolith or modular monolith. |
| Related updates must stay consistent. | Keep responsibilities that enforce the same rule together. Local changes need less coordination. |
| Capabilities must handle different loads. | Separate services permit separate resource allocation. |
| One overloaded capability must not disrupt others. | Separate runtimes can improve isolation. Code modules alone do not provide it. |
| One overloaded tenant must not disrupt others. | Every style needs controls within each shared capability. Service separation alone does not isolate tenants. |
| Long tasks must not block users. | Every style can use background workers. This requirement alone does not select microservices. |

Shared identity and access controls apply to every option. Independent releases have less weight with one owner.

Richardson calls forces that favor separation **dark energy**. Forces that favor grouping are **dark matter**.

For SmartHire, separate scaling and failure isolation favor separation. Consistent updates, fewer interactions and simple operation favor grouping.

## 3. Proposed Choice

Use a small number of services with clear business responsibilities. Use separate workers for background tasks.

- Keep responsibilities that enforce the same business rule together.
- Separate capabilities when separate resources provide clear value.
- Share account and organization access rules across actors.

## 4. Costs and Limits

Services add deployment and communication work. Dependencies and shared infrastructure can still spread failures.

A modular monolith remains an alternative if it can meet the isolation requirements more simply. Capacity and availability need testing.

Next: [ADR 0002 — Service Boundaries](0002-service-boundaries.md).
