# Todo Application Implementation Guide

## Overview

This guide provides implementation prompts for the Todo Full-Stack Web Application project, organized by phase and technology stack. Each prompt is designed to be used with Claude Code to generate the required code following the specifications.

## Implementation Instructions for Claude Code

### Before Starting Implementation

1. **Read all CLAUDE.md files**:
   - Root CLAUDE.md: Contains project-wide rules and constraints
   - Backend CLAUDE.md (if exists): Backend-specific rules
   - Frontend CLAUDE.md (if exists): Frontend-specific rules

2. **Follow all Spec-Kit references**:
   - Use `@specs/features/task-crud.md` for task CRUD requirements
   - Use `@specs/features/authentication.md` for authentication requirements
   - Use `@specs/api/rest-endpoints.md` for API endpoint specifications
   - Use `@specs/database/schema.md` for database schema requirements
   - Use `@specs/ui/components.md` for UI component specifications
   - Use `@specs/ui/pages.md` for UI page specifications

3. **Maintain quality standards**:
   - Ensure all code is production-ready
   - Follow security best practices
   - Implement proper error handling
   - Use appropriate logging
   - Write clean, maintainable code

### Phase 1: Backend Foundation

Execute the prompts in `implementation/prompts/phase1-backend.md` in order:

1. Implement database schema and models
2. Create FastAPI CRUD routes
3. Implement task CRUD features

### Phase 2: Full-Stack Implementation

Execute the following prompts in parallel where possible:

1. Backend authentication: `implementation/prompts/phase2-backend.md`
2. Frontend components: `implementation/prompts/phase2-frontend.md`

### Phase 3: Optional Features

Execute the prompts in `implementation/prompts/phase3-optional.md` if implementing the chatbot feature.

## Technology Stack Requirements

### Backend (Python/FastAPI)
- Use FastAPI for the web framework
- Use SQLModel for database models and ORM
- Use Neon PostgreSQL as the database
- Implement JWT-based authentication
- Follow REST API design principles
- Include proper request validation and error handling

### Frontend (Next.js/TypeScript/Tailwind CSS)
- Use Next.js 16+ with App Router
- Use TypeScript for type safety
- Use Tailwind CSS for styling
- Implement responsive design
- Follow accessibility best practices
- Create reusable components
- Connect to backend API endpoints

### Authentication (Better Auth + JWT)
- Use Better Auth for user management
- Implement JWT token issuance and verification
- Ensure proper user data isolation
- Implement secure password handling
- Add rate limiting for authentication endpoints

## Quality Assurance

### Code Quality
- Write clean, well-documented code
- Follow language-specific best practices
- Implement proper error handling
- Include appropriate logging
- Write unit and integration tests

### Security
- Implement proper authentication and authorization
- Sanitize all user inputs
- Protect against common vulnerabilities (XSS, CSRF, SQL injection)
- Use secure password hashing
- Implement rate limiting where appropriate

### Performance
- Optimize database queries with proper indexing
- Implement caching where appropriate
- Minimize network requests
- Optimize assets and bundles
- Implement lazy loading where appropriate

## Cross-Spec References

All implementations must follow these specifications:
- @specs/overview.md - Overall project architecture
- @specs/features/task-crud.md - Task management features
- @specs/features/authentication.md - Authentication system
- @specs/api/rest-endpoints.md - API specifications
- @specs/database/schema.md - Database schema
- @specs/ui/components.md - UI components
- @specs/ui/pages.md - UI pages