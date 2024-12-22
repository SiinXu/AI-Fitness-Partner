import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  NumberInput,
  NumberInputField,
  Select,
  Stack,
  useToast,
  VStack,
} from '@chakra-ui/react'
import { useState } from 'react'
import axios from 'axios'

export default function UploadWorkout() {
  const [loading, setLoading] = useState(false)
  const [workoutData, setWorkoutData] = useState({
    type: '',
    duration: 0,
    calories: 0,
    heart_rate: 0,
    date: new Date().toISOString().split('T')[0],
  })
  const toast = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      await axios.post('/api/fitness/workouts', workoutData)
      toast({
        title: 'Success',
        description: 'Workout data uploaded successfully',
        status: 'success',
        duration: 5000,
        isClosable: true,
      })
      // Reset form
      setWorkoutData({
        type: '',
        duration: 0,
        calories: 0,
        heart_rate: 0,
        date: new Date().toISOString().split('T')[0],
      })
    } catch (error) {
      toast({
        title: 'Error',
        description: error.response?.data?.error || 'Failed to upload workout data',
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
        <VStack spacing={4}>
          <FormControl isRequired>
            <FormLabel>Workout Type</FormLabel>
            <Select
              value={workoutData.type}
              onChange={(e) => setWorkoutData({ ...workoutData, type: e.target.value })}
            >
              <option value="">Select type</option>
              <option value="running">Running</option>
              <option value="cycling">Cycling</option>
              <option value="swimming">Swimming</option>
              <option value="weightlifting">Weight Lifting</option>
              <option value="yoga">Yoga</option>
              <option value="other">Other</option>
            </Select>
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Duration (minutes)</FormLabel>
            <NumberInput min={0} value={workoutData.duration}>
              <NumberInputField
                onChange={(e) =>
                  setWorkoutData({ ...workoutData, duration: parseInt(e.target.value) || 0 })
                }
              />
            </NumberInput>
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Calories Burned</FormLabel>
            <NumberInput min={0} value={workoutData.calories}>
              <NumberInputField
                onChange={(e) =>
                  setWorkoutData({ ...workoutData, calories: parseInt(e.target.value) || 0 })
                }
              />
            </NumberInput>
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Average Heart Rate</FormLabel>
            <NumberInput min={0} max={220} value={workoutData.heart_rate}>
              <NumberInputField
                onChange={(e) =>
                  setWorkoutData({ ...workoutData, heart_rate: parseInt(e.target.value) || 0 })
                }
              />
            </NumberInput>
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Date</FormLabel>
            <Input
              type="date"
              value={workoutData.date}
              onChange={(e) => setWorkoutData({ ...workoutData, date: e.target.value })}
            />
          </FormControl>

          <Button
            type="submit"
            colorScheme="blue"
            width="full"
            isLoading={loading}
            loadingText="Uploading..."
          >
            Upload Workout
          </Button>
        </VStack>
      </form>
    </Box>
  )
}
