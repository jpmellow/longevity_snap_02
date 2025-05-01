import React from 'react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import { 
  AppBar, 
  Box, 
  Drawer, 
  Toolbar, 
  Typography, 
  List, 
  ListItem, 
  ListItemIcon, 
  ListItemText,
  Container,
  Divider,
  Avatar
} from '@mui/material';
import { 
  Dashboard as DashboardIcon, 
  Assessment as AssessmentIcon, 
  History as HistoryIcon,
  Person as PersonIcon,
  Settings as SettingsIcon,
  Psychology as PsychologyIcon
} from '@mui/icons-material';

const drawerWidth = 240;

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
  { text: 'Take Assessment', icon: <AssessmentIcon />, path: '/assessment' },
  { text: 'My Assessment Report', icon: <AssessmentIcon />, path: '/results/a123456' },
  { text: 'History', icon: <HistoryIcon />, path: '/history' },
  { text: 'Agent Insights', icon: <PsychologyIcon />, path: '/agent-insights' },
];

const Layout = ({ children }) => {
  const location = useLocation();

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar 
        position="fixed" 
        sx={{ 
          width: `calc(100% - ${drawerWidth}px)`, 
          ml: `${drawerWidth}px`,
          boxShadow: 'none',
          backgroundColor: 'background.paper',
          color: 'text.primary',
          borderBottom: '1px solid',
          borderColor: 'divider'
        }}
      >
        <Toolbar>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            {menuItems.find(item => item.path === location.pathname)?.text || 'Longevity Snapshot'}
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
            backgroundColor: 'background.paper',
            borderRight: '1px solid',
            borderColor: 'divider'
          },
        }}
        variant="permanent"
        anchor="left"
      >
        <Box sx={{ 
          display: 'flex', 
          flexDirection: 'column', 
          alignItems: 'center', 
          py: 3,
          backgroundColor: 'primary.main',
          color: 'white'
        }}>
          <Avatar 
            sx={{ 
              width: 80, 
              height: 80, 
              mb: 1, 
              bgcolor: 'primary.light',
              border: '3px solid',
              borderColor: 'white'
            }}
          >
            <PersonIcon fontSize="large" />
          </Avatar>
          <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
            Longevity Snapshot
          </Typography>
          <Typography variant="body2" sx={{ opacity: 0.8 }}>
            Your path to optimal health
          </Typography>
        </Box>
        <Divider />
        <List>
          {menuItems.map((item) => (
            <ListItem 
              button 
              key={item.text} 
              component={RouterLink} 
              to={item.path}
              selected={location.pathname === item.path}
              sx={{
                '&.Mui-selected': {
                  backgroundColor: 'primary.light',
                  color: 'white',
                  '& .MuiListItemIcon-root': {
                    color: 'white',
                  },
                  '&:hover': {
                    backgroundColor: 'primary.light',
                  }
                },
                '&:hover': {
                  backgroundColor: 'rgba(46, 125, 50, 0.08)',
                }
              }}
            >
              <ListItemIcon sx={{ 
                color: location.pathname === item.path ? 'white' : 'primary.main' 
              }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItem>
          ))}
        </List>
        <Divider />
        <Box sx={{ flexGrow: 1 }} />
        <List>
          <ListItem button>
            <ListItemIcon>
              <SettingsIcon />
            </ListItemIcon>
            <ListItemText primary="Settings" />
          </ListItem>
        </List>
      </Drawer>
      <Box
        component="main"
        sx={{ 
          flexGrow: 1, 
          p: 3, 
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          backgroundColor: 'background.default',
          minHeight: '100vh'
        }}
      >
        <Toolbar />
        <Container maxWidth="lg" sx={{ py: 2 }}>
          {children}
        </Container>
      </Box>
    </Box>
  );
};

export default Layout;
