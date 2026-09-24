import { useState, useCallback } from 'react';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  latency_ms?: number;
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [model, setModel] = useState('qwen3:4b');
  const [conversationId, setConversationId] = useState<string | null>(null);

  const sendMessage = useCallback(async (content: string) => {
    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsTyping(true);

    const assistantMsgId = (Date.now() + 1).toString();
    const assistantMsg: Message = {
      id: assistantMsgId,
      role: 'assistant',
      content: '',
    };
    
    setMessages((prev) => [...prev, assistantMsg]);

    const startTime = performance.now();

    try {
      const response = await fetch('http://localhost:8000/api/v1/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: content,
          model: model,
          stream: true,
          conversation_id: conversationId,
        }),
      });

      if (!response.body) throw new Error("No response body");
      
      const newConvId = response.headers.get("X-Conversation-ID");
      if (newConvId && !conversationId) {
        setConversationId(newConvId);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let done = false;
      let text = '';

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          text += chunk;
          setMessages((prev) => 
            prev.map((msg) => 
              msg.id === assistantMsgId ? { ...msg, content: text } : msg
            )
          );
        }
      }
      
      const endTime = performance.now();
      
      setMessages((prev) => 
        prev.map((msg) => 
          msg.id === assistantMsgId ? { ...msg, latency_ms: Math.round(endTime - startTime) } : msg
        )
      );

    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prev) => 
        prev.map((msg) => 
          msg.id === assistantMsgId ? { ...msg, content: 'Error: Failed to fetch response from backend.' } : msg
        )
      );
    } finally {
      setIsTyping(false);
    }
  }, [model, conversationId]);

  const loadConversation = useCallback(async (id: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/chat/history/${id}`);
      if (!response.ok) throw new Error("Failed to fetch history");
      const data = await response.json();
      
      setMessages(data.map((msg: any) => ({
        id: msg.id,
        role: msg.role,
        content: msg.content,
        latency_ms: msg.latency_ms,
      })));
      setConversationId(id);
    } catch (error) {
      console.error("Error loading conversation:", error);
    }
  }, []);

  const createNewConversation = useCallback(() => {
    setMessages([]);
    setConversationId(null);
  }, []);

  return { 
    messages, 
    sendMessage, 
    isTyping, 
    model, 
    setModel,
    loadConversation,
    createNewConversation
  };
}
