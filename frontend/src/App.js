import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Dashboard from './pages/Dashboard';
import Assessment from './pages/Assessment';
import Results from './pages/Results';
import History from './pages/History';
import AgentInsights from './pages/AgentInsights';
import Layout from './components/Layout';

// Create a theme with longevity-focused colors
const theme = createTheme({
  palette: {
    primary: {
      main: '#2E7D32', // Forest green - representing vitality and growth
      light: '#60ad5e',
      dark: '#005005',
    },
    secondary: {
      main: '#1976D2', // Blue - representing clarity and calm
      light: '#63a4ff',
      dark: '#004ba0',
    },
    background: {
      default: '#f5f7f9',
      paper: '#ffffff',
    },
    text: {
      primary: '#2c3e50',
      secondary: '#546e7a',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 500,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 500,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 500,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 500,
    },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
          padding: '8px 16px',
        },
        contained: {
          boxShadow: 'none',
          '&:hover': {
            boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.05)',
          borderRadius: 12,
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/assessment" element={<Assessment />} />
            <Route path="/results/:assessmentId" element={<Results />} />
            <Route path="/history" element={<History />} />
            <Route path="/agent-insights" element={<AgentInsights />} />
            <Route path="/health-coach-chat" element={React.createElement(require('./pages/HealthCoachChat').default)} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  );
}

export default App;
