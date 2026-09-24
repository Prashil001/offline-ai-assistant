import React, { useState } from 'react';
import { Chat } from './components/Chat';
import { Dashboard } from './components/Dashboard';
import { MessageSquare, BarChart2 } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState<'chat' | 'benchmark'>('chat');

  return (
    <div className="flex h-screen bg-gray-900 text-gray-100 font-sans">
      {/* Sidebar */}
      <div className="w-64 bg-gray-950 border-r border-gray-800 flex flex-col">
        <div className="p-6">
          <h2 className="text-xl font-bold tracking-tight text-white">Offline AI</h2>
        </div>
        
        <nav className="flex-1 px-4 space-y-2">
          <button 
            onClick={() => setActiveTab('chat')}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${activeTab === 'chat' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'}`}
          >
            <MessageSquare className="w-5 h-5" />
            Chat & RAG
          </button>
          
          <button 
            onClick={() => setActiveTab('benchmark')}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${activeTab === 'benchmark' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'}`}
          >
            <BarChart2 className="w-5 h-5" />
            Benchmarks
          </button>
        </nav>
        
        <div className="p-4 border-t border-gray-800">
          <div className="text-xs text-gray-500 text-center">
            Portfolio Project v1.0
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {activeTab === 'chat' ? <Chat /> : <Dashboard />}
      </div>
    </div>
  );
}

export default App;
