import { useState, useCallback, useRef } from 'react';
import { ChatSSEEvent, CitationRef, ImpactDelta } from '../types';
import { ChatMessage } from '../components/VayuChatDrawer';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export function useChat(lat: number, lon: number) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState<boolean>(false);
  const abortRef = useRef<AbortController | null>(null);

  const sendMessage = useCallback(
    async (userText: string) => {
      const userMsg: ChatMessage = {
        id: `user-${Date.now()}`,
        sender: 'user',
        text: userText,
      };

      setMessages((prev) => [...prev, userMsg]);
      setIsStreaming(true);

      const assistantId = `assistant-${Date.now()}`;
      let accumulatedText = '';
      let citations: CitationRef[] = [];
      let impact: ImpactDelta | undefined;

      const controller = new AbortController();
      abortRef.current = controller;

      try {
        const resp = await fetch(`${API_BASE}/api/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: userText, lat, lon }),
          signal: controller.signal,
        });

        if (!resp.ok) {
          const errData = await resp.json().catch(() => ({ detail: 'Chat request failed.' }));
          throw new Error(errData.detail || `Server error (${resp.status})`);
        }

        const reader = resp.body?.getReader();
        const decoder = new TextDecoder();
        if (!reader) throw new Error('Readable stream not supported.');

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunkText = decoder.decode(value, { stream: true });
          const lines = chunkText.split('\n');

          for (const line of lines) {
            if (!line.startsWith('data: ')) continue;
            const payload = line.slice(6).trim();
            if (!payload) continue;

            try {
              const event: ChatSSEEvent = JSON.parse(payload);
              if (event.event === 'token' && event.content) {
                accumulatedText += event.content;
                setMessages((prev) => {
                  const existingIdx = prev.findIndex((m) => m.id === assistantId);
                  if (existingIdx !== -1) {
                    const copy = [...prev];
                    copy[existingIdx] = {
                      ...copy[existingIdx],
                      text: accumulatedText,
                      citations,
                      impact,
                    };
                    return copy;
                  } else {
                    return [
                      ...prev,
                      {
                        id: assistantId,
                        sender: 'assistant',
                        text: accumulatedText,
                        citations,
                        impact,
                      },
                    ];
                  }
                });
              } else if (event.event === 'citation' && event.citations) {
                citations = event.citations;
              } else if (event.event === 'impact' && event.impact) {
                impact = event.impact;
              }
            } catch {
              // Ignore partial JSON lines
            }
          }
        }
      } catch (err: unknown) {
        if ((err as Error).name !== 'AbortError') {
          setMessages((prev) => [
            ...prev,
            {
              id: `err-${Date.now()}`,
              sender: 'assistant',
              text: `⚠️ ${(err as Error).message || 'Sorry, I encountered an issue. Please try rephrasing your question.'}`,
            },
          ]);
        }
      } finally {
        setIsStreaming(false);
        abortRef.current = null;
      }
    },
    [lat, lon]
  );

  return { messages, isStreaming, sendMessage };
}
