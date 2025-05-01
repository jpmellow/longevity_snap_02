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
    name: '', // Preferred name
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
    cardioMinutesPerDay: '',
    cardioDaysPerWeek: '',
    strengthMinutesPerDay: '',
    strengthDaysPerWeek: '',
    mobilityMinutesPerDay: '',
    mobilityDaysPerWeek: '',
    
    // Mental Health
    stressLevel: 5,
    relaxationPractices: [],
    workLifeBalance: ''
  });
  
  // State for tracking form errors and validation
  const [formErrors, setFormErrors] = useState({});

  const [macroError, setMacroError] = useState('');

  const [unitSystem, setUnitSystem] = useState('metric'); // 'metric' or 'imperial'

  const [heightFeet, setHeightFeet] = useState('');
  const [heightInches, setHeightInches] = useState('');

  const gradientButton = {
    background: 'linear-gradient(90deg, #ff5858 0%, #f857a6 100%)',
    color: '#fff',
    borderRadius: '30px',
    boxShadow: '0 4px 20px 0 rgba(248,87,166,0.12)',
    fontWeight: 700,
    letterSpacing: 1,
    transition: 'all 0.2s cubic-bezier(.4,0,.2,1)',
    '&:hover': {
      background: 'linear-gradient(90deg, #ff5858 0%, #ff9966 100%)',
      transform: 'scale(1.05)',
      boxShadow: '0 6px 24px 0 rgba(255,88,88,0.18)',
    },
    mt: 2
  };

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
    
    // Handle unit system change
    if (name === 'unitSystem') {
      setUnitSystem(value);
      // Reset imperial height fields when switching units
      if (value === 'metric') {
        setHeightFeet('');
        setHeightInches('');
      }
      return;
    }
    
    // Clear validation error for this field when the user makes a change
    clearFieldError(name === 'preferredExercises' ? 'preferredExercises' : name);
    
    if (name === 'age') {
      let newValue = value;
      if (Number(value) > 119) {
        newValue = '0';
      }
      setFormData({ ...formData, age: newValue });
      return;
    }
    
    if (name === 'heightFeet') {
      setHeightFeet(value);
      // Update formData.height to total inches for validation
      setFormData({ ...formData, height: value && heightInches ? String(parseInt(value) * 12 + parseInt(heightInches || 0)) : '' });
      return;
    }
    if (name === 'heightInches') {
      setHeightInches(value);
      setFormData({ ...formData, height: heightFeet && value ? String(parseInt(heightFeet) * 12 + parseInt(value || 0)) : '' });
      return;
    }
    
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
    } else if ([
      'cardioMinutesPerDay', 'cardioDaysPerWeek',
      'strengthMinutesPerDay', 'strengthDaysPerWeek',
      'mobilityMinutesPerDay', 'mobilityDaysPerWeek'
    ].includes(name)) {
      setFormData({ ...formData, [name]: value });
      return;
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
        if (!formData.name) newErrors.name = 'Name is required';
        if (!formData.age) newErrors.age = 'Age is required';
        else if (Number(formData.age) >= 120) newErrors.age = 'Please enter a valid age less than 120';
        if (!formData.gender) newErrors.gender = 'Gender is required';
        if (!formData.height) newErrors.height = 'Height is required';
        else if (Number(formData.height) >= 280) newErrors.height = 'Please enter a valid height less than 280 cm';
        if (!formData.weight) newErrors.weight = 'Weight is required';
        else if (Number(formData.weight) >= 250) newErrors.weight = 'Please enter a valid weight less than 250 kg';
        break;
      
      case 1: // Health Goals
        if (formData.healthGoals.length === 0) newErrors.healthGoals = 'Select at least one health goal';
        break;
      
      case 2: // Sleep Patterns
        if (!formData.averageSleepHours) newErrors.averageSleepHours = 'Average sleep hours is required';
        else if (Number(formData.averageSleepHours) < 3 || Number(formData.averageSleepHours) > 14) newErrors.averageSleepHours = 'Please enter a value between 3 and 14 hours.';
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
        if (!formData.cardioMinutesPerDay) newErrors.cardioMinutesPerDay = 'Cardio minutes per day is required';
        if (!formData.cardioDaysPerWeek) newErrors.cardioDaysPerWeek = 'Cardio days per week is required';
        if (!formData.strengthMinutesPerDay) newErrors.strengthMinutesPerDay = 'Strength minutes per day is required';
        if (!formData.strengthDaysPerWeek) newErrors.strengthDaysPerWeek = 'Strength days per week is required';
        if (!formData.mobilityMinutesPerDay) newErrors.mobilityMinutesPerDay = 'Mobility minutes per day is required';
        if (!formData.mobilityDaysPerWeek) newErrors.mobilityDaysPerWeek = 'Mobility days per week is required';
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
      Boolean(formData.name && formData.age && formData.gender && formData.height && formData.weight),
      // Health Goals
      Boolean(formData.healthGoals.length > 0),
      // Sleep Patterns
      Boolean(formData.averageSleepHours && formData.sleepQuality && formData.sleepConsistency),
      // Nutrition
      Boolean(formData.dietType && formData.mealFrequency && formData.waterIntake && 
              formData.macronutrients.protein && formData.macronutrients.carbs && formData.macronutrients.fats),
      // Physical Activity
      Boolean(formData.cardioMinutesPerDay && formData.cardioDaysPerWeek && formData.strengthMinutesPerDay && formData.strengthDaysPerWeek && formData.mobilityMinutesPerDay && formData.mobilityDaysPerWeek),
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
      let submissionData = { ...formData };
      if (unitSystem === 'imperial') {
        // Convert lbs to kg
        submissionData.weight = formData.weight ? (parseFloat(formData.weight) * 0.453592).toFixed(1) : '';
        // Convert feet/inches to cm
        const totalInches = heightFeet && heightInches ? (parseInt(heightFeet) * 12 + parseInt(heightInches)) : (formData.height ? parseInt(formData.height) : 0);
        submissionData.height = totalInches ? (totalInches * 2.54).toFixed(1) : '';
      }
      const assessmentData = {
        ...submissionData,
        submissionDate: new Date().toISOString(),
        userId: 'current-user-id' // In a real app, this would come from auth
      };
      
      console.log('Submitting assessment data:', assessmentData);
      
      // Attempt to submit to backend API
      try {
        setTimeout(() => {
          const mockAssessmentId = `assessment-${Date.now()}`;
          // Reset formData (including name) after submit
          setFormData({
            name: '', age: '', gender: '', height: '', weight: '', healthGoals: [], motivationLevel: 5,
            averageSleepHours: '', sleepQuality: '', sleepConsistency: '', dietType: '', mealFrequency: '', waterIntake: '', macronutrients: { protein: '', carbs: '', fats: '' }, cardioMinutesPerDay: '', cardioDaysPerWeek: '', strengthMinutesPerDay: '', strengthDaysPerWeek: '', mobilityMinutesPerDay: '', mobilityDaysPerWeek: '', stressLevel: 5, relaxationPractices: [], workLifeBalance: ''
          });
          setHeightFeet(''); setHeightInches('');
          setUnitSystem('metric');
          navigate(`/results/${mockAssessmentId}`, { state: { name: formData.name, age: formData.age } });
        }, 2000);
      } catch (apiError) {
        console.error('API Error:', apiError);
        throw apiError;
      }
    } catch (error) {
      console.error('Error submitting assessment:', error);
      setSubmitting(false);
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
            
            <TextField
              label="What should we call you?"
              name="name"
              type="text"
              value={formData.name}
              onChange={handleChange}
              fullWidth
              required
              sx={{ borderRadius: '18px', mb: 2 }}
              inputProps={{ maxLength: 30 }}
            />
            
            <TextField
              label="Age "
              name="age"
              type="number"
              value={formData.age}
              onChange={handleChange}
              fullWidth
              required
              error={!!formErrors.age}
              helperText={
                formErrors.age
                  ? ` ${formErrors.age}`
                  : Number(formData.age) > 100
                  ? " Wow! You're aiming for a world record!"
                  : "Enter your age (must be less than 120)"
              }
              FormHelperTextProps={{
                style: {
                  color: formErrors.age
                    ? '#e65100'
                    : Number(formData.age) > 100
                    ? '#43a047'
                    : undefined
                }
              }}
              inputProps={{ min: 18, max: 119 }}
              sx={{ borderRadius: '18px', mb: 2 }}
            />
            
            {/* Unit system selection */}
            <FormControl component="fieldset" sx={{ mt: 2 }}>
              <FormLabel component="legend">Units</FormLabel>
              <RadioGroup
                row
                name="unitSystem"
                value={unitSystem}
                onChange={handleChange}
              >
                <FormControlLabel value="metric" control={<Radio />} label="Metric (kg, cm)" />
                <FormControlLabel value="imperial" control={<Radio />} label="Imperial (lbs, ft/in)" />
              </RadioGroup>
            </FormControl>
            
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
                <FormHelperText>{formErrors.gender || ''}</FormHelperText>
              </FormControl>
              
              {/* Height fields: metric = cm, imperial = ft/in */}
              {unitSystem === 'imperial' ? (
                <Stack direction="row" spacing={2}>
                  <TextField
                    label="Feet"
                    name="heightFeet"
                    type="number"
                    value={heightFeet}
                    onChange={handleChange}
                    fullWidth
                    required
                    inputProps={{ min: 0 }}
                    placeholder="Feet"
                    sx={{ borderRadius: '18px' }}
                  />
                  <TextField
                    label="Inches"
                    name="heightInches"
                    type="number"
                    value={heightInches}
                    onChange={handleChange}
                    fullWidth
                    required
                    inputProps={{ min: 0, max: 11 }}
                    placeholder="Inches"
                    sx={{ borderRadius: '18px' }}
                  />
                </Stack>
              ) : (
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
                  inputProps={{ min: 50, max: 279 }}
                  placeholder="Enter height in centimeters"
                  sx={{ borderRadius: '18px' }}
                />
              )}
              
              {/* Weight field with dynamic label/placeholder */}
              <TextField
                label={unitSystem === 'imperial' ? 'Weight (lbs)' : 'Weight (kg)'}
                name="weight"
                type="number"
                value={formData.weight}
                onChange={handleChange}
                fullWidth
                required
                error={!!formErrors.weight}
                helperText={formErrors.weight || ''}
                inputProps={{ min: 20, max: 249 }}
                placeholder={unitSystem === 'imperial' ? 'Enter weight in pounds' : 'Enter weight in kilograms'}
                sx={{ borderRadius: '18px' }}
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
                label="Average Sleep Hours (per night)"
                name="averageSleepHours"
                type="number"
                value={formData.averageSleepHours}
                onChange={handleChange}
                fullWidth
                required
                error={!!formErrors.averageSleepHours}
                helperText={formErrors.averageSleepHours || ''}
                inputProps={{ min: 3, max: 14 }}
                sx={{ borderRadius: '18px' }}
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
                  sx={{ borderRadius: '18px' }}
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
                  sx={{ borderRadius: '18px' }}
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
                  sx={{ borderRadius: '18px' }}
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
                  sx={{ borderRadius: '18px' }}
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
                  sx={{ borderRadius: '18px' }}
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
                  sx={{ borderRadius: '18px' }}
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
              For each activity, enter how many minutes you do it per day and how many days per week.
            </Typography>
            <Stack spacing={3} sx={{ mt: 3 }}>
              {/* Cardio */}
              <Typography variant="subtitle1">Cardio</Typography>
              <Stack direction="row" spacing={2}>
                <TextField
                  label="Minutes per day"
                  name="cardioMinutesPerDay"
                  type="number"
                  value={formData.cardioMinutesPerDay}
                  onChange={handleChange}
                  fullWidth
                  required
                  inputProps={{ min: 0, max: 300 }}
                  sx={{ borderRadius: '18px' }}
                />
                <TextField
                  label="Days per week"
                  name="cardioDaysPerWeek"
                  type="number"
                  value={formData.cardioDaysPerWeek}
                  onChange={handleChange}
                  fullWidth
                  required
                  inputProps={{ min: 0, max: 7 }}
                  sx={{ borderRadius: '18px' }}
                />
              </Stack>
              {/* Strength */}
              <Typography variant="subtitle1">Strength Training</Typography>
              <Stack direction="row" spacing={2}>
                <TextField
                  label="Minutes per day"
                  name="strengthMinutesPerDay"
                  type="number"
                  value={formData.strengthMinutesPerDay}
                  onChange={handleChange}
                  fullWidth
                  required
                  inputProps={{ min: 0, max: 300 }}
                  sx={{ borderRadius: '18px' }}
                />
                <TextField
                  label="Days per week"
                  name="strengthDaysPerWeek"
                  type="number"
                  value={formData.strengthDaysPerWeek}
                  onChange={handleChange}
                  fullWidth
                  required
                  inputProps={{ min: 0, max: 7 }}
                  sx={{ borderRadius: '18px' }}
                />
              </Stack>
              {/* Mobility */}
              <Typography variant="subtitle1">Stretching / Mobility</Typography>
              <Stack direction="row" spacing={2}>
                <TextField
                  label="Minutes per day"
                  name="mobilityMinutesPerDay"
                  type="number"
                  value={formData.mobilityMinutesPerDay}
                  onChange={handleChange}
                  fullWidth
                  required
                  inputProps={{ min: 0, max: 300 }}
                  sx={{ borderRadius: '18px' }}
                />
                <TextField
                  label="Days per week"
                  name="mobilityDaysPerWeek"
                  type="number"
                  value={formData.mobilityDaysPerWeek}
                  onChange={handleChange}
                  fullWidth
                  required
                  inputProps={{ min: 0, max: 7 }}
                  sx={{ borderRadius: '18px' }}
                />
              </Stack>
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
                  sx={{ borderRadius: '18px' }}
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
                    sx={gradientButton}
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
                  sx={gradientButton}
                >
                  Back
                </Button>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleNext}
                  sx={gradientButton}
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
