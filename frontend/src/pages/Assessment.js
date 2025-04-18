import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Stepper,
  Step,
  StepLabel,
  Card,
  CardContent,
  Button,
  TextField,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Slider,
  InputLabel,
  Select,
  MenuItem,
  Divider,
  CircularProgress,
  Stack,
  Alert,
  Chip,
  OutlinedInput,
  FormHelperText
} from '@mui/material';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

// Define the assessment sections
const steps = [
  'Basic Information',
  'Health Goals',
  'Sleep Patterns',
  'Nutrition',
  'Physical Activity',
  'Mental Health'
];

// Register ChartJS components
ChartJS.register(ArcElement, Tooltip, Legend);

const Assessment = () => {
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    // Basic Information
    age: '',
    gender: '',
    height: '',
    weight: '',
    
    // Health Goals
    healthGoals: [],
    motivationLevel: 5,
    
    // Sleep Patterns
    averageSleepHours: '',
    sleepQuality: '',
    sleepConsistency: '',
    
    // Nutrition
    dietType: '',
    mealFrequency: '',
    waterIntake: '',
    macronutrients: {
      protein: '',
      carbs: '',
      fats: ''
    },
    
    // Physical Activity
    exerciseFrequency: '',
    exerciseTypes: [],
    activityLevel: '',
    preferredExercises: [],
    
    // Mental Health
    stressLevel: 5,
    relaxationPractices: [],
    workLifeBalance: ''
  });
  
  // State for tracking form errors and validation
  const [formErrors, setFormErrors] = useState({});

  const [macroError, setMacroError] = useState('');

  const validateMacros = (macros) => {
    const total = Object.values(macros).reduce((sum, val) => sum + (Number(val) || 0), 0);
    if (total !== 100) {
      setMacroError(`Total should be 100%. Current total: ${total}%`);
      return false;
    }
    setMacroError('');
    return true;
  };
  
  // Reset validation errors for specified field
  const clearFieldError = (fieldName) => {
    if (formErrors[fieldName]) {
      const updatedErrors = { ...formErrors };
      delete updatedErrors[fieldName];
      setFormErrors(updatedErrors);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    // Clear validation error for this field when the user makes a change
    clearFieldError(name === 'preferredExercises' ? 'preferredExercises' : name);
    
    if (name.startsWith('macro_')) {
      const macroType = name.split('_')[1];
      const newMacros = {
        ...formData.macronutrients,
        [macroType]: value
      };
      setFormData({
        ...formData,
        macronutrients: newMacros
      });
      validateMacros(newMacros);
      clearFieldError('macros');
    } else {
      setFormData({
        ...formData,
        [name]: value
      });
    }
  };

  const handleSliderChange = (name) => (e, newValue) => {
    setFormData({
      ...formData,
      [name]: newValue
    });
  };

  // Validate the current step and return whether it's valid
  const validateStep = (step) => {
    const newErrors = {};
    let isValid = true;

    switch (step) {
      case 0: // Basic Information
        if (!formData.age) newErrors.age = 'Age is required';
        if (!formData.gender) newErrors.gender = 'Gender is required';
        if (!formData.height) newErrors.height = 'Height is required';
        if (!formData.weight) newErrors.weight = 'Weight is required';
        break;
      
      case 1: // Health Goals
        if (formData.healthGoals.length === 0) newErrors.healthGoals = 'Select at least one health goal';
        break;
      
      case 2: // Sleep Patterns
        if (!formData.averageSleepHours) newErrors.averageSleepHours = 'Average sleep hours is required';
        if (!formData.sleepQuality) newErrors.sleepQuality = 'Sleep quality is required';
        if (!formData.sleepConsistency) newErrors.sleepConsistency = 'Sleep consistency is required';
        break;
      
      case 3: // Nutrition
        if (!formData.dietType) newErrors.dietType = 'Diet type is required';
        if (!formData.mealFrequency) newErrors.mealFrequency = 'Meal frequency is required';
        if (!formData.waterIntake) newErrors.waterIntake = 'Water intake is required';
        
        // Validate macros
        const macroValid = validateMacros(formData.macronutrients);
        if (!macroValid) {
          newErrors.macros = 'Macronutrient distribution must total 100%';
        }
        break;
      
      case 4: // Physical Activity
        if (!formData.exerciseFrequency) newErrors.exerciseFrequency = 'Exercise frequency is required';
        if (!formData.activityLevel) newErrors.activityLevel = 'Activity level is required';
        if (formData.preferredExercises.length === 0) newErrors.preferredExercises = 'Select at least one exercise type';
        break;
      
      case 5: // Mental Health
        if (!formData.workLifeBalance) newErrors.workLifeBalance = 'Work-life balance is required';
        if (formData.relaxationPractices.length === 0) newErrors.relaxationPractices = 'Select at least one relaxation practice';
        break;
      
      default:
        break;
    }

    if (Object.keys(newErrors).length > 0) {
      isValid = false;
    }

    setFormErrors(newErrors);
    return isValid;
  };

  // Calculate completion status for each section
  const calculateCompletionStatus = () => {
    return [
      // Basic Information
      Boolean(formData.age && formData.gender && formData.height && formData.weight),
      // Health Goals
      Boolean(formData.healthGoals.length > 0),
      // Sleep Patterns
      Boolean(formData.averageSleepHours && formData.sleepQuality && formData.sleepConsistency),
      // Nutrition
      Boolean(formData.dietType && formData.mealFrequency && formData.waterIntake && 
              formData.macronutrients.protein && formData.macronutrients.carbs && formData.macronutrients.fats),
      // Physical Activity
      Boolean(formData.exerciseFrequency && formData.activityLevel && formData.preferredExercises.length > 0),
      // Mental Health
      Boolean(formData.workLifeBalance && formData.relaxationPractices.length > 0)
    ];
  };

  const handleNext = () => {
    // Validate the current step
    const isValid = validateStep(activeStep);
    if (!isValid) {
      // Show validation error alert or feedback
      return;
    }
    
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
    window.scrollTo(0, 0);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
    window.scrollTo(0, 0);
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    
    try {
      // Prepare the data for submission
      const assessmentData = {
        ...formData,
        submissionDate: new Date().toISOString(),
        userId: 'current-user-id' // In a real app, this would come from auth
      };
      
      console.log('Submitting assessment data:', assessmentData);
      
      // Attempt to submit to backend API
      try {
        // In a production app, this would be a real API endpoint
        // const response = await fetch('/api/assessments', {
        //   method: 'POST',
        //   headers: {
        //     'Content-Type': 'application/json',
        //   },
        //   body: JSON.stringify(assessmentData),
        // });
        // 
        // if (!response.ok) {
        //   throw new Error(`HTTP error! status: ${response.status}`);
        // }
        // 
        // const result = await response.json();
        // navigate(`/results/${result.assessmentId}`);
        
        // For now, simulate API call delay
        setTimeout(() => {
          // Navigate to results page with a mock assessment ID
          // In a real app, we would use the ID returned from the API
          const mockAssessmentId = `assessment-${Date.now()}`;
          navigate(`/results/${mockAssessmentId}`);
        }, 2000);
      } catch (apiError) {
        console.error('API Error:', apiError);
        throw apiError;
      }
    } catch (error) {
      console.error('Error submitting assessment:', error);
      setSubmitting(false);
      // In a real app, we would show an error message to the user
    }
  };

  // Render form based on active step
  const renderStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Basic Information
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              This information helps us provide personalized health insights based on your demographics.
            </Typography>
            
            <Stack spacing={3} sx={{ mt: 3 }}>
              <TextField
                label="Age"
                name="age"
                type="number"
                value={formData.age}
                onChange={handleChange}
                fullWidth
                required
                error={!!formErrors.age}
                helperText={formErrors.age || ''}
                inputProps={{ min: 18, max: 120 }}
              />
              
              <FormControl fullWidth required error={!!formErrors.gender}>
                <FormLabel>Gender</FormLabel>
                <RadioGroup
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  row
                >
                  <FormControlLabel value="male" control={<Radio />} label="Male" />
                  <FormControlLabel value="female" control={<Radio />} label="Female" />
                  <FormControlLabel value="other" control={<Radio />} label="Other" />
                </RadioGroup>
                {formErrors.gender && <Typography color="error" variant="caption">{formErrors.gender}</Typography>}
              </FormControl>
              
              <TextField
                label="Height (cm)"
                name="height"
                type="number"
                value={formData.height}
                onChange={handleChange}
                fullWidth
                required
                error={!!formErrors.height}
                helperText={formErrors.height || ''}
                inputProps={{ min: 100, max: 250 }}
              />
              
              <TextField
                label="Weight (kg)"
                name="weight"
                type="number"
                value={formData.weight}
                onChange={handleChange}
                fullWidth
                required
                error={!!formErrors.weight}
                helperText={formErrors.weight || ''}
                inputProps={{ min: 30, max: 250 }}
              />
            </Stack>
          </Box>
        );
        
      case 1:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Health Goals
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Understanding your goals helps us tailor recommendations to what matters most to you.
            </Typography>
            
            <Stack spacing={3} sx={{ mt: 3 }}>
              <FormControl fullWidth required error={!!formErrors.healthGoals}>
                <InputLabel>Health Goals</InputLabel>
                <Select
                  name="healthGoals"
                  multiple
                  value={formData.healthGoals}
                  onChange={handleChange}
                  input={<OutlinedInput label="Health Goals" />}
                  renderValue={(selected) => (
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {selected.map((value) => (
                        <Chip 
                          key={value} 
                          label={{
                            longevity: 'Increase Longevity',
                            weight: 'Weight Management',
                            energy: 'Improve Energy Levels',
                            sleep: 'Better Sleep Quality',
                            stress: 'Reduce Stress',
                            performance: 'Enhance Performance',
                            immunity: 'Boost Immunity',
                            mental: 'Mental Clarity'
                          }[value]} 
                        />
                      ))}
                    </Box>
                  )}
                >
                  <MenuItem value="longevity">Increase Longevity</MenuItem>
                  <MenuItem value="weight">Weight Management</MenuItem>
                  <MenuItem value="energy">Improve Energy Levels</MenuItem>
                  <MenuItem value="sleep">Better Sleep Quality</MenuItem>
                  <MenuItem value="stress">Reduce Stress</MenuItem>
                  <MenuItem value="performance">Enhance Performance</MenuItem>
                  <MenuItem value="immunity">Boost Immunity</MenuItem>
                  <MenuItem value="mental">Mental Clarity</MenuItem>
                  <MenuItem value="cognitive">Optimize Cognitive Function</MenuItem>
                  <MenuItem value="mood">Improve Mood & Emotional Wellbeing</MenuItem>
                </Select>
              </FormControl>
              
              <Box>
                <FormLabel>Motivation Level</FormLabel>
                <Slider
                  name="motivationLevel"
                  value={formData.motivationLevel}
                  onChange={handleSliderChange('motivationLevel')}
                  min={1}
                  max={10}
                  step={1}
                  marks
                  valueLabelDisplay="auto"
                  aria-labelledby="motivation-level-slider"
                />
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">Low</Typography>
                  <Typography variant="body2" color="text.secondary">High</Typography>
                </Box>
              </Box>
            </Stack>
          </Box>
        );
        
      case 2:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Sleep Patterns
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Quality sleep is a fundamental pillar of health and longevity.
            </Typography>
            
            <Stack spacing={3} sx={{ mt: 3 }}>
              <TextField
                label="Average Sleep Hours"
                name="averageSleepHours"
                type="number"
                value={formData.averageSleepHours}
                onChange={handleChange}
                fullWidth
                required
              />
              
              <FormControl fullWidth required>
                <FormLabel>Sleep Quality</FormLabel>
                <RadioGroup
                  name="sleepQuality"
                  value={formData.sleepQuality}
                  onChange={handleChange}
                >
                  <FormControlLabel value="excellent" control={<Radio />} label="Excellent - Wake refreshed" />
                  <FormControlLabel value="good" control={<Radio />} label="Good - Generally rested" />
                  <FormControlLabel value="fair" control={<Radio />} label="Fair - Sometimes tired" />
                  <FormControlLabel value="poor" control={<Radio />} label="Poor - Often tired" />
                  <FormControlLabel value="very_poor" control={<Radio />} label="Very Poor - Always exhausted" />
                </RadioGroup>
              </FormControl>
              
              <FormControl fullWidth required>
                <FormLabel>Sleep Consistency</FormLabel>
                <RadioGroup
                  name="sleepConsistency"
                  value={formData.sleepConsistency}
                  onChange={handleChange}
                >
                  <FormControlLabel value="very_consistent" control={<Radio />} label="Very consistent schedule" />
                  <FormControlLabel value="mostly_consistent" control={<Radio />} label="Mostly consistent" />
                  <FormControlLabel value="somewhat_variable" control={<Radio />} label="Somewhat variable" />
                  <FormControlLabel value="highly_variable" control={<Radio />} label="Highly variable/shift work" />
                </RadioGroup>
              </FormControl>
            </Stack>
          </Box>
        );
        
      case 3:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Nutrition
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Your dietary patterns significantly impact your health and longevity.
            </Typography>
            
            <Stack spacing={3} sx={{ mt: 3 }}>
              <FormControl fullWidth required>
                <InputLabel>Diet Type</InputLabel>
                <Select
                  name="dietType"
                  value={formData.dietType}
                  onChange={handleChange}
                  label="Diet Type"
                >
                  <MenuItem value="omnivore">Omnivore (All foods)</MenuItem>
                  <MenuItem value="mediterranean">Mediterranean</MenuItem>
                  <MenuItem value="vegetarian">Vegetarian</MenuItem>
                  <MenuItem value="vegan">Vegan</MenuItem>
                  <MenuItem value="paleo">Paleo</MenuItem>
                  <MenuItem value="keto">Ketogenic</MenuItem>
                  <MenuItem value="other">Other</MenuItem>
                </Select>
              </FormControl>
              
              <FormControl fullWidth required>
                <InputLabel>Meal Frequency</InputLabel>
                <Select
                  name="mealFrequency"
                  value={formData.mealFrequency}
                  onChange={handleChange}
                  label="Meal Frequency"
                >
                  <MenuItem value="1-2">1-2 meals per day</MenuItem>
                  <MenuItem value="3">3 meals per day</MenuItem>
                  <MenuItem value="4-5">4-5 meals per day</MenuItem>
                  <MenuItem value="grazing">Frequent snacking/grazing</MenuItem>
                  <MenuItem value="intermittent">Intermittent fasting</MenuItem>
                </Select>
              </FormControl>
              
              <FormControl fullWidth required>
                <InputLabel>Water Intake (Glasses/Day)</InputLabel>
                <Select
                  name="waterIntake"
                  value={formData.waterIntake}
                  onChange={handleChange}
                  label="Water Intake (Glasses/Day)"
                >
                  <MenuItem value="0-2">0-2 glasses</MenuItem>
                  <MenuItem value="3-5">3-5 glasses</MenuItem>
                  <MenuItem value="6-8">6-8 glasses</MenuItem>
                  <MenuItem value="8+">More than 8 glasses</MenuItem>
                </Select>
              </FormControl>

              <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
                Macronutrient Distribution (%)
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
                <TextField
                  label="Protein %"
                  name="macro_protein"
                  type="number"
                  value={formData.macronutrients.protein}
                  onChange={handleChange}
                  inputProps={{ min: 0, max: 100 }}
                  fullWidth
                  required
                  error={!!macroError}
                  helperText={macroError || "Recommended: 10-35%"}
                />
                <TextField
                  label="Carbs %"
                  name="macro_carbs"
                  type="number"
                  value={formData.macronutrients.carbs}
                  onChange={handleChange}
                  inputProps={{ min: 0, max: 100 }}
                  fullWidth
                  required
                  error={!!macroError}
                  helperText={macroError || "Recommended: 45-65%"}
                />
                <TextField
                  label="Fats %"
                  name="macro_fats"
                  type="number"
                  value={formData.macronutrients.fats}
                  onChange={handleChange}
                  inputProps={{ min: 0, max: 100 }}
                  fullWidth
                  required
                  error={!!macroError}
                  helperText={macroError || "Recommended: 20-35%"}
                />
              </Box>
              
              {/* Macronutrient Distribution Chart */}
              <Box sx={{ height: 300, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <Doughnut
                  data={{
                    labels: ['Protein', 'Carbs', 'Fats'],
                    datasets: [{
                      data: [
                        Number(formData.macronutrients.protein) || 0,
                        Number(formData.macronutrients.carbs) || 0,
                        Number(formData.macronutrients.fats) || 0
                      ],
                      backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)'
                      ],
                      borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)'
                      ],
                      borderWidth: 1
                    }]
                  }}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'bottom'
                      },
                      tooltip: {
                        callbacks: {
                          label: (context) => `${context.label}: ${context.raw}%`
                        }
                      }
                    }
                  }}
                />
              </Box>
            </Stack>
          </Box>
        );
        
      case 4:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Physical Activity
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Regular physical activity is one of the strongest predictors of healthy lifespan.
            </Typography>
            
            <Stack spacing={3} sx={{ mt: 3 }}>
              <FormControl fullWidth required>
                <InputLabel>Exercise Frequency</InputLabel>
                <Select
                  name="exerciseFrequency"
                  value={formData.exerciseFrequency}
                  onChange={handleChange}
                  label="Exercise Frequency"
                >
                  <MenuItem value="sedentary">Rarely or never</MenuItem>
                  <MenuItem value="light">1-2 times per week</MenuItem>
                  <MenuItem value="moderate">3-4 times per week</MenuItem>
                  <MenuItem value="active">5-6 times per week</MenuItem>
                  <MenuItem value="very_active">Daily</MenuItem>
                </Select>
              </FormControl>
              
              <FormControl fullWidth required>
                <InputLabel>Activity Level</InputLabel>
                <Select
                  name="activityLevel"
                  value={formData.activityLevel}
                  onChange={handleChange}
                  label="Activity Level"
                >
                  <MenuItem value="sedentary">Sedentary (Little to no exercise)</MenuItem>
                  <MenuItem value="light">Light (Exercise 1-3 times/week)</MenuItem>
                  <MenuItem value="moderate">Moderate (Exercise 3-5 times/week)</MenuItem>
                  <MenuItem value="active">Active (Exercise 6-7 times/week)</MenuItem>
                  <MenuItem value="very_active">Very Active (Exercise multiple times/day)</MenuItem>
                </Select>
                {!!formErrors.activityLevel && (
                  <FormHelperText error>{formErrors.activityLevel}</FormHelperText>
                )}
              </FormControl>

              <FormControl fullWidth required error={!!formErrors.preferredExercises}>
                <InputLabel>Exercise Types</InputLabel>
                <Select
                  name="preferredExercises"
                  multiple
                  value={formData.preferredExercises}
                  onChange={handleChange}
                  input={<OutlinedInput label="Exercise Types" />}
                  renderValue={(selected) => (
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {selected.map((value) => (
                        <Chip 
                          key={value} 
                          label={{
                            walking: 'Walking/Hiking',
                            jogging: 'Jogging/Running',
                            cycling: 'Cycling',
                            swimming: 'Swimming',
                            strength: 'Strength Training',
                            hiit: 'HIIT',
                            yoga: 'Yoga/Stretching',
                            pilates: 'Pilates',
                            balance: 'Balance Training',
                            sports: 'Sports/Athletics',
                            dance: 'Dance/Aerobics',
                            martial: 'Martial Arts',
                            functional: 'Functional Training',
                            crossfit: 'CrossFit',
                            calisthenics: 'Calisthenics'
                          }[value] || value} 
                        />
                      ))}
                    </Box>
                  )}
                >
                  <MenuItem value="walking">Walking/Hiking</MenuItem>
                  <MenuItem value="jogging">Jogging/Running</MenuItem>
                  <MenuItem value="cycling">Cycling</MenuItem>
                  <MenuItem value="swimming">Swimming</MenuItem>
                  <MenuItem value="strength">Strength Training</MenuItem>
                  <MenuItem value="hiit">High-Intensity Interval Training (HIIT)</MenuItem>
                  <MenuItem value="yoga">Yoga/Stretching</MenuItem>
                  <MenuItem value="pilates">Pilates</MenuItem>
                  <MenuItem value="balance">Balance Training</MenuItem>
                  <MenuItem value="sports">Sports/Athletics</MenuItem>
                  <MenuItem value="dance">Dance/Aerobics</MenuItem>
                  <MenuItem value="martial">Martial Arts</MenuItem>
                  <MenuItem value="functional">Functional Training</MenuItem>
                  <MenuItem value="crossfit">CrossFit</MenuItem>
                  <MenuItem value="calisthenics">Calisthenics</MenuItem>
                </Select>
                {!!formErrors.preferredExercises && (
                  <FormHelperText error>{formErrors.preferredExercises}</FormHelperText>
                )}
                <Typography variant="caption" color="text.secondary" sx={{ mt: 1 }}>
                  Select all exercise types that you currently do or are interested in
                </Typography>
              </FormControl>
            </Stack>
          </Box>
        );
        
      case 5:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Mental Health
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Effective stress management protects your health and slows biological aging.
            </Typography>
            
            <Stack spacing={3} sx={{ mt: 3 }}>
              <Box>
                <FormLabel>Stress Level</FormLabel>
                <Slider
                  name="stressLevel"
                  value={formData.stressLevel}
                  onChange={handleSliderChange('stressLevel')}
                  min={1}
                  max={10}
                  step={1}
                  marks
                  valueLabelDisplay="auto"
                  aria-labelledby="stress-level-slider"
                />
                {!!formErrors.stressLevel && (
                  <FormHelperText error>{formErrors.stressLevel}</FormHelperText>
                )}
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">Low</Typography>
                  <Typography variant="body2" color="text.secondary">High</Typography>
                </Box>
              </Box>
              
              <FormControl fullWidth required error={!!formErrors.workLifeBalance}>
                <InputLabel>Work-Life Balance</InputLabel>
                <Select
                  name="workLifeBalance"
                  value={formData.workLifeBalance}
                  onChange={handleChange}
                  label="Work-Life Balance"
                >
                  <MenuItem value="excellent">Excellent - Perfect balance</MenuItem>
                  <MenuItem value="good">Good - Mostly balanced</MenuItem>
                  <MenuItem value="fair">Fair - Occasionally imbalanced</MenuItem>
                  <MenuItem value="poor">Poor - Often imbalanced</MenuItem>
                  <MenuItem value="very_poor">Very Poor - No balance</MenuItem>
                </Select>
                {!!formErrors.workLifeBalance && (
                  <FormHelperText error>{formErrors.workLifeBalance}</FormHelperText>
                )}
              </FormControl>

              <FormControl fullWidth required error={!!formErrors.relaxationPractices}>
                <InputLabel>Relaxation Practices</InputLabel>
                <Select
                  name="relaxationPractices"
                  multiple
                  value={formData.relaxationPractices}
                  onChange={handleChange}
                  input={<OutlinedInput label="Relaxation Practices" />}
                  renderValue={(selected) => (
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {selected.map((value) => (
                        <Chip 
                          key={value} 
                          label={{
                            meditation: 'Meditation',
                            breathing: 'Deep Breathing',
                            yoga: 'Yoga',
                            nature: 'Time in Nature',
                            reading: 'Reading',
                            music: 'Music/Art',
                            exercise: 'Exercise',
                            social: 'Social Connection',
                            therapy: 'Therapy/Counseling',
                            journaling: 'Journaling'
                          }[value] || value} 
                        />
                      ))}
                    </Box>
                  )}
                >
                  <MenuItem value="meditation">Meditation</MenuItem>
                  <MenuItem value="breathing">Deep Breathing Exercises</MenuItem>
                  <MenuItem value="yoga">Yoga</MenuItem>
                  <MenuItem value="nature">Time in Nature</MenuItem>
                  <MenuItem value="reading">Reading</MenuItem>
                  <MenuItem value="music">Music/Art</MenuItem>
                  <MenuItem value="exercise">Exercise</MenuItem>
                  <MenuItem value="social">Social Connection</MenuItem>
                  <MenuItem value="therapy">Therapy/Counseling</MenuItem>
                  <MenuItem value="journaling">Journaling</MenuItem>
                </Select>
                <Typography variant="caption" color="text.secondary" sx={{ mt: 1 }}>
                  Select all practices that you currently use for relaxation or stress management
                </Typography>
              </FormControl>
            </Stack>
          </Box>
        );
        
      default:
        return null;
    }
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Longevity Health Assessment
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Complete this comprehensive assessment to receive personalized health insights and recommendations.
      </Typography>
      
      {/* Show error alert if there are validation errors */}
      {Object.keys(formErrors).length > 0 && (
        <Alert severity="error" sx={{ mb: 3 }}>
          Please correct the errors before proceeding
        </Alert>
      )}

      {/* Calculate completion status for each step */}
      {calculateCompletionStatus().includes(false) && (
        <Alert severity="info" sx={{ mb: 3 }}>
          Complete all sections to get the most accurate health insights
        </Alert>
      )}

      <Stepper activeStep={activeStep} alternativeLabel sx={{ mb: 4 }}>
        {steps.map((label, index) => {
          const stepCompleted = calculateCompletionStatus()[index];
          return (
            <Step key={label} completed={stepCompleted}>
              <StepLabel
                StepIconProps={{
                  sx: { color: stepCompleted ? 'success.main' : 'inherit' }
                }}
              >
                {label}
              </StepLabel>
            </Step>
          );
        })}
      </Stepper>
      
      <Card>
        <CardContent>
          {activeStep === steps.length ? (
            <Box sx={{ textAlign: 'center', py: 3 }}>
              {submitting ? (
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <CircularProgress size={60} sx={{ mb: 3 }} />
                  <Typography variant="h6">
                    Processing your assessment...
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    Our AI is analyzing your data to generate personalized recommendations
                  </Typography>
                </Box>
              ) : (
                <Box>
                  <Typography variant="h5" gutterBottom>
                    Ready to Submit Your Assessment
                  </Typography>
                  <Typography variant="body1" paragraph>
                    Your assessment is complete. Click submit to receive your personalized health insights.
                  </Typography>
                  <Button 
                    variant="contained" 
                    color="primary" 
                    onClick={handleSubmit}
                    size="large"
                    sx={{ mt: 2 }}
                  >
                    Submit Assessment
                  </Button>
                </Box>
              )}
            </Box>
          ) : (
            <Box>
              {renderStepContent(activeStep)}
              
              <Divider sx={{ my: 4 }} />
              
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Button
                  disabled={activeStep === 0}
                  onClick={handleBack}
                  variant="outlined"
                >
                  Back
                </Button>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleNext}
                >
                  {activeStep === steps.length - 1 ? 'Finish' : 'Next'}
                </Button>
              </Box>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default Assessment;
