import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  CircularProgress,
  Chip,
  IconButton,
  Tooltip,
  Grid,
  Stack
} from '@mui/material';
import {
  Visibility as VisibilityIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  TrendingFlat as TrendingFlatIcon,
  Timeline as TimelineIcon
} from '@mui/icons-material';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip as ChartTooltip,
  Legend
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  ChartTooltip,
  Legend
);

const History = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [assessmentHistory, setAssessmentHistory] = useState([]);
  const [selectedMetric, setSelectedMetric] = useState('longevityScore');
  const [metrics, setMetrics] = useState([]);

  useEffect(() => {
    // Simulate API call to get assessment history
    const fetchHistory = async () => {
      try {
        // In a real app, this would be an API call
        setTimeout(() => {
          const mockHistory = [
            {
              id: "a123456",
              date: "2023-05-15",
              longevityScore: 76,
              metrics: {
                sleep: 82,
                nutrition: 70,
                exercise: 75,
                stress: 65,
                bmi: 24.2,
                bloodPressure: "120/80",
                restingHeartRate: 65
              }
            },
            {
              id: "a123455",
              date: "2023-04-01",
              longevityScore: 72,
              metrics: {
                sleep: 78,
                nutrition: 68,
                exercise: 72,
                stress: 68,
                bmi: 24.8,
                bloodPressure: "122/82",
                restingHeartRate: 68
              }
            },
            {
              id: "a123454",
              date: "2023-03-01",
              longevityScore: 72,
              metrics: {
                sleep: 75,
                nutrition: 70,
                exercise: 70,
                stress: 70,
                bmi: 25.1,
                bloodPressure: "124/84",
                restingHeartRate: 70
              }
            },
            {
              id: "a123453",
              date: "2023-02-01",
              longevityScore: 70,
              metrics: {
                sleep: 72,
                nutrition: 68,
                exercise: 70,
                stress: 68,
                bmi: 25.3,
                bloodPressure: "125/85",
                restingHeartRate: 72
              }
            },
            {
              id: "a123452",
              date: "2023-01-01",
              longevityScore: 68,
              metrics: {
                sleep: 70,
                nutrition: 65,
                exercise: 68,
                stress: 65,
                bmi: 25.5,
                bloodPressure: "126/86",
                restingHeartRate: 72
              }
            }
          ];
          
          setAssessmentHistory(mockHistory);
          
          // Extract available metrics from the first assessment
          if (mockHistory.length > 0) {
            const metricOptions = [
              { value: 'longevityScore', label: 'Longevity Score' },
              ...Object.keys(mockHistory[0].metrics).map(key => ({
                value: key,
                label: key.charAt(0).toUpperCase() + key.slice(1)
              }))
            ];
            setMetrics(metricOptions);
          }
          
          setLoading(false);
        }, 1500);
      } catch (error) {
        console.error("Error fetching history:", error);
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  // Prepare chart data
  const getChartData = () => {
    // Sort assessments by date (oldest first)
    const sortedAssessments = [...assessmentHistory].sort(
      (a, b) => new Date(a.date) - new Date(b.date)
    );
    
    const labels = sortedAssessments.map(assessment => 
      new Date(assessment.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    );
    
    const datasets = [];
    
    if (selectedMetric === 'longevityScore') {
      datasets.push({
        label: 'Longevity Score',
        data: sortedAssessments.map(assessment => assessment.longevityScore),
        borderColor: '#2E7D32',
        backgroundColor: '#2E7D32',
        tension: 0.4
      });
    } else {
      datasets.push({
        label: metrics.find(m => m.value === selectedMetric)?.label || selectedMetric,
        data: sortedAssessments.map(assessment => assessment.metrics[selectedMetric]),
        borderColor: '#1976D2',
        backgroundColor: '#1976D2',
        tension: 0.4
      });
    }
    
    return { labels, datasets };
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `${metrics.find(m => m.value === selectedMetric)?.label || 'Metric'} History`,
      },
    },
    scales: {
      y: {
        beginAtZero: false,
      },
    },
  };

  // Helper function to determine trend icon
  const getTrendIcon = (current, previous) => {
    if (!previous) return null;
    
    if (current > previous) {
      return <TrendingUpIcon sx={{ color: '#4caf50' }} />;
    } else if (current < previous) {
      return <TrendingDownIcon sx={{ color: '#f44336' }} />;
    } else {
      return <TrendingFlatIcon sx={{ color: '#ff9800' }} />;
    }
  };

  // Helper function to format date
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Assessment History
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Track your health progress over time and view detailed assessment results.
      </Typography>

      <Grid container spacing={3}>
        {/* Chart Card */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  Health Metrics Trend
                </Typography>
                <Stack direction="row" spacing={1}>
                  {metrics.map((metric) => (
                    <Chip
                      key={metric.value}
                      label={metric.label}
                      onClick={() => setSelectedMetric(metric.value)}
                      color={selectedMetric === metric.value ? 'primary' : 'default'}
                      variant={selectedMetric === metric.value ? 'filled' : 'outlined'}
                    />
                  ))}
                </Stack>
              </Box>
              <Box sx={{ height: 300 }}>
                {assessmentHistory.length > 0 ? (
                  <Line options={chartOptions} data={getChartData()} />
                ) : (
                  <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                    <Typography variant="body1" color="text.secondary">
                      No assessment data available
                    </Typography>
                  </Box>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* History Table Card */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Assessment Records
              </Typography>
              <TableContainer component={Paper} variant="outlined">
                <Table sx={{ minWidth: 650 }}>
                  <TableHead>
                    <TableRow sx={{ backgroundColor: 'background.default' }}>
                      <TableCell>Date</TableCell>
                      <TableCell>Longevity Score</TableCell>
                      <TableCell>Sleep</TableCell>
                      <TableCell>Nutrition</TableCell>
                      <TableCell>Exercise</TableCell>
                      <TableCell>Stress</TableCell>
                      <TableCell align="center">Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {assessmentHistory.map((assessment, index) => (
                      <TableRow key={assessment.id} hover>
                        <TableCell>{formatDate(assessment.date)}</TableCell>
                        <TableCell>
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <Typography variant="body2" sx={{ fontWeight: 'medium', mr: 1 }}>
                              {assessment.longevityScore}
                            </Typography>
                            {index < assessmentHistory.length - 1 && 
                              getTrendIcon(
                                assessment.longevityScore, 
                                assessmentHistory[index + 1].longevityScore
                              )
                            }
                          </Box>
                        </TableCell>
                        <TableCell>{assessment.metrics.sleep}</TableCell>
                        <TableCell>{assessment.metrics.nutrition}</TableCell>
                        <TableCell>{assessment.metrics.exercise}</TableCell>
                        <TableCell>{assessment.metrics.stress}</TableCell>
                        <TableCell align="center">
                          <Tooltip title="View Results">
                            <IconButton 
                              size="small"
                              onClick={() => navigate(`/results/${assessment.id}`)}
                            >
                              <VisibilityIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
              {assessmentHistory.length === 0 && (
                <Box sx={{ textAlign: 'center', py: 3 }}>
                  <TimelineIcon sx={{ fontSize: 48, color: 'text.secondary', opacity: 0.5 }} />
                  <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
                    No assessment history found
                  </Typography>
                  <Button 
                    variant="contained" 
                    color="primary" 
                    sx={{ mt: 2 }}
                    onClick={() => navigate('/assessment')}
                  >
                    Take Your First Assessment
                  </Button>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default History;
