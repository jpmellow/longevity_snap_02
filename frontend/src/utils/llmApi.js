// Utility for calling OpenAI's API (or similar LLM endpoints)
// Assumes the API key is provided by the user or via environment variable

export async function fetchLLMReply({ messages, apiKey, model = 'gpt-4' }) {
  const url = 'https://api.openai.com/v1/chat/completions';
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiKey}`,
  };
  const body = JSON.stringify({
    model,
    messages: messages.map(msg => ({
      role: msg.sender === 'user' ? 'user' : (msg.sender === 'coach' ? 'assistant' : 'system'),
      content: msg.text
    })),
    max_tokens: 512,
    temperature: 0.7
  });
  const response = await fetch(url, { method: 'POST', headers, body });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error?.message || 'Failed to fetch LLM reply');
  }
  const data = await response.json();
  return data.choices?.[0]?.message?.content || '[No response]';
}
