import React, { useState, useRef } from 'react';
import { Box, Typography, Paper, TextField, Button, CircularProgress, Stack, Alert } from '@mui/material';
import { fetchLLMReply } from '../utils/llmApi';
import OpenAIApiKeyModal from '../components/OpenAIApiKeyModal';

const mockAssessment = {
  age: 42,
  gender: 'male',
  longevityScore: 76,
  previousScore: 72,
  motivationDriver: 'LONGEVITY',
  categoryScores: {
    sleep: 82,
    nutrition: 70,
    exercise: 75,
    stress: 65
  },
  nlp_area: 'schedule',
  nlp_recommendation: 'Try to maintain a consistent sleep schedule, even on weekends.',
  insights: [
    {
      title: 'Primary Motivation: Longevity',
      description: 'Your health recommendations emphasize long-term health optimization and adding healthy years to your life.'
    },
    {
      title: 'High Implementation Readiness',
      description: 'Your current lifestyle and preferences align well with the recommended changes, suggesting a smooth transition.'
    },
    {
      title: 'Key Personalization Factors',
      description: 'Your recommendations have been tailored based on your age, sleep patterns, and activity level.'
    }
  ],
  recommendations: [
    {
      category: 'sleep',
      title: 'Optimize Sleep Schedule',
      description: 'Maintain a consistent sleep schedule with 7-8 hours of quality sleep to support cellular repair and brain health.'
    },
    {
      category: 'nutrition',
      title: 'Increase Plant Diversity',
      description: 'Aim for 30+ different plant foods weekly to support gut microbiome diversity and reduce inflammation.'
    }
  ]
};

function buildInitialPrompt(assessment) {
  return (
    `You are a health coach consulting a user about their longevity score and how to maximize their healthy lifespan. Use the values below to provide actionable, personalized advice about nutrition, sleep, exercise, and stress management.\n\n` +
    `User Assessment:\n` +
    `- Age: ${assessment.age}\n` +
    `- Gender: ${assessment.gender}\n` +
    `- Longevity Score: ${assessment.longevityScore}\n` +
    `- Sleep Score: ${assessment.categoryScores.sleep}\n` +
    `- Nutrition Score: ${assessment.categoryScores.nutrition}\n` +
    `- Exercise Score: ${assessment.categoryScores.exercise}\n` +
    `- Stress Score: ${assessment.categoryScores.stress}\n\n` +
    `Begin by greeting the user and briefly explaining what their longevity score means. Then, offer specific recommendations for improving their longevity based on the scores above.`
  );
}

const HealthCoachChat = () => {
  const [messages, setMessages] = useState([
    { sender: 'system', text: buildInitialPrompt(mockAssessment) }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [pendingApiKey, setPendingApiKey] = useState('');
  const [error, setError] = useState('');
  const chatEndRef = useRef(null);

  const sendMessage = async () => {
    if (!input.trim() || !apiKey) return;
    setMessages(prev => [...prev, { sender: 'user', text: input }]);
    setLoading(true);
    setError('');
    setInput('');
    try {
      const reply = await fetchLLMReply({ messages: [...messages, { sender: 'user', text: input }], apiKey });
      setMessages(prev => [...prev, { sender: 'coach', text: reply }]);
    } catch (err) {
      setMessages(prev => [...prev, { sender: 'coach', text: '[Error: ' + err.message + ']' }]);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 700, mx: 'auto', mt: 4, p: 2 }}>
      <Typography variant="h4" gutterBottom>Consult with Health Coach</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Paper variant="outlined" sx={{ minHeight: 400, maxHeight: 500, overflowY: 'auto', p: 2, mb: 2 }}>
        <Stack spacing={2}>
          {messages.map((msg, idx) => (
            <Box key={idx} alignSelf={msg.sender === 'user' ? 'flex-end' : 'flex-start'}>
              <Typography variant="body2" color={msg.sender === 'user' ? 'primary' : 'secondary'}>
                <b>{msg.sender === 'user' ? 'You' : msg.sender === 'coach' ? 'Health Coach' : 'System'}:</b> {msg.text}
              </Typography>
            </Box>
          ))}
          {loading && <CircularProgress size={20} />}
          <div ref={chatEndRef} />
        </Stack>
      </Paper>
      <Box sx={{ display: 'flex', gap: 2 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Type your question..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => { if (e.key === 'Enter') sendMessage(); }}
          disabled={loading || !apiKey}
        />
        <Button variant="contained" color="success" onClick={sendMessage} disabled={loading || !apiKey}>
          Send
        </Button>
      </Box>
      <OpenAIApiKeyModal
        open={!apiKey}
        apiKey={pendingApiKey}
        setApiKey={setPendingApiKey}
        onSubmit={() => {
          setApiKey(pendingApiKey);
          setMessages([{ sender: 'system', text: buildInitialPrompt(mockAssessment) }]);
        }}
      />
    </Box>
  );
};

export default HealthCoachChat;
