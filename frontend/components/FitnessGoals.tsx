import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Select,
  Textarea,
  VStack,
  useToast,
  NumberInput,
  NumberInputField,
  Radio,
  RadioGroup,
  Stack,
  Checkbox,
} from '@chakra-ui/react'
import { useState, useEffect } from 'react'
import api from '../utils/api'

export default function FitnessGoals() {
  const [loading, setLoading] = useState(false)
  const [goals, setGoals] = useState(() => {
    // 从本地存储加载初始数据
    const savedGoals = localStorage.getItem('fitnessGoals')
    return savedGoals ? JSON.parse(savedGoals) : {
      primaryGoal: '',
      currentWeight: '',
      targetWeight: '',
      height: '',
      age: '',
      gender: '',
      activityLevel: '',
      timeCommitment: '',
      preferredWorkouts: [],
      medicalConditions: '',
      dietaryRestrictions: '',
      additionalNotes: '',
    }
  })
  const toast = useToast()

  // 从服务器加载数据
  useEffect(() => {
    const fetchGoals = async () => {
      try {
        const response = await api.get('/api/fitness/goals')
        if (response.data && Object.keys(response.data).length > 0) {
          setGoals(response.data)
          localStorage.setItem('fitnessGoals', JSON.stringify(response.data))
        }
      } catch (error) {
        console.error('Failed to fetch goals:', error)
      }
    }

    fetchGoals()
  }, [])

  // 自动保存到本地存储
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      localStorage.setItem('fitnessGoals', JSON.stringify(goals))
    }, 500) // 500ms 防抖

    return () => clearTimeout(timeoutId)
  }, [goals])

  const handlePreferredWorkoutsChange = (workout: string) => {
    setGoals(prev => {
      const newGoals = {
        ...prev,
        preferredWorkouts: prev.preferredWorkouts.includes(workout)
          ? prev.preferredWorkouts.filter(w => w !== workout)
          : [...prev.preferredWorkouts, workout]
      }
      return newGoals
    })
  }

  const handleChange = (field: string, value: any) => {
    setGoals(prev => {
      const newGoals = {
        ...prev,
        [field]: value
      }
      return newGoals
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await api.post('/api/fitness/goals', goals)
      
      // 更新本地存储
      localStorage.setItem('fitnessGoals', JSON.stringify(response.data.goals))
      
      toast({
        title: 'Success',
        description: 'Fitness goals updated successfully',
        status: 'success',
        duration: 5000,
        isClosable: true,
      })
    } catch (error) {
      console.error('Error submitting goals:', error)
      toast({
        title: 'Error',
        description: error.response?.data?.error || 'Failed to update fitness goals',
        status: 'error',
        duration: 5000,
        isClosable: true,
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box p={6} bg="white" borderRadius="lg" boxShadow="sm">
      <form onSubmit={handleSubmit}>
        <VStack spacing={4} align="stretch">
          <FormControl isRequired>
            <FormLabel>Primary Fitness Goal</FormLabel>
            <Select
              value={goals.primaryGoal}
              onChange={(e) => handleChange('primaryGoal', e.target.value)}
            >
              <option value="">Select goal</option>
              <option value="weight_loss">Weight Loss</option>
              <option value="muscle_gain">Muscle Gain</option>
              <option value="endurance">Improve Endurance</option>
              <option value="strength">Build Strength</option>
              <option value="flexibility">Increase Flexibility</option>
              <option value="general_fitness">General Fitness</option>
            </Select>
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Current Weight (kg)</FormLabel>
            <NumberInput>
              <NumberInputField
                value={goals.currentWeight}
                onChange={(e) => handleChange('currentWeight', e.target.value)}
              />
            </NumberInput>
          </FormControl>

          <FormControl>
            <FormLabel>Target Weight (kg)</FormLabel>
            <NumberInput>
              <NumberInputField
                value={goals.targetWeight}
                onChange={(e) => handleChange('targetWeight', e.target.value)}
              />
            </NumberInput>
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Height (cm)</FormLabel>
            <NumberInput>
              <NumberInputField
                value={goals.height}
                onChange={(e) => handleChange('height', e.target.value)}
              />
            </NumberInput>
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Age</FormLabel>
            <NumberInput>
              <NumberInputField
                value={goals.age}
                onChange={(e) => handleChange('age', e.target.value)}
              />
            </NumberInput>
          </FormControl>

          <FormControl as="fieldset" isRequired>
            <FormLabel as="legend">Gender</FormLabel>
            <RadioGroup
              value={goals.gender}
              onChange={(value) => handleChange('gender', value)}
            >
              <Stack direction="row">
                <Radio value="male">Male</Radio>
                <Radio value="female">Female</Radio>
                <Radio value="other">Other</Radio>
              </Stack>
            </RadioGroup>
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Activity Level</FormLabel>
            <Select
              value={goals.activityLevel}
              onChange={(e) => handleChange('activityLevel', e.target.value)}
            >
              <option value="">Select level</option>
              <option value="sedentary">Sedentary (little or no exercise)</option>
              <option value="light">Lightly active (1-3 days/week)</option>
              <option value="moderate">Moderately active (3-5 days/week)</option>
              <option value="very">Very active (6-7 days/week)</option>
              <option value="extra">Extra active (very active + physical job)</option>
            </Select>
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Time Commitment (hours per week)</FormLabel>
            <NumberInput>
              <NumberInputField
                value={goals.timeCommitment}
                onChange={(e) => handleChange('timeCommitment', e.target.value)}
              />
            </NumberInput>
          </FormControl>

          <FormControl>
            <FormLabel>Preferred Workouts</FormLabel>
            <Stack spacing={2}>
              {['Running', 'Cycling', 'Swimming', 'Weight Training', 'Yoga', 'HIIT', 'Pilates', 'Boxing'].map((workout) => (
                <Checkbox
                  key={workout}
                  isChecked={goals.preferredWorkouts.includes(workout)}
                  onChange={() => handlePreferredWorkoutsChange(workout)}
                >
                  {workout}
                </Checkbox>
              ))}
            </Stack>
          </FormControl>

          <FormControl>
            <FormLabel>Medical Conditions or Injuries</FormLabel>
            <Textarea
              value={goals.medicalConditions}
              onChange={(e) => handleChange('medicalConditions', e.target.value)}
              placeholder="Please list any relevant medical conditions or injuries..."
            />
          </FormControl>

          <FormControl>
            <FormLabel>Dietary Restrictions</FormLabel>
            <Textarea
              value={goals.dietaryRestrictions}
              onChange={(e) => handleChange('dietaryRestrictions', e.target.value)}
              placeholder="Please list any dietary restrictions or preferences..."
            />
          </FormControl>

          <FormControl>
            <FormLabel>Additional Notes</FormLabel>
            <Textarea
              value={goals.additionalNotes}
              onChange={(e) => handleChange('additionalNotes', e.target.value)}
              placeholder="Any other information you'd like to share..."
            />
          </FormControl>

          <Button
            type="submit"
            colorScheme="blue"
            isLoading={loading}
            loadingText="Updating..."
          >
            Update Fitness Goals
          </Button>
        </VStack>
      </form>
    </Box>
  )
}
