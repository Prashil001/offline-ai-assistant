import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Settings, Clock, Paperclip } from 'lucide-react';
import { useChat } from '../hooks/useChat';

const MODELS = ['qwen3:4b', 'gemma3:4b', 'llama3.2:3b'];

export function Chat() {
  const { messages, sendMessage, isTyping, model, setModel } = useChat();
  const [input, setInput] = useState('');
  const [uploading, setUploading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isTyping) return;
    sendMessage(input);
    setInput('');
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/api/v1/documents/upload', {
        method: 'POST',
        body: formData,
      });
      if (res.ok) {
        alert('Document uploaded and processed successfully!');
      } else {
        alert('Failed to upload document.');
      }
    } catch (err) {
      console.error(err);
      alert('Error uploading document.');
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  return (
    <div className="flex h-full flex-col bg-gray-900 text-gray-100">
      {/* Header */}
      <header className="flex items-center justify-between border-b border-gray-800 bg-gray-900 px-6 py-4">
        <div className="flex items-center gap-2">
          <Bot className="h-6 w-6 text-blue-500" />
          <h1 className="text-xl font-semibold">Chat Assistant</h1>
        </div>
        
        {/* Model Selector & Upload */}
        <div className="flex items-center gap-4">
          <div>
            <input 
              type="file" 
              className="hidden" 
              ref={fileInputRef}
              accept=".pdf,.txt,.md"
              onChange={handleFileUpload}
            />
            <button 
              onClick={() => fileInputRef.current?.click()}
              disabled={uploading}
              className="flex items-center gap-2 text-sm text-gray-300 hover:text-white"
            >
              <Paperclip className="h-4 w-4" />
              {uploading ? 'Uploading...' : 'Upload Doc'}
            </button>
          </div>
          
          <div className="flex items-center gap-2">
            <Settings className="h-4 w-4 text-gray-400" />
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="rounded-md border border-gray-700 bg-gray-800 px-3 py-1 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              {MODELS.map((m) => (
                <option key={m} value={m}>{m}</option>
              ))}
            </select>
          </div>
        </div>
      </header>

      {/* Chat Area */}
      <main className="flex-1 overflow-y-auto p-4 sm:p-6">
        <div className="mx-auto max-w-3xl space-y-6">
          {messages.length === 0 ? (
            <div className="flex h-[50vh] flex-col items-center justify-center text-center text-gray-500">
              <Bot className="mb-4 h-12 w-12 opacity-20" />
              <h2 className="text-xl font-medium text-gray-400">How can I help you today?</h2>
              <p className="mt-2 text-sm">Upload a document to use RAG, or just start chatting.</p>
            </div>
          ) : (
            messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex gap-4 ${
                  msg.role === 'assistant' ? 'bg-gray-800/50 p-6 rounded-lg border border-gray-800' : 'px-6'
                }`}
              >
                <div className="flex-shrink-0">
                  {msg.role === 'user' ? (
                    <div className="flex h-8 w-8 items-center justify-center rounded-sm bg-blue-600">
                      <User className="h-5 w-5 text-white" />
                    </div>
                  ) : (
                    <div className="flex h-8 w-8 items-center justify-center rounded-sm bg-emerald-600">
                      <Bot className="h-5 w-5 text-white" />
                    </div>
                  )}
                </div>
                <div className="flex-1 space-y-2">
                  <div className="prose prose-invert max-w-none">
                    <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                  </div>
                  {msg.latency_ms && (
                    <div className="flex items-center gap-1 text-xs text-gray-500">
                      <Clock className="h-3 w-3" />
                      {(msg.latency_ms / 1000).toFixed(2)}s
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
          {isTyping && messages[messages.length - 1]?.role === 'user' && (
             <div className="flex gap-4 bg-gray-800/50 p-6 rounded-lg border border-gray-800">
               <div className="flex-shrink-0">
                 <div className="flex h-8 w-8 items-center justify-center rounded-sm bg-emerald-600">
                   <Bot className="h-5 w-5 text-white" />
                 </div>
               </div>
               <div className="flex items-center gap-1">
                 <div className="h-2 w-2 animate-bounce rounded-full bg-gray-500"></div>
                 <div className="h-2 w-2 animate-bounce rounded-full bg-gray-500" style={{ animationDelay: '0.2s' }}></div>
                 <div className="h-2 w-2 animate-bounce rounded-full bg-gray-500" style={{ animationDelay: '0.4s' }}></div>
               </div>
             </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input Area */}
      <footer className="border-t border-gray-800 bg-gray-900 p-4 sm:p-6">
        <div className="mx-auto max-w-3xl">
          <form
            onSubmit={handleSubmit}
            className="relative flex items-center overflow-hidden rounded-lg border border-gray-700 bg-gray-800 focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Message the offline assistant..."
              className="w-full bg-transparent px-4 py-3 pr-12 focus:outline-none"
              disabled={isTyping}
            />
            <button
              type="submit"
              disabled={!input.trim() || isTyping}
              className="absolute right-2 rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white disabled:opacity-50 disabled:hover:bg-transparent"
            >
              <Send className="h-4 w-4" />
            </button>
          </form>
          <div className="mt-2 text-center text-xs text-gray-500">
            Running completely offline on {model}.
          </div>
        </div>
      </footer>
    </div>
  );
}
