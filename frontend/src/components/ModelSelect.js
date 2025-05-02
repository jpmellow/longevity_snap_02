import React from 'react';
import { Box, Typography, MenuItem, FormControl, InputLabel, Select, Button } from '@mui/material';

const MODEL_OPTIONS = [
  { label: 'GPT-4o (recommended)', value: 'gpt-4o' },
  { label: 'GPT-4', value: 'gpt-4' },
  { label: 'GPT-3.5-turbo', value: 'gpt-3.5-turbo' },
];

export default function ModelSelect({ model, setModel, onProceed, disabled }) {
  return (
    <Box sx={{ mt: 2, mb: 2, maxWidth: 400 }}>
      <Typography variant="h6" gutterBottom>Select a Language Model</Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
        Only OpenAI models are supported. Please enter your OpenAI API key before selecting a model.
      </Typography>
      <FormControl fullWidth disabled={disabled}>
        <InputLabel id="model-select-label">Model</InputLabel>
        <Select
          labelId="model-select-label"
          value={model}
          label="Model"
          onChange={e => setModel(e.target.value)}
        >
          {MODEL_OPTIONS.map(opt => (
            <MenuItem key={opt.value} value={opt.value}>{opt.label}</MenuItem>
          ))}
        </Select>
      </FormControl>
      <Button
        sx={{ mt: 2 }}
        variant="contained"
        color="primary"
        onClick={onProceed}
        disabled={!model || disabled}
      >
        Proceed
      </Button>
    </Box>
  );
}
