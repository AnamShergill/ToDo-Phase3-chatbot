<!-- SYNC IMPACT REPORT
Version change: N/A (initial version) → 1.0.0
Modified principles: N/A
Added sections: Core Principles for hackathon-todo project
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->
# hackathon-todo Constitution

## Core Principles

### I. Spec-Driven Development
All features must be fully specified before implementation using Spec-Kit Plus. Every API endpoint, database schema, and user interface element must be accurately described in structured specifications before any code is written.

### II. Full-Stack Integration
The application must maintain seamless integration between frontend (Next.js) and backend (FastAPI) components. All API responses, authentication flows, and user interactions must work end-to-end with proper error handling across the stack.

### III. Security-First Architecture
Security must be implemented at every layer: JWT authentication for API access, proper user data isolation, secure password handling, and protection against common vulnerabilities. Better Auth must be used for authentication flows.

### IV. Test-First (NON-NEGOTIABLE)
TDD is mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced. All components must have comprehensive test coverage before deployment.

### V. Multi-User Data Isolation
The system must ensure proper separation of user data at the database and API levels. Each user's tasks and data must be completely isolated from other users, with no possibility of cross-user data access.

### VI. Responsive Design & Accessibility
All user interfaces must be responsive across all device sizes and meet accessibility standards. The UI/UX must follow modern design principles with consistent color schemes, typography, and spacing.

## Technology Stack Requirements

The project must adhere to the specified technology stack: Frontend (Next.js 16+, TypeScript, Tailwind CSS), Backend (FastAPI, SQLModel), Database (Neon Serverless PostgreSQL), and Authentication (Better Auth + JWT). Deviations require explicit approval and architectural review.

## Development Workflow

All development must follow the Agentic Dev Stack approach with Spec-Driven Development using Spec-Kit Plus. Each phase (phase1-console, phase2-web, phase3-chatbot) must be completed before moving to the next, with proper validation at each stage. Code reviews must verify compliance with all constitutional principles.

## Governance

This constitution supersedes all other practices and guidelines in the project. All pull requests and code reviews must verify compliance with these principles. Any amendments to this constitution must be documented with proper approval and migration plans. All agents must follow the defined roles and responsibilities: Product Spec Architect (lead specs), UI/UX Designer (theme and components), Auth Security Specialist (authentication and security), Backend Engineer (API and DB), Frontend Engineer (client and UI/UX), QA Integration Agent (validation and testing).

**Version**: 1.0.0 | **Ratified**: 2026-01-09 | **Last Amended**: 2026-01-09