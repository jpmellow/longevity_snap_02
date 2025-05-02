import React from 'react';
import { Modal, Box, Typography, TextField, Button } from '@mui/material';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #1976D2',
  boxShadow: 24,
  p: 4,
  borderRadius: 2,
  display: 'flex',
  flexDirection: 'column',
  gap: 2
};

const OpenAIApiKeyModal = ({ open, apiKey, setApiKey, onSubmit }) => (
  <Modal open={open} onClose={() => {}} disableEscapeKeyDown>
    <Box sx={style}>
      <Typography variant="h6" gutterBottom>
        Enter your OpenAI API Key
      </Typography>
      <TextField
        label="OpenAI API Key"
        type="password"
        value={apiKey}
        onChange={e => setApiKey(e.target.value)}
        fullWidth
        autoFocus
        onKeyDown={e => {
          if (e.key === 'Enter' && apiKey) {
            onSubmit();
          }
        }}
      />
      <Typography variant="caption" color="text.secondary">
        Your key is never stored or sent to any server except OpenAI.
      </Typography>
      <Button
        variant="contained"
        color="primary"
        onClick={() => {
          if (apiKey) onSubmit();
        }}
        disabled={!apiKey}
      >
        Continue
      </Button>
    </Box>
  </Modal>
);


export default OpenAIApiKeyModal;
