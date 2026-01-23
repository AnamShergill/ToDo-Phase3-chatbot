# Phase 2 Backend Implementation Prompts

## Authentication Implementation Prompt

**Task**: Implement Better Auth signup/signin and JWT integration following @specs/features/authentication.md

**Instructions for Claude Code**:
- Read the authentication feature specification at @specs/features/authentication.md
- Set up Better Auth configuration for the frontend
- Create JWT utility functions in backend/src/utils/jwt.py
- Implement user registration and login endpoints in backend/src/api/auth.py
- Create user service functions for authentication in backend/src/services/user_service.py
- Ensure passwords are properly hashed using bcrypt or similar
- Implement proper token generation with appropriate claims
- Add token validation and refresh mechanisms
- Follow all security requirements from the spec
- Include rate limiting for authentication endpoints

## JWT-Protected Routes Implementation Prompt

**Task**: Implement JWT-protected FastAPI routes following @specs/api/rest-endpoints.md

**Instructions for Claude Code**:
- Read the API endpoint specification at @specs/api/rest-endpoints.md
- Create JWT authentication middleware in backend/src/middleware/auth.py
- Update all task endpoints to require valid JWT tokens
- Implement proper user identification from JWT claims
- Ensure user isolation (each user can only access their own data)
- Add appropriate error responses for authentication failures (401, 403)
- Implement logout functionality if needed
- Ensure all protected endpoints validate tokens properly
- Add token refresh capabilities if specified in the API spec