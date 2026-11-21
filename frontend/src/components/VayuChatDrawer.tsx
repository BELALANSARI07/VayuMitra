import React, { useEffect, useRef, useState } from 'react';
import { CitationRef, ImpactDelta } from '../types';
import { ImpactBadge } from './ImpactBadge';

export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  citations?: CitationRef[];
  impact?: ImpactDelta;
}

interface VayuChatDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  onOpen: () => void;
  messages: ChatMessage[];
  isStreaming: boolean;
  onSendMessage: (msg: string) => void;
}

const STARTER_PROMPTS = [
  'Is it safe to jog outdoors at 6 AM today?',
  'Best DIY air purifier hack under ₹500?',
  'School commute timing & safety for my child?',
  'Compare N95 vs cloth mask for two-wheelers',
];

export const VayuChatDrawer: React.FC<VayuChatDrawerProps> = ({
  isOpen,
  onClose,
  onOpen,
  messages,
  isStreaming,
  onSendMessage,
}) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll on new message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isStreaming]);

  // Handle Escape key to close
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  // Focus input when opened
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 150);
    }
  }, [isOpen]);

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || isStreaming) return;
    onSendMessage(input.trim());
    setInput('');
  };

  const handleTextareaKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <>
      {/* Floating Chat Trigger Button */}
      {!isOpen && (
        <button
          type="button"
          onClick={onOpen}
          aria-expanded={false}
          aria-label="Open VayuMitra GenAI Air Quality Chat Assistant"
          className="fixed bottom-6 right-6 z-40 bg-[#1F2937] hover:bg-[#374151] text-white px-5 py-3.5 rounded-full shadow-2xl flex items-center gap-3 transition-transform hover:scale-105 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-blue-500 border border-gray-600 font-bold tracking-wide"
        >
          <span className="text-xl" aria-hidden="true">
            💬
          </span>
          <span>Ask VayuMitra</span>
          <span className="px-2 py-0.5 rounded-full text-[10px] uppercase font-black bg-amber-400 text-[#1F2937]">
            AI Live
          </span>
        </button>
      )}

      {/* Backdrop overlay */}
      {isOpen && (
        <div
          onClick={onClose}
          aria-hidden="true"
          className="fixed inset-0 bg-black/40 backdrop-blur-xs z-40 transition-opacity"
        />
      )}

      {/* Chat Drawer */}
      <aside
        role="complementary"
        aria-label="Chat with VayuMitra Assistant"
        aria-hidden={!isOpen}
        className={`fixed inset-y-0 right-0 z-50 w-full sm:max-w-md bg-[#FFFBF7] shadow-2xl border-l border-[#FFE8D6] flex flex-col transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        {/* Header */}
        <div className="p-4 sm:p-5 bg-[#FFE8D6] border-b border-[#FFDAB9] flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <span className="text-2xl" aria-hidden="true">
              🤖
            </span>
            <div>
              <h2 className="text-base sm:text-lg font-extrabold text-[#1F2937] leading-none">
                VayuMitra Assistant
              </h2>
              <span className="text-xs text-[#78350F] font-semibold">
                Grounded in CPCB, WHO & Deterministic Math
              </span>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close Chat Drawer"
            className="p-2 rounded-xl text-[#1F2937] hover:bg-[#FFDAB9] focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-blue-600"
          >
            <span aria-hidden="true" className="text-lg font-bold">
              ✕
            </span>
          </button>
        </div>

        {/* Message Log */}
        <div
          role="log"
          aria-live="polite"
          aria-atomic="false"
          className="flex-1 overflow-y-auto p-4 sm:p-5 space-y-4"
        >
          {messages.length === 0 ? (
            <div className="space-y-4 my-6">
              <div className="bg-white p-4 rounded-2xl border border-[#FFE8D6] shadow-xs text-xs text-[#4B5563]">
                <p className="font-bold text-[#1F2937] mb-1">Welcome! I'm VayuMitra.</p>
                <p>
                  Ask me anything about safe outdoor exercise timings, low-cost indoor filters, child school commute safety, or sustainable transport alternatives. All health impact metrics are deterministically computed.
                </p>
              </div>

              <div>
                <span className="block text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-2">
                  Starter Questions:
                </span>
                <div className="space-y-2">
                  {STARTER_PROMPTS.map((prompt, i) => (
                    <button
                      key={i}
                      type="button"
                      onClick={() => onSendMessage(prompt)}
                      className="w-full text-left p-3 rounded-xl bg-white hover:bg-[#FFE8D6]/60 border border-[#E5E7EB] text-xs font-semibold text-[#1F2937] transition-all focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-blue-600 shadow-2xs"
                    >
                      💡 {prompt}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
              >
                <div
                  className={`max-w-[90%] p-3.5 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                    msg.sender === 'user'
                      ? 'bg-[#1F2937] text-white rounded-br-xs'
                      : 'bg-white border border-[#FFE8D6] text-[#1F2937] rounded-bl-xs shadow-xs'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{msg.text}</p>

                  {/* Impact badge if computed */}
                  {msg.impact && (
                    <div className="mt-2.5 pt-2 border-t border-gray-100">
                      <ImpactBadge
                        pm25ReductionUg={msg.impact.pm25_reduction_ug_per_day}
                        cigaretteEquivalents={msg.impact.cigarette_equivalents_saved}
                      />
                    </div>
                  )}

                  {/* Citations if available */}
                  {msg.citations && msg.citations.length > 0 && (
                    <div className="mt-3 pt-2 border-t border-gray-100 text-[11px] text-[#6B7280]">
                      <span className="font-bold uppercase tracking-wider text-[10px] text-[#D97706] block mb-1">
                        Authoritative Citations:
                      </span>
                      <ul className="space-y-0.5">
                        {msg.citations.map((c, idx) => (
                          <li key={idx} className="font-mono">
                            • {c.source} (p. {c.page}, {c.section})
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            ))
          )}

          {isStreaming && (
            <div className="flex items-center gap-2 text-xs font-semibold text-[#D97706] bg-amber-50 p-2.5 rounded-xl border border-amber-200 w-fit">
              <span className="animate-pulse">●</span> VayuMitra is responding...
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <form onSubmit={handleSubmit} className="p-3.5 sm:p-4 bg-white border-t border-[#E5E7EB]">
          <div className="relative">
            <label htmlFor="chat-user-input" className="sr-only">
              Type your air quality question
            </label>
            <textarea
              id="chat-user-input"
              ref={inputRef}
              rows={2}
              maxLength={1000}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleTextareaKeyDown}
              placeholder="Ask about outdoor jogging, DIY filters, or commute..."
              disabled={isStreaming}
              className="w-full px-3.5 py-2.5 rounded-xl border border-[#D1D5DB] text-xs sm:text-sm text-[#1F2937] placeholder:text-[#9CA3AF] resize-none focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-blue-600"
            />
          </div>

          <div className="flex items-center justify-between mt-2">
            <span
              aria-live="polite"
              aria-atomic="true"
              className={`text-[11px] font-mono ${
                input.length > 900 ? 'text-red-600 font-bold' : 'text-[#9CA3AF]'
              }`}
            >
              {input.length}/1000
            </span>

            <button
              type="submit"
              disabled={!input.trim() || isStreaming}
              className="px-4 py-2 rounded-xl bg-[#1F2937] hover:bg-[#374151] text-white text-xs font-bold transition-all focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-blue-600 disabled:opacity-40"
            >
              Send Message ➤
            </button>
          </div>
        </form>
      </aside>
    </>
  );
};
