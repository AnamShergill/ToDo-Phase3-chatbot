# AI-Powered Todo Chatbot Architecture Plan

## Overview
This plan outlines the architecture for implementing an AI-powered chatbot that allows users to manage their todos through natural language conversations using MCP tools.

## Architecture Components

### 1. Chat API Layer
**Component**: FastAPI endpoint `/api/{user_id}/chat`
- Stateless design requiring full conversation history retrieval on each request
- Integration with OpenAI Agent SDK for natural language processing
- MCP tool orchestration for database operations
- Response formatting with conversation_id, response text, and tool calls

**Files to Create/Modify**:
- `backend/src/api/chat.py` - Chat API endpoints
- `backend/src/schemas/chat.py` - Request/response schemas

### 2. MCP Server Implementation
**Component**: Model Context Protocol server exposing todo management tools
- `add_task` tool: Creates new tasks in the database
- `list_tasks` tool: Retrieves tasks based on user_id and status filters
- `complete_task` tool: Updates task completion status
- `delete_task` tool: Removes tasks from the database
- `update_task` tool: Modifies task details

**Files to Create/Modify**:
- `backend/src/mcp/server.py` - MCP server implementation
- `backend/src/mcp/tools.py` - Individual tool implementations

### 3. Database Layer Enhancements
**Component**: SQLModel entities for conversation management
- Conversation model: Stores conversation metadata
- Message model: Stores individual conversation messages
- Updated Task model: Ensure compatibility with new requirements

**Files to Create/Modify**:
- `backend/src/models/conversation.py` - Conversation entity
- `backend/src/models/message.py` - Message entity
- `backend/src/db/session.py` - Database session management

### 4. Service Layer
**Component**: Business logic for conversation management
- Conversation history loading and storage
- Message persistence
- Integration between chat API and MCP tools
- Error handling and user feedback

**Files to Create/Modify**:
- `backend/src/services/chat_service.py` - Chat business logic
- `backend/src/services/conversation_service.py` - Conversation management
- `backend/src/services/task_service.py` - Enhanced task operations

### 5. Frontend Integration
**Component**: OpenAI ChatKit UI for interacting with the chat API
- Chat interface for sending and receiving messages
- Conversation continuity support
- Display of tool-driven responses

**Files to Create/Modify**:
- `frontend/src/app/chat/page.tsx` - Chat page component
- `frontend/src/components/ChatInterface.tsx` - Chat UI component
- `frontend/src/lib/api/chat.ts` - Chat API client

## Technology Stack
- **Backend**: FastAPI, SQLModel, Neon Postgres
- **AI/ML**: OpenAI Agent SDK
- **MCP**: Model Context Protocol SDK
- **Frontend**: Next.js, OpenAI ChatKit
- **Database**: Neon Postgres with SQLModel ORM

## Data Flow Architecture

### Stateless Chat Request Flow
1. Client sends chat request with message and optional conversation_id
2. Server loads conversation history from database using conversation_id
3. Server appends new user message to conversation history
4. OpenAI Agent processes message with available MCP tools
5. MCP tools execute database operations (read/write)
6. Agent generates response based on tool execution results
7. Server stores assistant response in database
8. Server returns response to client with updated conversation_id

### MCP Tool Architecture
- Tools are registered with the MCP server
- Tools receive user_id and relevant parameters
- Tools perform database operations using SQLModel
- Tools return structured responses
- Tools are stateless and don't maintain session data

## Security Considerations
- User data isolation by user_id in all operations
- Authentication validation through existing Better Auth system
- Input sanitization for all user messages
- Secure database connection handling

## Performance Considerations
- Database indexing on user_id, conversation_id, and timestamps
- Efficient loading of conversation history
- Connection pooling for database operations
- Caching strategies for frequently accessed data

## Error Handling Strategy
- Graceful handling of database connection failures
- User-friendly error messages for invalid requests
- Proper logging for debugging and monitoring
- Recovery mechanisms for partial failures

## Deployment Architecture
- Backend deployment maintaining existing structure
- Environment variable configuration for OpenAI and MCP services
- Database migration scripts for new entities
- Frontend deployment with chat interface

## Dependencies
- OpenAI API access and credentials
- MCP SDK installation and configuration
- Existing database connection and models
- Better Auth integration for user identification

## Implementation Phases

### Phase 1: Database and Models
- Implement Conversation and Message SQLModel entities
- Create database migration scripts
- Test database operations

### Phase 2: MCP Server
- Implement MCP server infrastructure
- Create individual MCP tools (add_task, list_tasks, etc.)
- Test MCP tool functionality independently

### Phase 3: Chat API
- Implement chat endpoint in FastAPI
- Integrate OpenAI Agent with MCP tools
- Implement stateless conversation flow

### Phase 4: Frontend Integration
- Create chat interface using OpenAI ChatKit
- Connect frontend to chat API
- Implement conversation continuity

### Phase 5: Testing and Integration
- End-to-end testing of chat functionality
- User acceptance testing
- Performance optimization