'use client';

import { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/context/auth-context';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatInterfaceProps {
  initialMessages?: Message[];
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

export default function ChatInterface({
  initialMessages = [],
  onSendMessage,
  isLoading = false
}: ChatInterfaceProps) {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { user } = useAuth();

  // Update messages when initialMessages prop changes
  useEffect(() => {
    setMessages(initialMessages);
  }, [initialMessages]);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue.trim());
      setInputValue('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (inputValue.trim() && !isLoading) {
        handleSubmit(e);
      }
    }
  };

  return (
    <div className="flex flex-col h-full bg-surface rounded-lg border border-neon overflow-hidden">
      {/* Chat Header */}
      <div className="px-4 py-3 border-b border-neon bg-surface-secondary">
        <div className="flex items-center">
          <div className="w-3 h-3 rounded-full bg-green-500 mr-2"></div>
          <h2 className="text-lg font-semibold text-primary">AI Task Assistant</h2>
        </div>
        <p className="text-xs text-muted ml-5">Connected as {user?.name}</p>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-[calc(100vh-250px)]">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center p-4">
            <div className="mb-4">
              <div className="bg-gradient-to-r from-highlight-primary to-purple-500 p-3 rounded-full inline-block">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
              </div>
            </div>
            <h3 className="text-xl font-medium text-primary mb-2">Welcome to TodoBoom AI Assistant!</h3>
            <p className="text-muted max-w-md">
              I can help you manage your tasks. Try asking me to add, list, complete, or update tasks.
              For example: "Add a task to buy groceries" or "Show me my tasks".
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.role === 'user'
                    ? 'bg-highlight-primary text-white rounded-br-none'
                    : 'bg-surface-secondary text-primary rounded-bl-none border border-neon'
                }`}
              >
                <div className="whitespace-pre-wrap break-words">
                  {message.content}
                </div>
                <div className={`text-xs mt-1 ${message.role === 'user' ? 'text-blue-100' : 'text-muted'}`}>
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>

                {/* Display tool calls if this is an assistant message */}
                {message.role === 'assistant' && message.toolCalls && message.toolCalls.length > 0 && (
                  <div className="mt-2 pt-2 border-t border-gray-700">
                    <p className="text-xs text-yellow-400 font-medium">Used tools:</p>
                    <div className="mt-1 space-y-1">
                      {message.toolCalls.map((toolCall, index) => (
                        <div key={index} className="text-xs bg-gray-800 p-2 rounded">
                          <span className="font-mono text-cyan-300">{toolCall.name}</span>
                          <span className="ml-2 text-gray-400">
                            {JSON.stringify(toolCall.parameters)}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))
        )}

        {/* Typing indicator when loading */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="max-w-[80%] rounded-lg px-4 py-2 bg-surface-secondary text-primary rounded-bl-none border border-neon">
              <div className="flex space-x-2">
                <div className="w-2 h-2 rounded-full bg-muted animate-bounce"></div>
                <div className="w-2 h-2 rounded-full bg-muted animate-bounce delay-100"></div>
                <div className="w-2 h-2 rounded-full bg-muted animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-neon p-4 bg-surface-secondary">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message here..."
            disabled={isLoading}
            className="flex-1 resize-none border border-neon rounded-lg px-3 py-2 bg-input text-primary focus:outline-none focus:ring-2 focus:ring-highlight-primary focus:border-transparent min-h-[60px] max-h-32"
            rows={1}
          />
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className={`px-4 py-2 rounded-lg font-medium ${
              inputValue.trim() && !isLoading
                ? 'bg-gradient-to-r from-highlight-primary to-purple-600 text-white hover:opacity-90'
                : 'bg-gray-600 text-gray-400 cursor-not-allowed'
            }`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </form>
        <p className="text-xs text-muted mt-2 text-center">
          AI Assistant can help you manage tasks using natural language
        </p>
      </div>
    </div>
  );
}