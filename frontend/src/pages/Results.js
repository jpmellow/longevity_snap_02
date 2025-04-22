import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Divider,
  CircularProgress,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Avatar,
  Paper,
  Stack
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  DirectionsRun as ExerciseIcon,
  Restaurant as NutritionIcon,
  Nightlight as SleepIcon,
  SelfImprovement as StressIcon,
  Favorite as HeartIcon,
  Check as CheckIcon,
  Info as InfoIcon,
  Star as StarIcon
} from '@mui/icons-material';

const Results = () => {
  const { assessmentId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const [loading, setLoading] = useState(true);
  const [results, setResults] = useState(null);

  // Get name and age from location.state or localStorage
  const userName = location.state?.name || localStorage.getItem('assessmentName') || '';
  const userAge = location.state?.age || localStorage.getItem('assessmentAge') || '';

  useEffect(() => {
    // Simulate API call to get assessment results
    const fetchResults = async () => {
      try {
        // In a real app, this would be an API call using the assessmentId
        setTimeout(() => {
          setResults({
            id: assessmentId,
            date: "2023-05-15",
            longevityScore: 76,
            previousScore: 72,
            motivationDriver: "LONGEVITY",
            categoryScores: {
              sleep: 82,
              nutrition: 70,
              exercise: 75,
              stress: 65
            },
            insights: [
              {
                type: "motivation_driver",
                title: "Primary Motivation: Longevity",
                description: "Your health recommendations emphasize long-term health optimization and adding healthy years to your life",
                relevance: "high"
              },
              {
                type: "implementation_readiness",
                title: "High Implementation Readiness",
                description: "Your current lifestyle and preferences align well with the recommended changes, suggesting a smooth transition",
                relevance: "medium"
              },
              {
                type: "personalization_factors",
                title: "Key Personalization Factors",
                description: "Your recommendations have been tailored based on your age, sleep patterns, and activity level",
                factors: ["Age: 42", "Sleep Quality: Good", "Activity Level: Moderate"],
                relevance: "high"
              }
            ],
            recommendations: [
              {
                category: "sleep",
                title: "Optimize Sleep Schedule",
                description: "Maintain a consistent sleep schedule with 7-8 hours of quality sleep to support cellular repair and brain health.",
                priority: "high",
                evidence_level: "Strong",
                implementation_steps: [
                  "Set a consistent bedtime between 10-11pm",
                  "Create a 30-minute wind-down routine before bed",
                  "Keep your bedroom cool (65-68°F) and dark",
                  "Avoid screens 1 hour before bedtime"
                ],
                motivation_alignment: "Quality sleep is a fundamental pillar of longevity, supporting cellular repair and brain health"
              },
              {
                category: "nutrition",
                title: "Increase Plant Diversity",
                description: "Aim for 30+ different plant foods weekly to support gut microbiome diversity and reduce inflammation.",
                priority: "high",
                evidence_level: "Strong",
                implementation_steps: [
                  "Add 1-2 new vegetables or fruits to your shopping list each week",
                  "Include a variety of colors on your plate at each meal",
                  "Incorporate herbs and spices into your cooking",
                  "Try one new plant-based recipe weekly"
                ],
                motivation_alignment: "This dietary pattern is consistently associated with exceptional longevity in population studies"
              },
              {
                category: "exercise",
                title: "Add Strength Training",
                description: "Incorporate 2-3 strength training sessions weekly to preserve muscle mass and support metabolic health.",
                priority: "high",
                evidence_level: "Strong",
                implementation_steps: [
                  "Start with bodyweight exercises if you're new to strength training",
                  "Focus on compound movements (squats, pushups, rows)",
                  "Gradually increase resistance as you progress",
                  "Allow 48 hours recovery between sessions for the same muscle groups"
                ],
                motivation_alignment: "Regular physical activity is one of the strongest predictors of healthy lifespan"
              },
              {
                category: "stress",
                title: "Daily Mindfulness Practice",
                description: "Implement a daily 10-minute mindfulness practice to reduce chronic stress and improve stress resilience.",
                priority: "medium",
                evidence_level: "Moderate",
                implementation_steps: [
                  "Start with guided meditation using an app like Calm or Headspace",
                  "Begin with just 5 minutes daily and gradually increase",
                  "Try different techniques to find what works best for you",
                  "Schedule your practice at the same time each day"
                ],
                motivation_alignment: "Effective stress management protects your telomeres and slows biological aging"
              },
              {
                category: "sleep",
                title: "Optimize Sleep Environment",
                description: "Create an optimal sleep environment by minimizing disruptions and enhancing comfort.",
                priority: "medium",
                evidence_level: "Moderate",
                implementation_steps: [
                  "Invest in a quality mattress and pillows",
                  "Use blackout curtains to block light",
                  "Consider using white noise to mask disruptive sounds",
                  "Keep electronics out of the bedroom"
                ],
                motivation_alignment: "Quality sleep is a fundamental pillar of longevity, supporting cellular repair and brain health"
              },
              {
                category: "nutrition",
                title: "Reduce Ultra-Processed Foods",
                description: "Minimize consumption of ultra-processed foods to reduce inflammation and support metabolic health.",
                priority: "medium",
                evidence_level: "Strong",
                implementation_steps: [
                  "Read ingredient labels and avoid products with long lists of additives",
                  "Cook more meals at home using whole food ingredients",
                  "Prepare healthy snacks in advance to avoid convenience foods",
                  "Gradually replace processed items with whole food alternatives"
                ],
                motivation_alignment: "This dietary pattern is consistently associated with exceptional longevity in population studies"
              }
            ]
          });
          setLoading(false);
        }, 1500);
      } catch (error) {
        console.error("Error fetching results:", error);
        setLoading(false);
      }
    };

    fetchResults();
  }, [assessmentId]);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'sleep':
        return <SleepIcon sx={{ color: '#1976D2' }} />;
      case 'nutrition':
        return <NutritionIcon sx={{ color: '#2E7D32' }} />;
      case 'exercise':
        return <ExerciseIcon sx={{ color: '#FF9800' }} />;
      case 'stress':
        return <StressIcon sx={{ color: '#9C27B0' }} />;
      default:
        return <HeartIcon color="primary" />;
    }
  };

  const getCategoryColor = (category) => {
    switch (category) {
      case 'sleep':
        return '#1976D2'; // Blue
      case 'nutrition':
        return '#2E7D32'; // Green
      case 'exercise':
        return '#FF9800'; // Orange
      case 'stress':
        return '#9C27B0'; // Purple
      default:
        return '#2E7D32'; // Default to primary color
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return '#d32f2f'; // Red
      case 'medium':
        return '#f57c00'; // Orange
      case 'low':
        return '#388e3c'; // Green
      default:
        return '#757575'; // Grey
    }
  };

  const getEvidenceLevelColor = (level) => {
    switch (level) {
      case 'Strong':
        return '#388e3c'; // Green
      case 'Moderate':
        return '#f57c00'; // Orange
      case 'Limited':
        return '#757575'; // Grey
      default:
        return '#757575'; // Grey
    }
  };

  return (
    <Box>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          {userName ? `Great job, ${userName}!` : 'Great job!'}
        </Typography>
        {userAge && (
          <Typography variant="subtitle1" color="text.secondary">
            Age: {userAge}
          </Typography>
        )}
      </Box>
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Your Health Assessment Results
        </Typography>
        <Button 
          variant="outlined" 
          color="primary" 
          onClick={() => navigate('/')}
        >
          Back to Dashboard
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Longevity Score Card */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Your Longevity Score
              </Typography>
              <Box sx={{ 
                display: 'flex', 
                justifyContent: 'center', 
                alignItems: 'center', 
                flexDirection: 'column',
                my: 2 
              }}>
                <Box sx={{ 
                  position: 'relative', 
                  display: 'flex', 
                  justifyContent: 'center', 
                  alignItems: 'center' 
                }}>
                  <CircularProgress 
                    variant="determinate" 
                    value={results.longevityScore} 
                    size={160} 
                    thickness={5} 
                    sx={{ color: 'primary.main' }} 
                  />
                  <Box sx={{ 
                    position: 'absolute', 
                    display: 'flex', 
                    flexDirection: 'column', 
                    justifyContent: 'center', 
                    alignItems: 'center' 
                  }}>
                    <Typography variant="h3" component="div" color="primary.main" sx={{ fontWeight: 'bold' }}>
                      {results.longevityScore}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      out of 100
                    </Typography>
                  </Box>
                </Box>
                {results.previousScore && (
                  <Box sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
                    <Typography variant="body2" color="text.secondary">
                      +{results.longevityScore - results.previousScore} points since last assessment
                    </Typography>
                  </Box>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Category Scores Card */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Health Category Scores
              </Typography>
              <Grid container spacing={2} sx={{ mt: 1 }}>
                {Object.entries(results.categoryScores).map(([category, score]) => (
                  <Grid item xs={6} sm={3} key={category}>
                    <Paper 
                      elevation={0} 
                      sx={{ 
                        p: 2, 
                        textAlign: 'center',
                        border: '1px solid',
                        borderColor: 'divider',
                        borderRadius: 2
                      }}
                    >
                      <Avatar 
                        sx={{ 
                          bgcolor: getCategoryColor(category),
                          mx: 'auto',
                          mb: 1
                        }}
                      >
                        {getCategoryIcon(category)}
                      </Avatar>
                      <Typography variant="h5" sx={{ fontWeight: 'medium' }}>
                        {score}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ textTransform: 'capitalize' }}>
                        {category}
                      </Typography>
                    </Paper>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Insights Card */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Key Health Insights
              </Typography>
              <Grid container spacing={2} sx={{ mt: 1 }}>
                {results.insights.map((insight, index) => (
                  <Grid item xs={12} md={4} key={index}>
                    <Paper 
                      elevation={0} 
                      sx={{ 
                        p: 2,
                        height: '100%',
                        border: '1px solid',
                        borderColor: 'divider',
                        borderRadius: 2
                      }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <Avatar sx={{ bgcolor: 'primary.light', mr: 1.5 }}>
                          <InfoIcon />
                        </Avatar>
                        <Typography variant="h6" component="div">
                          {insight.title}
                        </Typography>
                      </Box>
                      <Typography variant="body2" paragraph>
                        {insight.description}
                      </Typography>
                      {insight.factors && (
                        <List dense disablePadding>
                          {insight.factors.map((factor, i) => (
                            <ListItem key={i} disablePadding sx={{ py: 0.5 }}>
                              <ListItemIcon sx={{ minWidth: 30 }}>
                                <CheckIcon fontSize="small" color="primary" />
                              </ListItemIcon>
                              <ListItemText primary={factor} />
                            </ListItem>
                          ))}
                        </List>
                      )}
                      <Chip 
                        size="small" 
                        label={`${insight.relevance} relevance`} 
                        color={insight.relevance === 'high' ? 'primary' : 'default'}
                        variant={insight.relevance === 'high' ? 'filled' : 'outlined'}
                        sx={{ mt: 1 }}
                      />
                    </Paper>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Recommendations Card */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Personalized Recommendations
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Based on your assessment, we've created the following personalized recommendations to optimize your health and longevity.
              </Typography>
              
              <Box sx={{ mt: 3 }}>
                {results.recommendations.map((recommendation, index) => (
                  <Accordion key={index} sx={{ mb: 2 }}>
                    <AccordionSummary
                      expandIcon={<ExpandMoreIcon />}
                      sx={{ 
                        borderLeft: '4px solid',
                        borderColor: getCategoryColor(recommendation.category)
                      }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                        <Avatar sx={{ bgcolor: getCategoryColor(recommendation.category), mr: 2 }}>
                          {getCategoryIcon(recommendation.category)}
                        </Avatar>
                        <Box sx={{ flexGrow: 1 }}>
                          <Typography variant="subtitle1" sx={{ fontWeight: 'medium' }}>
                            {recommendation.title}
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 1, mt: 0.5 }}>
                            <Chip 
                              size="small" 
                              label={`Priority: ${recommendation.priority}`} 
                              sx={{ bgcolor: getPriorityColor(recommendation.priority), color: 'white' }}
                            />
                            <Chip 
                              size="small" 
                              label={`Evidence: ${recommendation.evidence_level}`}
                              sx={{ bgcolor: getEvidenceLevelColor(recommendation.evidence_level), color: 'white' }}
                            />
                            <Chip 
                              size="small" 
                              label={recommendation.category} 
                              sx={{ bgcolor: getCategoryColor(recommendation.category), color: 'white' }}
                            />
                          </Box>
                        </Box>
                      </Box>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Box>
                        <Typography variant="body1" paragraph>
                          {recommendation.description}
                        </Typography>
                        
                        <Typography variant="subtitle2" sx={{ mt: 2, mb: 1, fontWeight: 'bold' }}>
                          Implementation Steps:
                        </Typography>
                        <List disablePadding>
                          {recommendation.implementation_steps.map((step, i) => (
                            <ListItem key={i} disablePadding sx={{ py: 0.5 }}>
                              <ListItemIcon sx={{ minWidth: 36 }}>
                                <Avatar sx={{ width: 24, height: 24, bgcolor: 'primary.main' }}>
                                  {i + 1}
                                </Avatar>
                              </ListItemIcon>
                              <ListItemText primary={step} />
                            </ListItem>
                          ))}
                        </List>
                        
                        <Box sx={{ 
                          mt: 2, 
                          p: 2, 
                          bgcolor: 'rgba(46, 125, 50, 0.08)', 
                          borderRadius: 2,
                          display: 'flex',
                          alignItems: 'center'
                        }}>
                          <StarIcon color="primary" sx={{ mr: 1 }} />
                          <Typography variant="body2">
                            <strong>Motivation Alignment:</strong> {recommendation.motivation_alignment}
                          </Typography>
                        </Box>
                      </Box>
                    </AccordionDetails>
                  </Accordion>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Results;
