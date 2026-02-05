import api from './api.ts';

// Chat API functions
export const chatApi = {
  // Send a message to the chat endpoint
  sendMessage: async (userId: number, message: string, conversationId?: string) => {
    const response = await api.post(`/api/${userId}/chat`, {
      message,
      conversation_id: conversationId
    });
    return response.data;
  },

  // Get conversation history (if needed for initial load)
  getConversationHistory: async (userId: number, conversationId: string) => {
    // This would be a GET endpoint if available, but currently the API is POST-only
    // We'll handle conversation continuity through the sendMessage endpoint
    return null;
  }
};