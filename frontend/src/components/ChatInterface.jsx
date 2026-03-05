import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Upload, Send } from 'lucide-react';

export default function ChatInterface({ session, onNewSession }) {
    const [messages, setMessages] = useState(session?.history || []);
    const [input, setInput] = useState('');
    const [isUploading, setIsUploading] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const fileInputRef = useRef(null);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMsg = input;
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
        setIsLoading(true);

        try {
            const res = await fetch('http://localhost:8000/chat/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: session.session.id,
                    message: userMsg
                })
            });
            const data = await res.json();
            setMessages(prev => [...prev, data]);
        } catch (err) {
            console.error(err);
            setMessages(prev => [...prev, { role: 'assistant', content: "Error connecting to server." }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleFileUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setIsUploading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            await fetch(`http://localhost:8000/upload/?session_id=${session.session.id}`, {
                method: 'POST',
                body: formData
            });

            setMessages(prev => [...prev, {
                role: 'system',
                content: `File uploaded successfully: ${file.name}. \n\nYou can now ask me to analyze it or create a study guide!`
            }]);
        } catch (err) {
            console.error(err);
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div className="flex flex-col h-screen max-w-5xl mx-auto bg-surface shadow-xl border-x border-gray-200">
            {/* Header */}
            <div className="px-6 py-4 border-b border-gray-200 bg-white flex justify-between items-center shrink-0">
                <div>
                    <h1 className="text-xl font-bold text-gray-900 font-inter">Coursework Analyzer</h1>
                    <p className="text-sm text-gray-500 font-inter">{session?.session.course_name} - {session?.session.topic}</p>
                </div>
                <button
                    onClick={onNewSession}
                    className="text-sm text-brand-600 hover:text-brand-800 font-medium transition-colors"
                >
                    New Session
                </button>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-surface-muted">
                {messages.length === 0 && (
                    <div className="text-center text-gray-500 mt-20">
                        <p>Upload a lecture slide, note, or audio file to begin.</p>
                    </div>
                )}
                {messages.map((msg, i) => (
                    <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] rounded-2xl px-6 py-4 shadow-sm ${msg.role === 'user'
                                ? 'bg-brand-600 text-white'
                                : msg.role === 'system'
                                    ? 'bg-blue-50 text-blue-800 ring-1 ring-blue-200 text-sm'
                                    : 'bg-white ring-1 ring-gray-200 text-gray-900'
                            }`}>
                            {msg.role === 'assistant' ? (
                                <div className="prose prose-sm md:prose-base max-w-none prose-headings:font-inter prose-p:font-inter">
                                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                                </div>
                            ) : (
                                <div className="whitespace-pre-wrap font-inter">{msg.content}</div>
                            )}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-white ring-1 ring-gray-200 text-gray-500 rounded-2xl px-6 py-4 shadow-sm">
                            <span className="animate-pulse">Analyzing...</span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 bg-white border-t border-gray-200 shrink-0">
                <div className="max-w-4xl mx-auto relative flex items-center">
                    <input
                        type="file"
                        ref={fileInputRef}
                        onChange={handleFileUpload}
                        className="hidden"
                    />
                    <button
                        onClick={() => fileInputRef.current?.click()}
                        disabled={isUploading}
                        className="absolute left-4 p-2 text-gray-400 hover:text-brand-600 transition-colors disabled:opacity-50"
                    >
                        <Upload size={20} />
                    </button>

                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                        placeholder="Ask a question or request a study guide..."
                        className="w-full pl-14 pr-14 py-4 bg-gray-50 border border-gray-200 rounded-full focus:outline-none focus:ring-2 focus:ring-brand-500 focus:bg-white transition-all font-inter"
                    />

                    <button
                        onClick={handleSend}
                        disabled={!input.trim() || isLoading}
                        className="absolute right-4 p-2 text-brand-600 hover:text-brand-800 transition-colors disabled:opacity-50"
                    >
                        <Send size={20} />
                    </button>
                </div>
                {isUploading && (
                    <p className="text-xs text-center text-gray-500 mt-2 animate-pulse">Uploading and processing file...</p>
                )}
            </div>
        </div>
    );
}
