import React, { useState, useEffect } from 'react';
import { 
  useTheme, 
  Box, 
  Paper, 
  Typography, 
  Grid, 
  Button, 
  Tabs, 
  Tab, 
  Divider, 
  Avatar, 
  Chip,
  Card,
  CardContent,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  Tooltip,
  LinearProgress,
  Stack,
  alpha,
  StepLabel,
  List,
  ListItem,
  Stepper,
  Step
} from '@mui/material';
import { 
  LocalHospital as MedicalIcon,
  Psychology as NeurologyIcon,
  Psychology as PsychologyIcon,
  MonitorHeart as CardiologyIcon,
  Biotech as EndocrinologyIcon,
  Restaurant as NutritionIcon,
  Opacity as BiometricsIcon,
  Science as ScienceIcon,
  BiotechOutlined as BiomarkersIcon,
  Timeline as TrendsIcon,
  CompareArrows as ComparativeIcon,
  Memory as MemoryIcon,
  DataObject as ProcessingIcon,
  Insights as InsightsIcon,
  FilterAlt as FilterIcon,
  Analytics as AnalyticsIcon,
  DataUsage as DataUsageIcon,
  AccessTime as TimeIcon,
  Group as PopulationIcon,
  ArrowUpward as ImproveIcon,
  ArrowDownward as DeclineIcon,
  Sync as SyncIcon,
  MoreVert as MoreIcon,
  Lightbulb as LightbulbIcon,
  Assignment as AssignmentIcon,
  Check as CheckIcon,
  Info as InfoIcon,
  ExpandMore as ExpandMoreIcon,
  PlayArrow as PlayArrowIcon,
  Pause as PauseIcon,
  Settings as SettingsIcon,
  Timeline as TimelineIcon,
  Nightlight as SleepIcon
} from '@mui/icons-material';
import { 
  Chart as ChartJS, 
  RadialLinearScale, 
  PointElement, 
  LineElement, 
  ArcElement,
  Filler, 
  Tooltip as ChartTooltip, 
  Legend,
  CategoryScale,
  LinearScale
} from 'chart.js'; // (all used)
import { Radar, Line } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  ArcElement,
  ChartTooltip,
  Legend,
  CategoryScale,
  LinearScale
);

/**
 * Agent Insights Page - Advanced Analytics Dashboard
 * 
 * Features:
 * - Multi-agent AI architecture visualization
 * - Real-time agent communication simulation
 * - Multi-dimensional statistical analysis
 * - Explainable AI decision processes
 * - Predictive health modeling
 * 
 * This component implements a sophisticated AI agent network visualization
 * that shows how multiple specialized AI agents collaborate to analyze health data
 * and generate insights. It includes animations of the decision process,
 * statistical visualizations, and predictive modeling capabilities.
 */
