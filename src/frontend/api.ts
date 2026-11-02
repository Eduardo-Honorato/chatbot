/**
 * API services for Chatbot Frontend
 * communicates with the Flask backend
 */

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export interface SearchResult {
  file: string;
  excerpt: string;
}

export interface ChatResponse {
  response: string;
  provider: string;
}

// Backend API base URL
// In production, this will be the Vercel deployment URL
const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:5000';

// Chat API
export const chatAPI = async (message: string): Promise<ChatResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Chat API error:', error);
    throw error;
  }
};

// History API
export const historyAPI = async (sessionId: string): Promise<Message[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/history?session_id=${sessionId}`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return data.messages || [];
  } catch (error) {
    console.error('History API error:', error);
    throw error;
  }
};

// Search API
export const searchAPI = async (query: string): Promise<SearchResult[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return data.results || [];
  } catch (error) {
    console.error('Search API error:', error);
    throw error;
  }
};

// Health check API
export const healthAPI = async (): Promise<{ status: string; version: string }> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Health API error:', error);
    throw error;
  }
};