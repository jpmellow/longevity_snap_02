import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Box, 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  Button, 
  Divider,
  CircularProgress,
  LinearProgress,
  Stack,
  Avatar
} from '@mui/material';
import { 
  DirectionsRun as ExerciseIcon,
  Restaurant as NutritionIcon,
  Nightlight as SleepIcon,
  SelfImprovement as StressIcon,
  Favorite as HeartIcon,
  Timeline as ProgressIcon,
  Assessment as AssessmentIcon
} from '@mui/icons-material';
import { Doughnut, Line } from 'react-chartjs-2';
import { 
  Chart as ChartJS, 
  ArcElement, 
  Tooltip, 
  Legend, 
  CategoryScale, 
  LinearScale, 
  PointElement, 
  LineElement, 
  Title,
  Filler
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Filler
);

const Dashboard = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userData, setUserData] = useState(null);
  const [latestAssessment, setLatestAssessment] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Simulate API call to get user data and latest assessment
        await new Promise(resolve => setTimeout(resolve, 1000)); // Add a small delay to simulate API call
        
        setUserData({
          name: "Alex Johnson",
          age: 42,
          longevityScore: 76,
          motivationDriver: "LONGEVITY",
          lastAssessment: "2023-05-15",
          assessmentCount: 3
        });
        
        setLatestAssessment({
          id: "a123456",
          date: "2023-05-15",
          longevityScore: 76,
          previousScore: 72,
          categoryScores: {
            sleep: 82,
            nutrition: 70,
            exercise: 75,
            stress: 65
          },
          topRecommendations: [
            {
              category: "sleep",
              title: "Optimize Sleep Schedule",
              description: "Maintain a consistent sleep schedule with 7-8 hours of quality sleep to support cellular repair and brain health."
            },
            {
              category: "nutrition",
              title: "Increase Plant Diversity",
              description: "Aim for 30+ different plant foods weekly to support gut microbiome diversity and reduce inflammation."
            },
            {
              category: "exercise",
              title: "Add Strength Training",
              description: "Incorporate 2-3 strength training sessions weekly to preserve muscle mass and support metabolic health."
            }
          ]
        });
        
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography color="error">Error: {error}</Typography>
      </Box>
    );
  }

  // Chart data for longevity score history
  const scoreHistoryData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [
      {
        label: 'Longevity Score',
        data: [68, 70, 72, 72, 76],
        fill: false,
        backgroundColor: '#2E7D32',
        borderColor: '#2E7D32',
        tension: 0.4
      },
    ],
  };

  // Chart data for category breakdown
  const categoryBreakdownData = {
    labels: ['Sleep', 'Nutrition', 'Exercise', 'Stress'],
    datasets: [
      {
        data: [82, 70, 75, 65],
        backgroundColor: [
          '#1976D2', // Sleep - Blue
          '#2E7D32', // Nutrition - Green
          '#FF9800', // Exercise - Orange
          '#9C27B0', // Stress - Purple
        ],
        borderWidth: 1,
      },
    ],
  };

  // Chart options
  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '70%',
    plugins: {
      legend: {
        position: 'bottom',
      },
    },
  };

  const lineOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      y: {
        min: 50,
        max: 100,
      },
    },
  };

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

  return (
    <Box>
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Welcome back, {userData.name}
        </Typography>
        <Button 
          variant="contained" 
          color="primary" 
          startIcon={<AssessmentIcon />}
          onClick={() => navigate('/assessment')}
        >
          Take New Assessment
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Longevity Score Card */}
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
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
                    value={userData.longevityScore} 
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
                      {userData.longevityScore}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      out of 100
                    </Typography>
                  </Box>
                </Box>
                <Box sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
                  <ProgressIcon color="primary" sx={{ mr: 1 }} />
                  <Typography variant="body2" color="text.secondary">
                    +{latestAssessment.longevityScore - latestAssessment.previousScore} points since last assessment
                  </Typography>
                </Box>
              </Box>
              <Divider sx={{ my: 2 }} />
              <Typography variant="body2" color="text.secondary">
                Primary Motivation Driver:
              </Typography>
              <Typography variant="body1" sx={{ fontWeight: 'medium' }}>
                {userData.motivationDriver.charAt(0) + userData.motivationDriver.slice(1).toLowerCase()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Category Breakdown Card */}
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Health Category Breakdown
              </Typography>
              <Box sx={{ height: 240, mt: 2 }}>
                <Doughnut data={categoryBreakdownData} options={doughnutOptions} />
              </Box>
              <Divider sx={{ my: 2 }} />
              <Typography variant="body2" color="text.secondary">
                Highest Category: Sleep ({latestAssessment.categoryScores.sleep})
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Lowest Category: Stress ({latestAssessment.categoryScores.stress})
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Progress Chart Card */}
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Longevity Score Progress
              </Typography>
              <Box sx={{ height: 240, mt: 2 }}>
                <Line data={scoreHistoryData} options={lineOptions} />
              </Box>
              <Divider sx={{ my: 2 }} />
              <Typography variant="body2" color="text.secondary">
                Assessments Completed: {userData.assessmentCount}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Last Assessment: {new Date(userData.lastAssessment).toLocaleDateString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Top Recommendations Card */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Top Recommendations
              </Typography>
              <Grid container spacing={2} sx={{ mt: 1 }}>
                {latestAssessment.topRecommendations.map((recommendation, index) => (
                  <Grid item xs={12} md={4} key={index}>
                    <Card variant="outlined" sx={{ height: '100%' }}>
                      <CardContent>
                        <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
                          <Avatar sx={{ bgcolor: 'primary.light' }}>
                            {getCategoryIcon(recommendation.category)}
                          </Avatar>
                          <Typography variant="h6" component="div">
                            {recommendation.title}
                          </Typography>
                        </Stack>
                        <Typography variant="body2" color="text.secondary">
                          {recommendation.description}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
                <Button 
                  variant="outlined" 
                  color="primary"
                  onClick={() => navigate(`/results/${latestAssessment.id}`)}
                >
                  View All Recommendations
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