const AgentInsights = () => {
  // State management
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState(0);
  const [insightsData, setInsightsData] = useState(null);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [confidenceMetrics, setConfidenceMetrics] = useState({});
  const [timeframeFilter, setTimeframeFilter] = useState('6months');
  const [processingStage, setProcessingStage] = useState(0);
  const [animateProcess, setAnimateProcess] = useState(false);
  const [agentMessages, setAgentMessages] = useState([]);
  const [predictiveModels, setPredictiveModels] = useState({});
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedMetric, setSelectedMetric] = useState('longevity');
  const [processStep, setProcessStep] = useState(0);
  const [loadingProgress, setLoadingProgress] = useState(0);
  
  // Tabs configuration
  const tabs = [
    { id: 'network', label: 'Agent Network', icon: <MemoryIcon /> },
    { id: 'sports', label: 'Sports Medicine', icon: <MedicalIcon /> },
    { id: 'insights', label: 'AI Insights', icon: <InsightsIcon /> },
    { id: 'process', label: 'Decision Process', icon: <ProcessingIcon /> },
    { id: 'stats', label: 'Statistical Analysis', icon: <AnalyticsIcon /> },
    { id: 'predictive', label: 'Predictive Models', icon: <TrendsIcon /> }
  ];
  
  // Processing stages for the decision pipeline
  const processingStages = [
    { id: 0, name: 'Data Collection', icon: <DataUsageIcon />, color: '#2196F3' },
    { id: 1, name: 'Pre-processing', icon: <FilterIcon />, color: '#9C27B0' },
    { id: 2, name: 'Feature Extraction', icon: <BiomarkersIcon />, color: '#FF9800' },
    { id: 3, name: 'Pattern Recognition', icon: <TimelineIcon />, color: '#4CAF50' },
    { id: 4, name: 'Analysis', icon: <AnalyticsIcon />, color: '#F44336' },
    { id: 5, name: 'Insight Generation', icon: <LightbulbIcon />, color: '#FFEB3B' },
    { id: 6, name: 'Recommendation', icon: <AssignmentIcon />, color: '#795548' }
  ];

  // Metrics for visualizations
  const healthMetrics = [
    { id: 'longevity', name: 'Longevity Score', color: '#4CAF50', domain: [0, 100] },
    { id: 'metabolic', name: 'Metabolic Health', color: '#2196F3', domain: [0, 100] },
    { id: 'cardiac', name: 'Cardiovascular', color: '#F44336', domain: [0, 100] },
    { id: 'neuro', name: 'Cognitive Health', color: '#9C27B0', domain: [0, 100] },
    { id: 'immune', name: 'Immune Function', color: '#FF9800', domain: [0, 100] },
    { id: 'stress', name: 'Stress Resilience', color: '#795548', domain: [0, 100] },
    { id: 'fitness', name: 'Physical Fitness', color: '#00BCD4', domain: [0, 100] }
  ];

  // Data processing steps for the loading animation
  const processingSteps = [
    'Initializing health data analysis...',
    'Loading patient biometric information...',
    'Activating AI agent network...',
    'Analyzing historical trends...',
    'Running predictive models...',
    'Generating personalized insights...',
    'Preparing visualization dashboard...',
    'Finalizing analysis results...'
  ];

  // Simulate data processing - guaranteed to reach 100%
  useEffect(() => {
    // Only run this effect once when component mounts
    if (loading) {
      // Set a longer duration (20 seconds for the whole animation)
      const progressMilestones = processingSteps.map((_, index) => 
        (index + 1) * (88 / processingSteps.length)
      );
      
      // Predetermined progress points with timing
      const progressPoints = [
        { progress: 0, delay: 0 },
        { progress: 10, delay: 1000 },
        { progress: 25, delay: 3000 },
        { progress: 45, delay: 4000 },
        { progress: 60, delay: 3000 },
        { progress: 75, delay: 3000 },
        { progress: 88, delay: 3000 },
        { progress: 95, delay: 2000 },
        { progress: 98, delay: 500 },
        { progress: 100, delay: 5000 }, // Long delay at 100%
      ];
      
      // Start at first point
      let currentPointIndex = 0;
      
      // Set first progress immediately
      setLoadingProgress(progressPoints[0].progress);
      
      // Function to process the next progress point
      const processNextPoint = () => {
        currentPointIndex++;
        
        // If we've gone through all points, finish
        if (currentPointIndex >= progressPoints.length) {
          // This is the final step - we've reached 100%
          // Wait 5 seconds (already included in the last delay) before hiding
          setLoading(false);
          return;
        }
        
        const currentPoint = progressPoints[currentPointIndex];
        
        // Update progress to this point's value
        setLoadingProgress(currentPoint.progress);
        
        // Update process step based on progress
        const newStep = progressMilestones.findIndex(milestone => 
          currentPoint.progress <= milestone
        );
        
        // Only update step if it's different and valid
        if (newStep !== -1 && newStep !== processStep) {
          setProcessStep(newStep);
        }
        
        // Schedule the next point after the delay
        setTimeout(processNextPoint, currentPoint.delay);
      };
      
      // Start the process
      processNextPoint();
    }
  }, [loading, processStep, processingSteps]);

  // Handle tab change
  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  // Handle menu open/close
  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  // Change timeframe filter
  const handleTimeframeChange = (timeframe) => {
    setTimeframeFilter(timeframe);
    handleMenuClose();
    fetchData();
  };

  // Select an agent for detailed view
  const handleAgentSelect = (agent) => {
    setSelectedAgent(agent === selectedAgent ? null : agent);
  };

  // Toggle animation of the decision process
  const toggleAnimation = () => {
    if (!animateProcess) {
      setProcessingStage(0);
      setAnimateProcess(true);
    } else {
      setAnimateProcess(false);
    }
  };

  // Generate predictive models for health metrics
  const generatePredictiveModels = () => {
    const timeframeMap = {
      '1month': 30,
      '3months': 90,
      '6months': 180,
      '1year': 365
    };
    
    const days = timeframeMap[timeframeFilter];
    const futureProjection = Math.floor(days * 0.7); // Project into the future
    
    // Generate datasets for each health metric
    const models = {};
    healthMetrics.forEach(metric => {
      // Historical data
      const historicalData = Array(days).fill().map((_, i) => {
        // Create some patterns with noise
        const base = 50 + Math.sin(i / 15) * 15 + Math.random() * 10;
        return {
          day: -days + i,
          value: Math.min(100, Math.max(0, base)) // Keep within 0-100 range
        };
      });
      
      // Predictive data - extend the pattern with increasing uncertainty
      const predictiveData = Array(futureProjection).fill().map((_, i) => {
        const lastValue = historicalData[historicalData.length - 1].value;
        const trend = (historicalData[historicalData.length - 1].value - historicalData[historicalData.length - 20].value) / 20;
        const projectedValue = lastValue + trend * i;
        const uncertainty = Math.min(30, 2 + (i / 10)); // Increasing uncertainty over time
        
        return {
          day: i + 1,
          value: projectedValue,
          upperBound: Math.min(100, projectedValue + uncertainty),
          lowerBound: Math.max(0, projectedValue - uncertainty)
        };
      });
      
      models[metric.id] = {
        historical: historicalData,
        predictive: predictiveData,
        trend: predictiveData[predictiveData.length - 1].value > historicalData[historicalData.length - 1].value ? 'improving' : 'declining'
      };
    });
    
    return models;
  };

  // Fetch all data for the dashboard
  const fetchData = async () => {
    setLoading(true);
    
    try {
      // In a real app, these would be API calls
      // Simulate API delay
      setTimeout(() => {
        setPredictiveModels(generatePredictiveModels());
        setInsightsData(generateInsightsData());
        setConfidenceMetrics(generateConfidenceMetrics());
        setLoading(false);
      }, 1500);
    } catch (error) {
      console.error('Error fetching agent insights data:', error);
      setLoading(false);
    }
  };

  // Generate insights data
  const generateInsightsData = () => {
    return {
      user: {
        id: 'user123',
        name: 'John Doe',
        age: 42,
        lastAssessment: new Date().toISOString()
      },
      summary: {
        longevityScore: 76,
        biologicalAge: 39,
        chronologicalAge: 42,
        healthSpan: 84.5,
        topRecommendations: 3,
        improvingMetrics: 4,
        decliningMetrics: 1,
        stableMetrics: 2
      },
      keyInsights: [
        {
          id: 'insight1',
          title: 'Sleep-Glucose Connection',
          description: 'Your sleep patterns are significantly impacting your glucose regulation. We detected a 68% correlation between sleep disruption and morning glucose spikes.',
          source: ['cardio', 'neuro', 'nutrition'],
          confidence: 89,
          impact: 'high',
          category: 'metabolic',
          recommendation: 'Consider shifting carbohydrate intake to earlier in the day and implement a consistent pre-sleep routine.'
        },
        {
          id: 'insight2',
          title: 'Cognitive Performance Pattern',
          description: 'Peak cognitive performance occurs between 10-11AM on days following physical exercise. Creative problem-solving metrics improved by 42%.',
          source: ['neuro', 'sports'],
          confidence: 76,
          impact: 'medium',
          category: 'cognitive',
          recommendation: 'Schedule cognitively demanding tasks for mid-morning, especially after days with physical activity.'
        },
        {
          id: 'insight3',
          title: 'Recovery Optimization',
          description: 'Your recovery metrics show incomplete recovery following high-intensity workouts, particularly when separated by less than 48 hours.',
          source: ['sports', 'cardio', 'biometrics'],
          confidence: 92,
          impact: 'high',
          category: 'fitness',
          recommendation: 'Implement 48-hour recovery windows after high-intensity training and prioritize nutrition timing.'
        }
      ],
      riskFactors: [
        {
          id: 'risk1',
          title: 'Glucose Variability',
          level: 'moderate',
          trend: 'improving',
          description: 'High glucose variability may increase risk of metabolic dysfunction. Your metrics show improvement over the last 30 days.',
          confidence: 88
        },
        {
          id: 'risk2',
          title: 'Sleep Consistency',
          level: 'moderate',
          trend: 'stable',
          description: 'Inconsistent sleep patterns may impact cognitive health and metabolic function. Your patterns show minimal change over time.',
          confidence: 91
        },
        {
          id: 'risk3',
          title: 'Cardiovascular Metrics',
          level: 'low',
          trend: 'stable',
          description: 'Cardiovascular metrics are within optimal ranges with no significant changes in recent months.',
          confidence: 95
        }
      ]
    };
  };

  // Generate confidence metrics for visualizations
  const generateConfidenceMetrics = () => {
    return {
      overall: 84,
      domains: {
        nutrition: 82,
        sleep: 89,
        physical: 90,
        metabolic: 79,
        cognitive: 85,
        cardiovascular: 88
      },
      data: {
        completeness: 92,
        consistency: 87,
        recency: 95,
        accuracy: 89,
        reliability: 83
      },
      insights: {
        general: 92,
        cardio: 87,
        neuro: 84,
        nutrition: 89,
        endocrine: 81,
        sports: 90,
        biometrics: 95
      }
    };
  };

  // Advance the processing stage for the animated decision process
  const advanceProcessingStage = () => {
    if (processingStage < processingStages.length - 1) {
      setProcessingStage(prev => prev + 1);
    } else {
      setProcessingStage(0); // Reset to beginning
    }
  };

  // Animation effect for decision process
  useEffect(() => {
    let timer;
    if (animateProcess) {
      timer = setInterval(() => {
        advanceProcessingStage();
      }, 1000);
    }
    
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [animateProcess, processingStage]);

  // Initial data fetch
  useEffect(() => {
    fetchData();
  }, [timeframeFilter]);
  
  // Simulated agents with specialties
  const agents = [
    {
      id: 'general',
      name: 'Medical Director',
      role: 'Orchestrator',
      specialty: 'System Integration',
      icon: <MedicalIcon />,
      color: '#2E7D32',
      confidence: 92,
      status: 'active',
      connections: ['cardio', 'neuro', 'nutrition', 'biometrics'],
      expertise: ['Risk Assessment', 'Multi-source Integration', 'Medical Literature'],
      description: 'Coordinates all specialist agents and synthesizes their insights into cohesive recommendations.'
    },
    {
      id: 'cardio',
      name: 'CardioAgent',
      role: 'Specialist',
      specialty: 'Cardiovascular Health',
      icon: <CardiologyIcon />,
      color: '#D32F2F',
      confidence: 87,
      status: 'active',
      connections: ['general', 'biometrics', 'sports'],
      expertise: ['Heart Rate Variability', 'Blood Pressure Patterns', 'Cardiovascular Risk'],
      description: 'Analyzes cardiovascular metrics and identifies patterns that may indicate heart health issues.'
    },
    {
      id: 'neuro',
      name: 'NeuroAgent',
      role: 'Specialist',
      specialty: 'Cognitive Function',
      icon: <NeurologyIcon />,
      color: '#7B1FA2',
      confidence: 84,
      status: 'active',
      connections: ['general', 'biometrics', 'nutrition'],
      expertise: ['Sleep Quality', 'Cognitive Performance', 'Stress Responses'],
      description: 'Focuses on brain health metrics and cognitive function indicators.'
    },
    {
      id: 'nutrition',
      name: 'NutriAgent',
      role: 'Specialist',
      specialty: 'Dietary Analysis',
      icon: <NutritionIcon />,
      color: '#1976D2',
      confidence: 89,
      status: 'active',
      connections: ['general', 'biometrics', 'endocrine'],
      expertise: ['Macronutrient Balance', 'Micronutrient Optimization', 'Metabolic Impact'],
      description: 'Evaluates dietary patterns and their impact on overall health and performance.'
    },
    {
      id: 'endocrine',
      name: 'EndoAgent',
      role: 'Specialist',
      specialty: 'Hormonal Balance',
      icon: <EndocrinologyIcon />,
      color: '#0097A7',
      confidence: 81,
      status: 'active',
      connections: ['general', 'nutrition', 'biometrics'],
      expertise: ['Glucose Regulation', 'Thyroid Function', 'Hormone Analysis'],
      description: 'Monitors hormonal patterns and their effects on energy, mood, and metabolism.'
    },
    {
      id: 'sports',
      name: 'KinesisAgent',
      role: 'Specialist',
      specialty: 'Movement Analysis',
      icon: <MedicalIcon />,
      color: '#FF9800',
      confidence: 90,
      status: 'active',
      connections: ['general', 'cardio', 'biometrics'],
      expertise: ['Movement Quality', 'Recovery Capacity', 'Performance Optimization'],
      description: 'Assesses physical performance metrics and movement efficiency.'
    },
    {
      id: 'biometrics',
      name: 'BiometricAgent',
      role: 'Data Processor',
      specialty: 'Biomarker Analysis',
      icon: <BiometricsIcon />,
      color: '#607D8B',
      confidence: 95,
      status: 'active',
      connections: ['general', 'cardio', 'neuro', 'nutrition', 'endocrine', 'sports'],
      expertise: ['Data Validation', 'Signal Processing', 'Anomaly Detection'],
      description: 'Processes raw biometric data and prepares it for specialized analysis.'
    }
  ];
  
  // Render the Agent Insights dashboard
  const theme = useTheme();

  return (
    <Box sx={{ pb: 4 }}>
      {loading ? (
        <Box 
          sx={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '80vh',
            textAlign: 'center',
            px: 2
          }}
        >
          <Typography variant="h4" sx={{ mb: 5, fontWeight: 'medium' }}>
            Preparing Your Health Intelligence Dashboard
          </Typography>
          
          <Box sx={{ width: '100%', maxWidth: 600, mb: 3 }}>
            <LinearProgress 
              variant="determinate" 
              value={loadingProgress} 
              sx={{
                height: 10,
                borderRadius: 5,
                backgroundColor: alpha(theme.palette.primary.main, 0.15),
                '& .MuiLinearProgress-bar': {
                  borderRadius: 5,
                  backgroundImage: `linear-gradient(90deg, ${theme.palette.primary.dark}, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                  transition: 'transform 0.4s cubic-bezier(0.65, 0.05, 0.36, 1)'
                }
              }}
            />
          </Box>
          
          <Typography variant="h6" color="primary" sx={{ mb: 1, fontWeight: 'medium' }}>
            {Math.round(loadingProgress)}% Complete
          </Typography>
          
          <Typography variant="body1" sx={{ mb: 4, maxWidth: 600 }}>
            {processingSteps[processStep]}
          </Typography>
          
          <Box sx={{ 
            display: 'flex', 
            gap: 2, 
            justifyContent: 'center',
            flexWrap: 'wrap',
            opacity: 0.7
          }}>
            <Chip 
              icon={<DataUsageIcon />} 
              label="Processing Biometric Data" 
              variant="outlined" 
              color="primary"
            />
            <Chip 
              icon={<AnalyticsIcon />} 
              label="Running Statistical Models" 
              variant="outlined" 
              color="primary"
            />
            <Chip 
              icon={<PsychologyIcon />} 
              label="AI Agent Activation" 
              variant="outlined" 
              color="primary"
            />
          </Box>
        </Box>
      ) : (
        <>
          {/* Page Header */}
          <Box sx={{ mb: 4 }}>
            <Typography variant="h4" component="h1" gutterBottom>
              Agent Insights Platform
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              Advanced AI agent network analyzing your health data to deliver personalized insights and recommendations.
            </Typography>
          </Box>
          
          {/* Loading State */}
          {/* Control Panel */}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Tabs 
              value={activeTab} 
              onChange={handleTabChange} 
              variant="scrollable"
              scrollButtons="auto"
            >
              {tabs.map(tab => (
                <Tab 
                  key={tab.id} 
                  label={tab.label} 
                  icon={tab.icon} 
                  iconPosition="start"
                />
              ))}
            </Tabs>
            
            <Box>
              <Button
                variant="outlined"
                startIcon={<TimeIcon />}
                onClick={handleMenuOpen}
                size="small"
                sx={{ mr: 1 }}
              >
                {timeframeFilter === '1month' ? '1 Month' :
                 timeframeFilter === '3months' ? '3 Months' :
                 timeframeFilter === '6months' ? '6 Months' : '1 Year'}
              </Button>
              
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleMenuClose}
              >
                <MenuItem onClick={() => handleTimeframeChange('1month')}>1 Month</MenuItem>
                <MenuItem onClick={() => handleTimeframeChange('3months')}>3 Months</MenuItem>
                <MenuItem onClick={() => handleTimeframeChange('6months')}>6 Months</MenuItem>
                <MenuItem onClick={() => handleTimeframeChange('1year')}>1 Year</MenuItem>
              </Menu>
              
              <Button
                variant="contained"
                startIcon={animateProcess ? <PauseIcon /> : <PlayArrowIcon />}
                onClick={toggleAnimation}
                color="primary"
                size="small"
              >
                {animateProcess ? 'Pause Simulation' : 'Start Simulation'}
              </Button>
            </Box>
          </Box>
          
          {/* Main Content */}
          <Box sx={{ mt: 2 }}>
            {/* Agent Network View */}
            {activeTab === 0 && (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Multi-Agent Intelligence Network
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Interactive visualization of specialized AI agents analyzing your health data in real-time.
                  </Typography>
                  
                  {/* Network Visualization - In a real app, this would use a library like react-flow */}
                  <Paper 
                    elevation={0} 
                    sx={{ 
                      height: 500, 
                      bgcolor: 'rgba(0,0,0,0.02)', 
                      p: 2, 
                      position: 'relative',
                      borderRadius: 2,
                      mb: 2
                    }}
                  >
                    {/* This is a placeholder for a proper network visualization */}
                    {/* In a real implementation, use react-flow or d3.js */}
                    {agents.map(agent => (
                      <Box
                        key={agent.id}
                        sx={{
                          position: 'absolute',
                          left: { x: 0, y: 0 },
                          width: agent.id === 'general' ? 120 : 100,
                          height: agent.id === 'general' ? 120 : 100,
                          bgcolor: agent.color,
                          color: 'white',
                          borderRadius: '50%',
                          display: 'flex',
                          flexDirection: 'column',
                          alignItems: 'center',
                          justifyContent: 'center',
                          cursor: 'pointer',
                          transition: 'all 0.3s ease',
                          transform: selectedAgent === agent ? 'scale(1.1)' : 'scale(1)',
                          boxShadow: selectedAgent === agent ? 
                            '0 0 0 4px rgba(255,255,255,0.8), 0 10px 20px rgba(0,0,0,0.19)' : 
                            '0 4px 8px rgba(0,0,0,0.1)',
                          zIndex: selectedAgent === agent ? 10 : 1,
                          '&:hover': {
                            transform: 'scale(1.05)',
                            boxShadow: '0 6px 12px rgba(0,0,0,0.15)'
                          }
                        }}
                        onClick={() => handleAgentSelect(agent)}
                      >
                        <Box sx={{ fontSize: 32, mb: 0.5 }}>
                          {agent.icon}
                        </Box>
                        <Typography variant="caption" sx={{ fontWeight: 'bold', fontSize: '0.7rem' }}>
                          {agent.name}
                        </Typography>
                        <Chip 
                          label={`${agent.confidence}%`} 
                          size="small" 
                          sx={{ 
                            height: 20, 
                            fontSize: '0.6rem', 
                            mt: 0.5, 
                            bgcolor: 'rgba(255,255,255,0.25)',
                            color: 'white'
                          }} 
                        />
                      </Box>
                    ))}
                    
                    {/* Edge Connections would be rendered here in a real implementation */}
                  </Paper>
                  
                  {/* Selected Agent Details */}
                  {selectedAgent && (
                    <Card variant="outlined" sx={{ mb: 2 }}>
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                          <Avatar sx={{ bgcolor: selectedAgent.color, mr: 2 }}>
                            {selectedAgent.icon}
                          </Avatar>
                          <Box>
                            <Typography variant="h6">{selectedAgent.name}</Typography>
                            <Typography variant="body2" color="text.secondary">
                              {selectedAgent.role} • {selectedAgent.specialty}
                            </Typography>
                          </Box>
                          <Box sx={{ ml: 'auto', display: 'flex', alignItems: 'center' }}>
                            <Chip 
                              label={`${selectedAgent.confidence}% Confidence`} 
                              color="primary" 
                              size="small" 
                              sx={{ mr: 1 }} 
                            />
                            <Chip 
                              label={selectedAgent.status} 
                              color="success" 
                              size="small" 
                            />
                          </Box>
                        </Box>
                        
                        <Typography variant="body2" paragraph>
                          {selectedAgent.description}
                        </Typography>
                        
                        <Typography variant="subtitle2" gutterBottom>
                          Areas of Expertise:
                        </Typography>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                          {selectedAgent.expertise.map(item => (
                            <Chip key={item} label={item} size="small" variant="outlined" />
                          ))}
                        </Box>
                        
                        <Typography variant="subtitle2" gutterBottom>
                          Connected Agents:
                        </Typography>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                          {selectedAgent.connections.map(connId => {
                            const connectedAgent = agents.find(a => a.id === connId);
                            if (!connectedAgent) return null;
                            return (
                              <Chip 
                                key={connId}
                                avatar={<Avatar sx={{ bgcolor: connectedAgent.color }}>{connectedAgent.icon}</Avatar>}
                                label={connectedAgent.name}
                                size="small"
                                variant="outlined"
                                onClick={() => handleAgentSelect(connectedAgent)}
                              />
                            );
                          })}
                        </Box>
                      </CardContent>
                    </Card>
                  )}
                  
                  {/* Agent Communication Feed */}
                  <Typography variant="h6" gutterBottom>
                    Real-time Agent Communication
                  </Typography>
                  <Paper variant="outlined" sx={{ p: 2, maxHeight: 400, overflow: 'auto' }}>
                    <List sx={{ width: '100%' }}>
                      {agentMessages.map(message => {
                        const agent = agents.find(a => a.id === message.agentId);
                        if (!agent) return null;
                        
                        return (
                          <ListItem 
                            key={message.id} 
                            alignItems="flex-start"
                            sx={{
                              mb: 2,
                              bgcolor: message.type === 'recommendation' ? 'rgba(46, 125, 50, 0.08)' : 'transparent',
                              borderRadius: 1
                            }}
                          >
                            <ListItemIcon sx={{ mt: 0 }}>
                              <Avatar sx={{ width: 24, height: 24, bgcolor: agent.color }}>
                                {agent.icon}
                              </Avatar>
                            </ListItemIcon>
                            <ListItemText
                              primary={
                                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                                  <Typography variant="subtitle2">{agent.name}</Typography>
                                  <Typography variant="caption" color="text.secondary">
                                    {new Date(message.timestamp).toLocaleTimeString()}
                                  </Typography>
                                </Box>
                              }
                              secondary={
                                <>
                                  <Typography
                                    component="span"
                                    variant="body2"
                                    color="text.primary"
                                    sx={{ display: 'block', mb: 0.5 }}
                                  >
                                    {message.content}
                                  </Typography>
                                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                                    <Chip 
                                      size="small" 
                                      label={`${message.confidence}% confidence`} 
                                      variant="outlined"
                                      sx={{ height: 20 }}
                                    />
                                    {message.referencesMessage && (
                                      <Typography variant="caption" color="text.secondary">
                                        References: {Array.isArray(message.referencesMessage) ? 
                                          message.referencesMessage.join(', ') : 
                                          message.referencesMessage}
                                      </Typography>
                                    )}
                                  </Box>
                                </>
                              }
                            />
                          </ListItem>
                        );
                      })}
                    </List>
                  </Paper>
                </CardContent>
              </Card>
            )}
            
            {/* AI Insights View */}
            {activeTab === 1 && insightsData && (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    AI-Generated Health Insights
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Key insights and patterns identified by our multi-agent AI system from your health data.
                  </Typography>
                  
                  {/* Summary Stats */}
                  <Grid container spacing={3} sx={{ mb: 4 }}>
                    <Grid item xs={12} sm={6} md={3}>
                      <Paper elevation={0} sx={{ p: 2, bgcolor: 'rgba(46, 125, 50, 0.08)', borderRadius: 2 }}>
                        <Typography variant="overline" display="block">Longevity Score</Typography>
                        <Typography variant="h3" sx={{ color: 'primary.main', fontWeight: 'bold' }}>
                          {insightsData.summary.longevityScore}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Biological Age: {insightsData.summary.biologicalAge} years
                        </Typography>
                      </Paper>
                    </Grid>
                    
                    <Grid item xs={12} sm={6} md={3}>
                      <Paper elevation={0} sx={{ p: 2, bgcolor: 'rgba(25, 118, 210, 0.08)', borderRadius: 2 }}>
                        <Typography variant="overline" display="block">Health Metrics</Typography>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Box>
                            <Typography variant="body2" sx={{ display: 'flex', alignItems: 'center' }}>
                              <ImproveIcon sx={{ fontSize: 16, color: 'success.main', mr: 0.5 }} />
                              {insightsData.summary.improvingMetrics} improving
                            </Typography>
                            <Typography variant="body2" sx={{ display: 'flex', alignItems: 'center' }}>
                              <MedicalIcon sx={{ fontSize: 42, color: '#1976d2' }} />
                              {insightsData.summary.decliningMetrics} declining
                            </Typography>
                          </Box>
                          <Box>
                            <Typography variant="body2" sx={{ display: 'flex', alignItems: 'center' }}>
                              <SyncIcon sx={{ fontSize: 16, color: 'info.main', mr: 0.5 }} />
                              {insightsData.summary.stableMetrics} stable
                            </Typography>
                          </Box>
                        </Box>
                      </Paper>
                    </Grid>
                    
                    <Grid item xs={12} sm={6} md={3}>
                      <Paper elevation={0} sx={{ p: 2, bgcolor: 'rgba(211, 47, 47, 0.08)', borderRadius: 2 }}>
                        <Typography variant="overline" display="block">Confidence Level</Typography>
                        <Typography variant="h3" sx={{ color: 'error.main', fontWeight: 'bold' }}>
                          {confidenceMetrics.overall}%
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Overall AI confidence in insights
                        </Typography>
                      </Paper>
                    </Grid>
                    
                    <Grid item xs={12} sm={6} md={3}>
                      <Paper elevation={0} sx={{ p: 2, bgcolor: 'rgba(123, 31, 162, 0.08)', borderRadius: 2 }}>
                        <Typography variant="overline" display="block">Healthspan</Typography>
                        <Typography variant="h3" sx={{ color: 'secondary.main', fontWeight: 'bold' }}>
                          {insightsData.summary.healthSpan}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Projected years of healthy life
                        </Typography>
                      </Paper>
                    </Grid>
                  </Grid>
                  
                  {/* Key Insights */}
                  <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
                    Top AI-Generated Insights
                  </Typography>
                  <Grid container spacing={3}>
                    {insightsData.keyInsights.map(insight => (
                      <Grid item xs={12} md={4} key={insight.id}>
                        <Card variant="outlined">
                          <CardContent>
                            <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', mb: 2 }}>
                              <Typography variant="subtitle1" component="div" sx={{ fontWeight: 'medium' }}>
                                {insight.title}
                              </Typography>
                              <Chip 
                                size="small" 
                                label={`${insight.confidence}%`}
                                color={insight.confidence > 85 ? 'success' : 'default'}
                              />
                            </Box>
                            
                            <Typography variant="body2" paragraph>
                              {insight.description}
                            </Typography>
                            
                            <Divider sx={{ my: 1.5 }} />
                            
                            <Box sx={{ mt: 2 }}>
                              <Typography variant="caption" color="text.secondary" gutterBottom display="block">
                                Contributing Agents:
                              </Typography>
                              <Stack direction="row" spacing={1}>
                                {insight.source.map(agentId => {
                                  const agent = agents.find(a => a.id === agentId);
                                  if (!agent) return null;
                                  return (
                                    <Tooltip key={agentId} title={agent.name}>
                                      <Avatar sx={{ width: 24, height: 24, bgcolor: agent.color }}>
                                        {agent.icon}
                                      </Avatar>
                                    </Tooltip>
                                  );
                                })}
                              </Stack>
                            </Box>
                            
                            <Box sx={{ 
                              mt: 2, 
                              p: 1.5, 
                              bgcolor: 'rgba(46, 125, 50, 0.08)', 
                              borderRadius: 1
                            }}>
                              <Typography variant="body2">
                                <strong>Recommendation:</strong> {insight.recommendation}
                              </Typography>
                            </Box>
                          </CardContent>
                        </Card>
                      </Grid>
                    ))}
                  </Grid>
                  
                  {/* Risk Factors */}
                  <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
                    Risk Assessment
                  </Typography>
                  <Grid container spacing={3}>
                    {insightsData.riskFactors.map(risk => (
                      <Grid item xs={12} md={4} key={risk.id}>
                        <Paper variant="outlined" sx={{ p: 2 }}>
                          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                            <Box sx={{ flexGrow: 1 }}>
                              <Typography variant="subtitle2">{risk.title}</Typography>
                              <Typography variant="caption" color="text.secondary" display="block">
                                Risk level: <strong>{risk.level}</strong>
                              </Typography>
                            </Box>
                            <Chip 
                              label={risk.trend} 
                              size="small" 
                              color={risk.trend === 'improving' ? 'success' : 
                                    risk.trend === 'declining' ? 'error' : 'default'}
                              icon={risk.trend === 'improving' ? <ImproveIcon /> : 
                                   risk.trend === 'declining' ? <DeclineIcon /> : <SyncIcon />}
                            />
                          </Box>
                          <Typography variant="body2">
                            {risk.description}
                          </Typography>
                          <LinearProgress 
                            variant="determinate" 
                            value={risk.confidence} 
                            sx={{ mt: 2, height: 6, borderRadius: 3 }} 
                          />
                          <Typography variant="caption" align="right" display="block" sx={{ mt: 0.5 }}>
                            {risk.confidence}% confidence
                          </Typography>
                        </Paper>
                      </Grid>
                    ))}
                  </Grid>
                </CardContent>
              </Card>
            )}
            
            {/* Decision Process View */}
            {activeTab === 2 && (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    AI Decision Process
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Visualization of how AI agents analyze your data to generate insights.
                  </Typography>
                  
                  {/* Processing Pipeline */}
                  <Box sx={{ my: 4 }}>
                    <Stepper activeStep={processingStage} alternativeLabel>
                      {processingStages.map((stage) => (
                        <Step key={stage.id} completed={processingStage >= stage.id}>
                          <StepLabel 
                            StepIconComponent={() => (
                              <Avatar
                                sx={{
                                  width: 40,
                                  height: 40,
                                  bgcolor: processingStage === stage.id ? 
                                    stage.color : 
                                    processingStage > stage.id ? 
                                      'success.main' : 
                                      'grey.300',
                                  color: processingStage >= stage.id ? 'white' : 'text.secondary',
                                  transition: 'all 0.5s ease'
                                }}
                              >
                                {processingStage > stage.id ? <CheckIcon /> : stage.icon}
                              </Avatar>
                            )}
                          >
                            {stage.name}
                          </StepLabel>
                        </Step>
                      ))}
                    </Stepper>
                  </Box>
                  
                  {/* Current Processing Stage Description */}
                  <Paper 
                    elevation={0} 
                    sx={{ 
                      p: 3, 
                      bgcolor: processingStages[processingStage].color + '10',
                      borderLeft: `4px solid ${processingStages[processingStage].color}`,
                      borderRadius: 2,
                      mb: 4 
                    }}
                  >
                    <Typography variant="h6" gutterBottom>
                      {processingStages[processingStage].name}
                    </Typography>
                    
                    {processingStage === 0 && (
                      <Typography variant="body2">
                        The system is collecting and organizing your health data from multiple sources, including wearable devices, 
                        manual input, and external health records. The Biometric Agent is validating data consistency and quality.
                      </Typography>
                    )}
                    
                    {processingStage === 1 && (
                      <Typography variant="body2">
                        Raw data is being cleaned, normalized, and structured. Outliers are identified, and missing values are 
                        imputed using statistical methods. Signal noise is filtered out to improve data quality.
                      </Typography>
                    )}
                    
                    {processingStage === 2 && (
                      <Typography variant="body2">
                        Key features and biomarkers are extracted from the preprocessed data. The system identifies important 
                        patterns and metrics that will be used for analysis, reducing dimensionality while preserving information.
                      </Typography>
                    )}
                    
                    {processingStage === 3 && (
                      <Typography variant="body2">
                        Specialized agents search for known patterns and correlations in your health data. Multiple pattern recognition 
                        algorithms run in parallel, each looking for specific signatures in different health domains.
                      </Typography>
                    )}
                    
                    {processingStage === 4 && (
                      <Typography variant="body2">
                        Identified patterns are analyzed in the context of scientific literature and population data. 
                        Each specialized agent applies domain-specific knowledge to interpret the findings and evaluate their significance.
                      </Typography>
                    )}
                    
                    {processingStage === 5 && (
                      <Typography variant="body2">
                        The Medical Director agent integrates analyses from all specialist agents to generate meaningful insights. 
                        Confidence levels are calculated based on data quality, pattern strength, and scientific evidence.
                      </Typography>
                    )}
                    
                    {processingStage === 6 && (
                      <Typography variant="body2">
                        Personalized recommendations are formulated based on the generated insights, taking into account your 
                        goals, preferences, and implementation capacity. The system prioritizes recommendations for maximum impact.
                      </Typography>
                    )}
                    
                    <Box sx={{ display: 'flex', mt: 2 }}>
                      <Button
                        variant="contained"
                        startIcon={animateProcess ? <PauseIcon /> : <PlayArrowIcon />}
                        onClick={toggleAnimation}
                        sx={{ mr: 2 }}
                      >
                        {animateProcess ? 'Pause' : 'Animate'} Process
                      </Button>
                      
                      <Button
                        variant="outlined"
                        onClick={advanceProcessingStage}
                        disabled={animateProcess}
                      >
                        Next Stage
                      </Button>
                    </Box>
                  </Paper>
                </CardContent>
              </Card>
            )}
            
            {/* Statistical Analysis View */}
            {activeTab === 3 && (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Multi-dimensional Statistical Analysis
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Advanced statistical analysis of your health data across multiple dimensions.
                  </Typography>
                  
                  {/* Summary Metrics */}
                  <Grid container spacing={3} sx={{ mb: 4 }}>
                    <Grid item xs={12} md={6}>
                      <Paper elevation={0} sx={{ p: 2, height: '100%', bgcolor: 'rgba(25, 118, 210, 0.05)', borderRadius: 2 }}>
                        <Typography variant="subtitle1" gutterBottom>Health Domain Analysis</Typography>
                        <Typography variant="body2" color="text.secondary" paragraph>
                          Radar chart showing health performance across key domains relative to optimal ranges.
                        </Typography>
                        
                        {/* Radar Chart */}
                        <Box sx={{ height: 350, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                          <Radar
                            data={{
                              labels: ['Metabolic', 'Cardiovascular', 'Cognitive', 'Immune', 'Physical', 'Recovery'],
                              datasets: [
                                {
                                  label: 'Your Metrics',
                                  data: [72, 85, 68, 78, 82, 65],
                                  backgroundColor: 'rgba(46, 125, 50, 0.2)',
                                  borderColor: 'rgba(46, 125, 50, 1)',
                                  pointBackgroundColor: 'rgba(46, 125, 50, 1)',
                                  pointBorderColor: '#fff',
                                  pointHoverBackgroundColor: '#fff',
                                  pointHoverBorderColor: 'rgba(46, 125, 50, 1)'
                                },
                                {
                                  label: 'Optimal Range',
                                  data: [85, 85, 85, 85, 85, 85],
                                  backgroundColor: 'rgba(66, 66, 66, 0.1)',
                                  borderColor: 'rgba(66, 66, 66, 0.5)',
                                  borderDash: [5, 5],
                                  pointBackgroundColor: 'rgba(66, 66, 66, 0.5)',
                                  pointBorderColor: '#fff',
                                  pointHoverBackgroundColor: '#fff',
                                  pointHoverBorderColor: 'rgba(66, 66, 66, 1)'
                                },
                                {
                                  label: 'Population Average',
                                  data: [65, 68, 62, 66, 70, 60],
                                  backgroundColor: 'rgba(25, 118, 210, 0.2)',
                                  borderColor: 'rgba(25, 118, 210, 1)',
                                  pointBackgroundColor: 'rgba(25, 118, 210, 1)',
                                  pointBorderColor: '#fff',
                                  pointHoverBackgroundColor: '#fff',
                                  pointHoverBorderColor: 'rgba(25, 118, 210, 1)'
                                }
                              ]
                            }}
                            options={{
                              elements: {
                                line: {
                                  tension: 0.2
                                }
                              },
                              scales: {
                                r: {
                                  angleLines: {
                                    display: true
                                  },
                                  suggestedMin: 0,
                                  suggestedMax: 100
                                }
                              }
                            }}
                          />
                        </Box>
                      </Paper>
                    </Grid>
                    
                    <Grid item xs={12} md={6}>
                      <Paper elevation={0} sx={{ p: 2, height: '100%', bgcolor: 'rgba(123, 31, 162, 0.05)', borderRadius: 2 }}>
                        <Typography variant="subtitle1" gutterBottom>Correlations Matrix</Typography>
                        <Typography variant="body2" color="text.secondary" paragraph>
                          Strength of relationships between different health metrics in your data.
                        </Typography>
                        
                        {/* Correlation Matrix */}
                        <Box sx={{ p: 2, overflowX: 'auto' }}>
                          <Grid container spacing={1}>
                            {/* Headers */}
                            <Grid item xs={3}></Grid>
                            {['Sleep', 'Stress', 'Activity', 'Nutrition', 'Glucose'].map((header, i) => (
                              <Grid item xs={1.8} key={`header-${i}`}>
                                <Typography variant="caption" sx={{ fontWeight: 'bold', display: 'block', textAlign: 'center' }}>
                                  {header}
                                </Typography>
                              </Grid>
                            ))}
                            
                            {/* Matrix Rows */}
                            {[
                              { name: 'Sleep', correlations: [1, -0.72, 0.48, 0.31, -0.65] },
                              { name: 'Stress', correlations: [-0.72, 1, -0.58, -0.22, 0.81] },
                              { name: 'Activity', correlations: [0.48, -0.58, 1, 0.41, -0.35] },
                              { name: 'Nutrition', correlations: [0.31, -0.22, 0.41, 1, -0.67] },
                              { name: 'Glucose', correlations: [-0.65, 0.81, -0.35, -0.67, 1] }
                            ].map((row, rowIndex) => (
                              <React.Fragment key={`row-${rowIndex}`}>
                                <Grid item xs={3}>
                                  <Typography variant="caption" sx={{ fontWeight: 'bold' }}>
                                    {row.name}
                                  </Typography>
                                </Grid>
                                {row.correlations.map((correlation, colIndex) => {
                                  // Color based on correlation strength
                                  let color = 'rgba(200, 200, 200, 0.3)';
                                  if (correlation === 1) {
                                    color = 'rgba(46, 125, 50, 0.7)';
                                  } else if (correlation > 0.6) {
                                    color = 'rgba(46, 125, 50, 0.5)';
                                  } else if (correlation > 0.3) {
                                    color = 'rgba(46, 125, 50, 0.3)';
                                  } else if (correlation < -0.6) {
                                    color = 'rgba(211, 47, 47, 0.5)';
                                  } else if (correlation < -0.3) {
                                    color = 'rgba(211, 47, 47, 0.3)';
                                  }
                                  
                                  return (
                                    <Grid item xs={1.8} key={`cell-${rowIndex}-${colIndex}`}>
                                      <Box sx={{
                                        height: 40,
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        bgcolor: color,
                                        borderRadius: 1,
                                        mb: 1,
                                        position: 'relative'
                                      }}>
                                        <Typography variant="caption" sx={{ fontWeight: 'bold' }}>
                                          {correlation.toFixed(2)}
                                        </Typography>
                                      </Box>
                                    </Grid>
                                  );
                                })}
                              </React.Fragment>
                            ))}
                          </Grid>
                          
                          <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-around' }}>
                            <Chip size="small" sx={{ bgcolor: 'rgba(46, 125, 50, 0.5)', color: 'white' }} label="Strong Positive" />
                            <Chip size="small" sx={{ bgcolor: 'rgba(200, 200, 200, 0.3)' }} label="Neutral" />
                            <Chip size="small" sx={{ bgcolor: 'rgba(211, 47, 47, 0.5)', color: 'white' }} label="Strong Negative" />
                          </Box>
                          
                          <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 2, textAlign: 'center' }}>
                            Matrix shows Pearson correlation coefficients (-1 to +1)
                          </Typography>
                        </Box>
                      </Paper>
                    </Grid>
                  </Grid>
                  
                  {/* AI-Generated Statistical Insights */}
                  <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
                    AI-Generated Statistical Insights
                  </Typography>
                  
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={4}>
                      <Paper variant="outlined" sx={{ p: 2 }}>
                        <Typography variant="subtitle2" gutterBottom>
                          Bivariate Relationship Analysis
                        </Typography>
                        <Typography variant="body2" paragraph>
                          Strong negative correlation (-0.72) between sleep quality and stress levels. Sleep fragmentation 
                          increases with higher reported stress, suggesting a bidirectional relationship.
                        </Typography>
                        <Chip 
                          size="small" 
                          color="primary" 
                          label="87% statistical confidence"
                          sx={{ mt: 1 }} 
                        />
                      </Paper>
                    </Grid>
                    
                    <Grid item xs={12} md={4}>
                      <Paper variant="outlined" sx={{ p: 2 }}>
                        <Typography variant="subtitle2" gutterBottom>
                          Multivariate Pattern Detection
                        </Typography>
                        <Typography variant="body2" paragraph>
                          Combination of high stress (&gt;75%), poor sleep quality (&lt;65%), and evening food intake creates a 
                          statistically significant effect on morning glucose levels (p=0.003).
                        </Typography>
                        <Chip 
                          size="small" 
                          color="primary" 
                          label="92% statistical confidence"
                          sx={{ mt: 1 }} 
                        />
                      </Paper>
                    </Grid>
                    
                    <Grid item xs={12} md={4}>
                      <Paper variant="outlined" sx={{ p: 2 }}>
                        <Typography variant="subtitle2" gutterBottom>
                          Cohort Comparative Analysis
                        </Typography>
                        <Typography variant="body2" paragraph>
                          Your cardiovascular metrics are in the top 15% of your age-matched demographic cohort, particularly 
                          in heart rate recovery and heart rate variability measures.
                        </Typography>
                        <Chip 
                          size="small" 
                          color="primary" 
                          label="94% statistical confidence"
                          sx={{ mt: 1 }} 
                        />
                      </Paper>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            )}
            
            {/* Predictive Models View */}
            {activeTab === 4 && (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Predictive Health Modeling
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    AI-powered predictive models showing projected health trajectories based on current data and trends.
                  </Typography>
                  
                  {/* Metric Selector */}
                  <Box sx={{ display: 'flex', gap: 2, mb: 3, flexWrap: 'wrap' }}>
                    {healthMetrics.map(metric => (
                      <Chip
                        key={metric.id}
                        label={metric.name}
                        onClick={() => setSelectedMetric(metric.id)}
                        color={selectedMetric === metric.id ? 'primary' : 'default'}
                        variant={selectedMetric === metric.id ? 'filled' : 'outlined'}
                        sx={{ px: 1 }}
                      />
                    ))}
                  </Box>
                  
                  {/* Predictive Chart */}
                  {predictiveModels[selectedMetric] && (
                    <Paper elevation={0} sx={{ p: 2, bgcolor: 'rgba(0,0,0,0.02)', borderRadius: 2, mb: 3 }}>
                      <Box sx={{ height: 400, mb: 3 }}>
                        <Line
                          data={{
                            datasets: [
                              {
                                label: 'Historical Data',
                                data: predictiveModels[selectedMetric].historical.map(point => ({
                                  x: point.day,
                                  y: point.value
                                })),
                                borderColor: 'rgba(25, 118, 210, 1)',
                                backgroundColor: 'rgba(25, 118, 210, 0.1)',
                                pointRadius: 0,
                                borderWidth: 2,
                                fill: false,
                                tension: 0.4
                              },
                              {
                                label: 'Predicted Trend',
                                data: predictiveModels[selectedMetric].predictive.map(point => ({
                                  x: point.day,
                                  y: point.value
                                })),
                                borderColor: 'rgba(46, 125, 50, 1)',
                                backgroundColor: 'rgba(46, 125, 50, 0.1)',
                                borderDash: [5, 5],
                                pointRadius: 0,
                                borderWidth: 2,
                                fill: false,
                                tension: 0.4
                              },
                              {
                                label: 'Uncertainty Range',
                                data: predictiveModels[selectedMetric].predictive.flatMap(point => [
                                  { x: point.day, y: point.lowerBound },
                                  { x: point.day, y: point.upperBound }
                                ]),
                                borderColor: 'transparent',
                                backgroundColor: 'rgba(46, 125, 50, 0.1)',
                                pointRadius: 0,
                                fill: true,
                                tension: 0.4
                              }
                            ]
                          }}
                          options={{
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                              x: {
                                type: 'linear',
                                position: 'bottom',
                                title: {
                                  display: true,
                                  text: 'Days (Past to Future)'
                                },
                                grid: {
                                  display: false
                                },
                                ticks: {
                                  callback: function(value) {
                                    if (value === 0) return 'Today';
                                    if (value < 0) return value + 'd';
                                    return '+' + value + 'd';
                                  }
                                }
                              },
                              y: {
                                min: 0,
                                max: 100,
                                title: {
                                  display: true,
                                  text: healthMetrics.find(m => m.id === selectedMetric)?.name || 'Value'
                                }
                              }
                            },
                            plugins: {
                              tooltip: {
                                mode: 'index',
                                intersect: false,
                                callbacks: {
                                  label: function(context) {
                                    if (context.dataset.label === 'Uncertainty Range') return null;
                                    return context.dataset.label + ': ' + context.parsed.y.toFixed(1);
                                  }
                                }
                              },
                              annotation: {
                                annotations: {
                                  line1: {
                                    type: 'line',
                                    xMin: 0,
                                    xMax: 0,
                                    borderColor: 'rgba(0, 0, 0, 0.5)',
                                    borderWidth: 2,
                                    borderDash: [6, 6],
                                    label: {
                                      display: true,
                                      content: 'Today',
                                      position: 'start'
                                    }
                                  }
                                }
                              }
                            }
                          }}
                        />
                      </Box>
                      
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Box>
                          <Typography variant="subtitle2">
                            {healthMetrics.find(m => m.id === selectedMetric)?.name} Prediction
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Based on {timeframeFilter === '1month' ? '30' : 
                                     timeframeFilter === '3months' ? '90' : 
                                     timeframeFilter === '6months' ? '180' : '365'} days of historical data
                          </Typography>
                        </Box>
                        <Chip 
                          label={predictiveModels[selectedMetric].trend === 'improving' ? 'Improving Trend' : 'Declining Trend'}
                          color={predictiveModels[selectedMetric].trend === 'improving' ? 'success' : 'error'}
                          icon={predictiveModels[selectedMetric].trend === 'improving' ? <ImproveIcon /> : <DeclineIcon />}
                          size="small"
                        />
                      </Box>
                    </Paper>
                  )}
                  
                  {/* What-If Scenarios */}
                  <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
                    What-If Scenario Analysis
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Explore how implementing different interventions could impact your future health trajectory.
                  </Typography>
                  
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={4}>
                      <Paper variant="outlined" sx={{ p: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                          <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                            <SleepIcon />
                          </Avatar>
                          <Typography variant="subtitle1">
                            Sleep Optimization
                          </Typography>
                        </Box>
                        <Typography variant="body2" paragraph>
                          Improving sleep consistency and quality to 85% optimal could improve your Cognitive Health score by 14-18% 
                          and Metabolic Health by 8-10% within 60 days.
                        </Typography>
                        <Button variant="outlined" size="small" startIcon={<AnalyticsIcon />} fullWidth>
                          View Simulation
                        </Button>
                      </Paper>
                    </Grid>
                    
                    <Grid item xs={12} md={4}>
                      <Paper variant="outlined" sx={{ p: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                          <Avatar sx={{ bgcolor: 'error.main', mr: 2 }}>
                            <MedicalIcon />
                          </Avatar>
                          <Typography variant="subtitle1">
                            Exercise Protocol
                          </Typography>
                        </Box>
                        <Typography variant="body2" paragraph>
                          Adding 2 more strength training sessions weekly could improve your Cardiovascular score by 12-15% 
                          and Physical Fitness by 18-22% within 90 days.
                        </Typography>
                        <Button variant="outlined" size="small" startIcon={<AnalyticsIcon />} fullWidth>
                          View Simulation
                        </Button>
                      </Paper>
                    </Grid>
                    
                    <Grid item xs={12} md={4}>
                      <Paper variant="outlined" sx={{ p: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                          <Avatar sx={{ bgcolor: 'success.main', mr: 2 }}>
                            <NutritionIcon />
                          </Avatar>
                          <Typography variant="subtitle1">
                            Nutrition Shift
                          </Typography>
                        </Box>
                        <Typography variant="body2" paragraph>
                          Shifting to a Mediterranean diet pattern could improve your Immune Function score by 10-12% 
                          and Cardiovascular score by 7-9% within 120 days.
                        </Typography>
                        <Button variant="outlined" size="small" startIcon={<AnalyticsIcon />} fullWidth>
                          View Simulation
                        </Button>
                      </Paper>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            )}
            
            {/* Placeholder for any remaining tabs */}
            {activeTab > 4 && (
              <Card>
                <CardContent sx={{ textAlign: 'center', py: 8 }}>
                  <Typography variant="h6" gutterBottom>
                    {tabs[activeTab].label} View
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    This view is part of the complete implementation but is not shown in this demo.
                  </Typography>
                  <Button variant="outlined" onClick={() => setActiveTab(0)}>
                    Return to Agent Network
                  </Button>
                </CardContent>
              </Card>
            )}
          </Box>
        </>
      )}
    </Box>
  );
};

export default AgentInsights;
