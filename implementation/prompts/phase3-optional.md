# Phase 3 Optional Implementation Prompts

## Chatbot Implementation Prompt

**Task**: Implement chatbot for task management following @specs/features/chatbot.md

**Instructions for Claude Code**:
- Read the chatbot feature specification at @specs/features/chatbot.md (if exists, otherwise create based on user stories)
- Create a chatbot service in backend/src/services/chatbot_service.py
- Implement natural language processing for task creation
- Create the chatbot API endpoint in backend/src/api/chatbot.py
- Implement intent recognition for common task operations
- Add response generation for user queries
- Ensure the chatbot can interact with the task management system
- Include proper error handling and fallback responses
- Add logging for chatbot interactions
- Consider privacy and security aspects of chat data

## API Integration Prompt

**Task**: Ensure chatbot can query task API following @specs/api/rest-endpoints.md

**Instructions for Claude Code**:
- Read the API endpoint specification at @specs/api/rest-endpoints.md
- Integrate the chatbot service with existing task API endpoints
- Implement proper authentication for chatbot API calls
- Ensure the chatbot respects user data isolation
- Add appropriate error handling for API failures
- Implement caching if needed for performance
- Follow the same response format as other API endpoints
- Add rate limiting to prevent abuse of chatbot functionality

## Chat Interface Implementation Prompt

**Task**: Add chat interface following @specs/ui/pages.md

**Instructions for Claude Code**:
- Read the UI pages specification at @specs/ui/pages.md
- Create the Chat Interface component in frontend/src/components/chat-interface.tsx
- Add chat interface to the dashboard page or create a dedicated chat page
- Implement real-time messaging functionality
- Add typing indicators and message history
- Ensure the interface is responsive and accessible
- Follow the design system for styling and components
- Add proper error handling for chat functionality
- Implement scroll behavior for message history