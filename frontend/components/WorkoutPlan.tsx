import {
  Box,
  Button,
  Heading,
  Text,
  VStack,
  List,
  ListItem,
  ListIcon,
  useToast,
  Badge,
  HStack,
  Divider,
} from '@chakra-ui/react'
import { useState, useEffect } from 'react'
import axios from 'axios'
import { MdFitnessCenter } from 'react-icons/md'

export default function WorkoutPlan() {
  const [loading, setLoading] = useState(false)
  const [plan, setPlan] = useState<any>(null)
  const toast = useToast()

  const fetchPlan = async () => {
    setLoading(true)
    try {
      const response = await axios.get('/api/fitness/plan')
      setPlan(response.data)
    } catch (error) {
      toast({
        title: 'Error',
        description: error.response?.data?.error || 'Failed to fetch workout plan',
        status: 'error',
        duration: 5000,
        isClosable: true,
      })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchPlan()
  }, [])

  const generateNewPlan = async () => {
    setLoading(true)
    try {
      const response = await axios.post('/api/fitness/plan/generate')
      setPlan(response.data)
      toast({
        title: 'Success',
        description: 'New workout plan generated successfully',
        status: 'success',
        duration: 5000,
        isClosable: true,
      })
    } catch (error) {
      toast({
        title: 'Error',
        description: error.response?.data?.error || 'Failed to generate new plan',
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
      <VStack spacing={4} align="stretch">
        <HStack justify="space-between">
          <Heading size="md">Your Workout Plan</Heading>
          <Button
            colorScheme="blue"
            size="sm"
            onClick={generateNewPlan}
            isLoading={loading}
            loadingText="Generating..."
          >
            Generate New Plan
          </Button>
        </HStack>

        {plan ? (
          <VStack spacing={4} align="stretch">
            {plan.weeks.map((week: any, weekIndex: number) => (
              <Box key={weekIndex}>
                <Heading size="sm" mb={2}>
                  Week {weekIndex + 1}
                </Heading>
                <List spacing={3}>
                  {week.days.map((day: any, dayIndex: number) => (
                    <ListItem key={dayIndex}>
                      <HStack>
                        <ListIcon as={MdFitnessCenter} color="blue.500" />
                        <Text fontWeight="bold">{day.name}:</Text>
                        <Badge colorScheme={day.intensity === 'High' ? 'red' : day.intensity === 'Medium' ? 'yellow' : 'green'}>
                          {day.intensity}
                        </Badge>
                      </HStack>
                      <Text ml={6} mt={1}>{day.workout}</Text>
                      {day.notes && <Text ml={6} fontSize="sm" color="gray.600">{day.notes}</Text>}
                    </ListItem>
                  ))}
                </List>
                {weekIndex < plan.weeks.length - 1 && <Divider my={4} />}
              </Box>
            ))}
          </VStack>
        ) : (
          <Text>Loading your personalized workout plan...</Text>
        )}
      </VStack>
    </Box>
  )
}
