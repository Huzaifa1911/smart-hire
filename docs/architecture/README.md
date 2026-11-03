# Architecture Guide

Read the documents in this order. Each answers a different question.

| Step | Question | Document |
| --- | --- | --- |
| 1 | What must the system do? | [Problem statement](problem_statement.md) |
| 2 | Why use separate services? | [ADR 0001: Architecture style](../adrs/0001-architecture-style.md) |
| 3 | Who owns each responsibility and its data? | [ADR 0002: Service boundaries](../adrs/0002-service-boundaries.md) |
| 4 | How does each business process work? | [Workflows](workflows/README.md) |
| 5 | How do the runtime components fit together? | [High-level architecture](high_level_architecture.md) |

Business rules live in the problem statement. ADRs explain decisions. Workflows show steps and specific failure behavior. The architecture describes runtime components.

The architecture and ADRs are proposed. The repository contains service foundations, not the complete target system.
Database schemas, API contracts and detailed sequence diagrams will be defined as each workflow is implemented.

[ADR 0003: JWT authentication and authorization](../adrs/0003-authentication-and-sessions.md) defines the selected token approach, role checks and membership revocation.

The [concept documents](../concept/) are preserved source requirements.
