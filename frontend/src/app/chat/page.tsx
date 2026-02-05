'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/auth-context';
import Header from '@/components/header';
import ChatInterface from '@/components/chat-interface';
import { chatApi } from '@/lib/chat-api';
import toast, { Toaster } from 'react-hot-toast';

interface ToolCall {
  name: string;
  parameters: Record<string, any>;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  toolCalls?: ToolCall[];
}

export default function ChatPage() {
  const { loading, isAuthenticated, user } = useAuth();
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);

  // Check authentication
  useEffect(() => {
    if (!loading && !isAuthenticated()) {
      router.push('/login');
    }
  }, [loading, isAuthenticated, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-app">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-highlight-primary"></div>
      </div>
    );
  }

  if (!isAuthenticated() || !user) {
    return null; // Redirect happens in useEffect
  }

  const handleSendMessage = async (message: string) => {
    if (!user?.id || isLoading) return;

    try {
      setIsLoading(true);

      // Add user message to UI immediately
      const userMessage: Message = {
        id: Date.now().toString(),
        role: 'user',
        content: message,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, userMessage]);

      // Send message to API
      const response = await chatApi.sendMessage(user.id, message, currentConversationId ?? undefined);

      // Update conversation ID if new conversation was created
      if (response.conversation_id && !currentConversationId) {
        setCurrentConversationId(response.conversation_id);
      }

      // Add assistant response to messages with tool calls
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: response.response,
        timestamp: new Date(response.timestamp),
        toolCalls: response.tool_calls || []
      };

      setMessages(prev => [...prev, assistantMessage]);

    } catch (error: any) {
      console.error('Error sending message:', error);

      // Show error message to user
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to send message';
      toast.error(`Error: ${errorMessage}`);

      // Add error message to UI
      const errorMessageObj: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: `Sorry, I encountered an error: ${errorMessage}`,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessageObj]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-app">
      <Header />
      <main className="py-6">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-primary">AI Task Assistant</h1>
            <p className="text-muted">Chat with your personal AI assistant to manage tasks</p>
          </div>

          <div className="h-[calc(100vh-200px)] flex flex-col">
            <ChatInterface
              initialMessages={messages}
              onSendMessage={handleSendMessage}
              isLoading={isLoading}
            />
          </div>
        </div>
      </main>
      <Toaster position="top-right" />
    </div>
  );
}