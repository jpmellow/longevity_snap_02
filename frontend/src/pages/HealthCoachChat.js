import React, { useState, useRef } from 'react';
import { Box, Typography, Paper, TextField, Button, CircularProgress, Stack } from '@mui/material';

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
  return `You are a longevity health coach. Here is a summary of the user's assessment:\n\n` +
    `Age: ${assessment.age}\n` +
    `Gender: ${assessment.gender}\n` +
    `Longevity Score: ${assessment.longevityScore}\n` +
    `Previous Score: ${assessment.previousScore}\n` +
    `Motivation Driver: ${assessment.motivationDriver}\n` +
    `Category Scores: Sleep ${assessment.categoryScores.sleep}, Nutrition ${assessment.categoryScores.nutrition}, Exercise ${assessment.categoryScores.exercise}, Stress ${assessment.categoryScores.stress}\n` +
    `NLP Area: ${assessment.nlp_area}\n` +
    `NLP Recommendation: ${assessment.nlp_recommendation}\n` +
    (assessment.insights.length > 0 ? `Key Insights: ${assessment.insights.map(i => i.title + ': ' + i.description).join('; ')}\n` : '') +
    (assessment.recommendations.length > 0 ? `Recommendations: ${assessment.recommendations.map(r => r.category + ' - ' + r.title + ': ' + r.description).join('; ')}\n` : '') +
    `\nBegin the conversation by greeting the user and offering to answer questions or provide personalized longevity advice based on their results.`;
}

const HealthCoachChat = () => {
  const [messages, setMessages] = useState([
    { sender: 'system', text: buildInitialPrompt(mockAssessment) }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  // Placeholder for LLM integration
  const sendMessage = async () => {
    if (!input.trim()) return;
    setMessages(prev => [...prev, { sender: 'user', text: input }]);
    setLoading(true);
    setInput('');
    // Simulate LLM response
    setTimeout(() => {
      setMessages(prev => [...prev, { sender: 'coach', text: "[LLM reply placeholder]" }]);
      setLoading(false);
    }, 1200);
  };

  return (
    <Box sx={{ maxWidth: 700, mx: 'auto', mt: 4, p: 2 }}>
      <Typography variant="h4" gutterBottom>Consult with Health Coach</Typography>
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
        />
        <Button variant="contained" color="success" onClick={sendMessage} disabled={loading}>
          Send
        </Button>
      </Box>
    </Box>
  );
};

export default HealthCoachChat;
