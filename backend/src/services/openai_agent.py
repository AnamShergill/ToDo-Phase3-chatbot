"""
OpenAI Agent Integration
Handles the OpenAI Agent API integration with MCP tools
"""

import os
from typing import Dict, Any, List, Optional
from openai import OpenAI
from src.mcp.server import mcp_server
import json


class OpenAIAgentService:
    """
    Service to integrate OpenAI Agent with MCP tools
    - Agent can call MCP tools based on natural language
    - Tool execution results are properly formatted
    - Agent generates appropriate responses based on tool output
    """

    def __init__(self):
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.client = OpenAI(api_key=api_key)
        self.tools = self._define_agent_tools()

    def _define_agent_tools(self) -> List[Dict[str, Any]]:
        """
        Define the tools available to the OpenAI agent
        These map to our MCP tools
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Creates a new task for a user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer", "description": "The ID of the user"},
                            "title": {"type": "string", "description": "The title of the task"},
                            "description": {"type": "string", "description": "Optional description of the task"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Returns tasks for a user filtered by status",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer", "description": "The ID of the user"},
                            "status": {
                                "type": "string",
                                "enum": ["all", "pending", "completed"],
                                "description": "Filter tasks by status"
                            }
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Marks a specified task as complete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer", "description": "The ID of the user"},
                            "task_id": {"type": "integer", "description": "The ID of the task to complete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Removes a specified task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer", "description": "The ID of the user"},
                            "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Updates task details",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer", "description": "The ID of the user"},
                            "task_id": {"type": "integer", "description": "The ID of the task to update"},
                            "title": {"type": "string", "description": "New title for the task (optional)"},
                            "description": {"type": "string", "description": "New description for the task (optional)"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]

    async def run_agent(self, user_id: int, user_message: str, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Run the OpenAI agent with the provided message and conversation history
        The agent will use MCP tools as needed
        """
        try:
            # Prepare messages for the agent
            messages = []

            # Add system message to instruct the agent
            messages.append({
                "role": "system",
                "content": f"""You are a helpful AI assistant that manages tasks for users. Use the available tools to add, list, complete, delete, or update tasks. Always respect the user_id ({user_id}) when calling tools. The user wants you to help manage their tasks."""
            })

            # Add conversation history
            for msg in conversation_history:
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })

            # Add the current user message
            messages.append({
                "role": "user",
                "content": user_message
            })

            # Call OpenAI with tools
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Could be configurable
                messages=messages,
                tools=self.tools,
                tool_choice="auto"  # Auto-select tools as needed
            )

            # Process the response
            return await self._process_agent_response(response, user_id)

        except Exception as e:
            print(f"Error running OpenAI agent: {str(e)}")
            return {
                'response': f"I'm sorry, I encountered an error: {str(e)}",
                'tool_calls': [],
                'success': False
            }

    async def _process_agent_response(self, response, user_id: int) -> Dict[str, Any]:
        """
        Process the agent's response, including any tool calls
        """
        choice = response.choices[0]
        message = choice.message

        tool_calls = []
        tool_call_results = []

        # Handle tool calls if any
        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Ensure user_id is set correctly
                function_args['user_id'] = user_id

                # Call the MCP tool
                try:
                    result = await mcp_server.call_tool(function_name, function_args)

                    tool_calls.append({
                        'name': function_name,
                        'parameters': function_args,
                        'result': result
                    })

                    tool_call_results.append(result)
                except Exception as e:
                    tool_call_results.append({
                        'success': False,
                        'error': f"Tool call failed: {str(e)}"
                    })

        # Formulate the response
        if message.content:
            response_text = message.content
        else:
            # If no content but there were tool calls, generate a response based on tool results
            if tool_call_results:
                success_results = [r for r in tool_call_results if r.get('success')]
                error_results = [r for r in tool_call_results if not r.get('success')]

                parts = []
                if success_results:
                    parts.append(f"I've completed {len(success_results)} action(s) successfully.")
                if error_results:
                    parts.append(f"Some actions had issues: {[r.get('error', 'Unknown error') for r in error_results]}")

                response_text = " ".join(parts) if parts else "I've processed your request."
            else:
                response_text = "I've processed your request."

        return {
            'response': response_text,
            'tool_calls': tool_calls,
            'success': True
        }