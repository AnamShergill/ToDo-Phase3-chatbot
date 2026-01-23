"""
Chat Service
Core business logic for chat operations
"""

from typing import Dict, Any, List
from src.services.conversation_service import ConversationService
from src.services.openai_agent import OpenAIAgentService
from src.schemas.chat import ToolCall
from datetime import datetime
import asyncio
import os


class ChatService:
    """
    Core business logic for chat operations
    - Loads conversation history from database
    - Stores new user messages
    - Stores assistant responses
    - Integrates with OpenAI Agent and MCP tools
    - Proper error handling and logging
    """

    def __init__(self):
        self.conversation_service = ConversationService()

        # Initialize OpenAI Agent if API key is available
        if os.getenv("OPENAI_API_KEY"):
            self.agent_service = OpenAIAgentService()
        else:
            self.agent_service = None
            print("WARNING: OPENAI_API_KEY not found. Using simulated agent.")

    async def process_chat_request(self, user_id: int, message: str, conversation_id: str = None) -> Dict[str, Any]:
        """
        Process a chat request and return response
        """
        try:
            # Get or create conversation
            conversation = self.conversation_service.get_or_create_conversation(user_id, conversation_id)
            current_conversation_id = conversation.id

            # Save user message
            self.conversation_service.save_message(
                conversation_id=current_conversation_id,
                user_id=user_id,
                role='user',
                content=message
            )

            # Load conversation history
            history = self.conversation_service.get_conversation_history(current_conversation_id, user_id)

            # Process with OpenAI agent or fallback to simulated agent
            if self.agent_service:
                agent_response = await self.agent_service.run_agent(user_id, message, history)
            else:
                agent_response = await self._simulate_agent_response(user_id, message, history)

            # Save assistant response
            self.conversation_service.save_message(
                conversation_id=current_conversation_id,
                user_id=user_id,
                role='assistant',
                content=agent_response['response']
            )

            # Return response with conversation ID and any tool calls made
            return {
                'conversation_id': current_conversation_id,
                'response': agent_response.get('response', ''),
                'tool_calls': agent_response.get('tool_calls', []),
                'timestamp': datetime.utcnow().isoformat()
            }

        except Exception as e:
            # Proper error handling and logging
            print(f"Error processing chat request: {str(e)}")
            return {
                'conversation_id': conversation_id or '',
                'response': f"I'm sorry, I encountered an error: {str(e)}",
                'tool_calls': [],
                'timestamp': datetime.utcnow().isoformat()
            }

    async def _simulate_agent_response(self, user_id: int, user_message: str, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Simulate agent response that integrates with MCP tools
        This is used when OpenAI API key is not available
        """
        # For the simulation, we'll use a simple rule-based approach
        # In a real implementation, this would be handled by the OpenAI agent
        from src.mcp.server import mcp_server

        tool_calls = []
        response_text = ""

        # Simple rule-based processing to demonstrate MCP tool integration
        lower_msg = user_message.lower()

        if 'add' in lower_msg and ('task' in lower_msg or 'todo' in lower_msg):
            # Extract task title from message (simple extraction)
            task_title = self._extract_task_title(user_message)

            if task_title:
                # Call add_task tool
                tool_params = {
                    'user_id': user_id,
                    'title': task_title
                }

                # Extract description if present
                if 'description' in lower_msg or 'desc' in lower_msg:
                    # Simple description extraction
                    desc_start = max(lower_msg.find('description'), lower_msg.find('desc'))
                    if desc_start != -1:
                        description = user_message[desc_start + (11 if 'description' in lower_msg else 5):].strip()
                        if description.startswith(':'):
                            description = description[1:].strip()
                        tool_params['description'] = description

                try:
                    result = await mcp_server.call_tool('add_task', tool_params)
                    if result.get('success'):
                        tool_calls.append({
                            'name': 'add_task',
                            'parameters': tool_params
                        })
                        response_text = f"I've added the task '{task_title}' to your list."
                    else:
                        response_text = f"I couldn't add the task: {result.get('error', 'Unknown error')}"
                except Exception as e:
                    response_text = f"I encountered an error while adding the task: {str(e)}"
            else:
                response_text = "I can help you add a task. Please specify what task you'd like to add."

        elif 'list' in lower_msg and ('task' in lower_msg or 'todo' in lower_msg):
            # Determine status filter
            status = 'all'
            if 'completed' in lower_msg:
                status = 'completed'
            elif 'pending' in lower_msg or 'incomplete' in lower_msg:
                status = 'pending'

            try:
                tool_params = {
                    'user_id': user_id,
                    'status': status
                }

                result = await mcp_server.call_tool('list_tasks', tool_params)
                if result.get('success'):
                    tool_calls.append({
                        'name': 'list_tasks',
                        'parameters': tool_params
                    })

                    tasks = result.get('tasks', [])
                    if tasks:
                        task_list = "\n".join([f"- {task['title']}" for task in tasks[:5]])  # Limit to first 5
                        if len(tasks) > 5:
                            task_list += f"\n... and {len(tasks) - 5} more tasks"

                        status_text = f"{status} " if status != 'all' else ""
                        response_text = f"Here are your {status_text}tasks:\n{task_list}"
                    else:
                        status_text = f"{status} " if status != 'all' else ""
                        response_text = f"You don't have any {status_text}tasks."
                else:
                    response_text = f"I couldn't list your tasks: {result.get('error', 'Unknown error')}"
            except Exception as e:
                response_text = f"I encountered an error while listing tasks: {str(e)}"

        elif 'complete' in lower_msg or 'done' in lower_msg or 'finish' in lower_msg:
            # Extract task identifier (this would be more sophisticated in a real implementation)
            task_id = self._extract_task_id(user_message)
            if task_id:
                try:
                    tool_params = {
                        'user_id': user_id,
                        'task_id': task_id
                    }

                    result = await mcp_server.call_tool('complete_task', tool_params)
                    if result.get('success'):
                        tool_calls.append({
                            'name': 'complete_task',
                            'parameters': tool_params
                        })
                        response_text = f"I've marked the task as complete."
                    else:
                        response_text = f"I couldn't complete the task: {result.get('error', 'Unknown error')}"
                except Exception as e:
                    response_text = f"I encountered an error while completing the task: {str(e)}"
            else:
                response_text = "I can help you mark a task as complete. Please specify which task."

        elif 'delete' in lower_msg or 'remove' in lower_msg:
            # Extract task identifier
            task_id = self._extract_task_id(user_message)
            if task_id:
                try:
                    tool_params = {
                        'user_id': user_id,
                        'task_id': task_id
                    }

                    result = await mcp_server.call_tool('delete_task', tool_params)
                    if result.get('success'):
                        tool_calls.append({
                            'name': 'delete_task',
                            'parameters': tool_params
                        })
                        response_text = f"I've deleted the task."
                    else:
                        response_text = f"I couldn't delete the task: {result.get('error', 'Unknown error')}"
                except Exception as e:
                    response_text = f"I encountered an error while deleting the task: {str(e)}"
            else:
                response_text = "I can help you delete a task. Please specify which task."

        elif 'update' in lower_msg or 'change' in lower_msg or 'modify' in lower_msg:
            # Extract task identifier and new details
            task_id = self._extract_task_id(user_message)
            if task_id:
                new_title = self._extract_task_title(user_message)
                try:
                    tool_params = {
                        'user_id': user_id,
                        'task_id': task_id
                    }

                    if new_title:
                        tool_params['title'] = new_title

                    result = await mcp_server.call_tool('update_task', tool_params)
                    if result.get('success'):
                        tool_calls.append({
                            'name': 'update_task',
                            'parameters': tool_params
                        })
                        response_text = f"I've updated the task."
                    else:
                        response_text = f"I couldn't update the task: {result.get('error', 'Unknown error')}"
                except Exception as e:
                    response_text = f"I encountered an error while updating the task: {str(e)}"
            else:
                response_text = "I can help you update a task. Please specify which task and what changes to make."

        else:
            # Default response for unrecognized commands
            response_text = f"I understand you said: '{user_message}'. I can help you manage your tasks. You can ask me to add, list, complete, delete, or update tasks."

        return {
            'response': response_text,
            'tool_calls': tool_calls,
            'success': True
        }

    def _extract_task_title(self, message: str) -> str:
        """
        Simple method to extract task title from user message
        In a real implementation, this would use NLP to better understand the intent
        """
        # Remove common prefixes
        message_lower = message.lower()

        # Look for patterns like "add task to..." or "create task..."
        for pattern in ['add task to ', 'add a task to ', 'create task ', 'create a task ', 'add ', 'make ', 'create ']:
            if pattern in message_lower:
                start_pos = message_lower.find(pattern) + len(pattern)
                task_title = message[start_pos:].strip()

                # Remove common suffixes
                for suffix in ['.', '!', '?', 'please', 'thanks', 'thank you']:
                    if task_title.lower().endswith(suffix):
                        task_title = task_title[:-len(suffix)].strip()

                return task_title if task_title else message

        # If no pattern matched, return the whole message as a fallback
        return message.strip()

    def _extract_task_id(self, message: str) -> int:
        """
        Simple method to extract task ID from user message
        In a real implementation, this would use more sophisticated NLP
        """
        # This is a simplified version - in reality, you'd need more advanced NLP
        # to identify which specific task the user wants to operate on
        # For now, we'll just return None to indicate that we can't reliably identify the task
        return None