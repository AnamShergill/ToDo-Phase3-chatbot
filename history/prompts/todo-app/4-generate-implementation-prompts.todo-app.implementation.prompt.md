---
id: 4
title: generate-implementation-prompts
stage: implementation
date_iso: 2026-01-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-app
branch: master
user: Bruno
command: sp.implement
labels:
  - implementation
  - todo-app
  - prompts
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - implementation/prompts/phase1-backend.md
  - implementation/prompts/phase2-backend.md
  - implementation/prompts/phase2-frontend.md
  - implementation/prompts/phase3-optional.md
  - implementation/implementation-guide.md
tests_yaml: []
prompt_text: |
  "Generate full implementation prompts for the Todo Full-Stack Web Application.

  Include prompts for Claude Code to:

  Phase 1:
  - @specs/database/schema.md implement tasks table in Neon PostgreSQL
  - @specs/api/rest-endpoints.md implement all task CRUD FastAPI routes
  - @specs/features/task-crud.md implement create/read/update/delete/complete features

  Phase 2:
  - @specs/features/authentication.md implement Better Auth signup/signin and JWT integration
  - @specs/api/rest-endpoints.md implement JWT-protected FastAPI routes
  - @specs/ui/components.md implement reusable frontend components
  - @specs/ui/pages.md implement pages layouts with responsive design

  Phase 3 (Optional):
  - @specs/features/chatbot.md implement chatbot for task management
  - @specs/api/rest-endpoints.md ensure chatbot can query task API
  - @specs/ui/pages.md add chat interface

  Ensure Claude Code:
  - Reads CLAUDE.md files (root, frontend, backend)
  - Follows all Spec-Kit references (@specs/...)
  - Generates full-stack code automatically
  - Maintains responsiveness, Tailwind styling, and JWT security
  "
response_text: |
  Created comprehensive implementation prompts for the Todo Full-Stack Web Application project. The implementation includes:

  - Phase 1 prompts for backend foundation (database, API routes, CRUD features)
  - Phase 2 prompts for backend authentication and frontend components/pages
  - Phase 3 optional prompts for chatbot features
  - Master implementation guide with instructions for Claude Code

  Each prompt is structured to guide Claude Code in generating code that follows the specifications, maintains quality standards, and implements the required features correctly.
outcome: |
  Successfully created detailed implementation prompts organized by phase and technology stack.
evaluation: |
  All required implementation prompts have been created with proper structure and spec references.
---

# Implementation Prompts Generation PHR

## Summary
Created comprehensive implementation prompts for the Todo Full-Stack Web Application project organized by phase and technology stack.

## Details
The implementation includes:
- Phase 1 prompts for backend foundation (database schema, API routes, CRUD features)
- Phase 2 prompts for backend authentication and frontend components/pages
- Phase 3 optional prompts for chatbot features
- Master implementation guide with instructions for Claude Code

Each prompt is structured to guide Claude Code in generating code that follows the specifications, maintains quality standards, and implements the required features correctly.

## Files Created
- implementation/prompts/phase1-backend.md - Backend foundation prompts
- implementation/prompts/phase2-backend.md - Backend authentication prompts
- implementation/prompts/phase2-frontend.md - Frontend components/pages prompts
- implementation/prompts/phase3-optional.md - Optional chatbot prompts
- implementation/implementation-guide.md - Master implementation guide

## Validation
- All prompts follow the required structure and include proper spec references
- Phases are organized logically with clear instructions for Claude Code
- Quality standards and technology stack requirements are clearly specified