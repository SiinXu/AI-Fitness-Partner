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
} from '@chakra-ui/react'
import { useState } from 'react'
import axios from 'axios'
import { MdCheckCircle } from 'react-icons/md'

export default function WorkoutAnalysis() {
  const [loading, setLoading] = useState(false)
  const [analysis, setAnalysis] = useState<any>(null)
  const toast = useToast()

  const analyzeWorkouts = async () => {
    setLoading(true)
    try {
      const response = await axios.get('/api/fitness/analyze')
      setAnalysis(response.data)
    } catch (error) {
      toast({
        title: 'Error',
        description: error.response?.data?.error || 'Failed to analyze workouts',
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
        <Heading size="md">Workout Analysis</Heading>
        
        <Button
          colorScheme="blue"
          onClick={analyzeWorkouts}
          isLoading={loading}
          loadingText="Analyzing..."
        >
          Analyze My Workouts
        </Button>

        {analysis && (
          <VStack spacing={4} align="stretch" mt={4}>
            <Box>
              <Heading size="sm" mb={2}>Key Insights</Heading>
              <Text>{analysis.insights}</Text>
            </Box>

            <Box>
              <Heading size="sm" mb={2}>Trends</Heading>
              <List spacing={2}>
                {analysis.trends.map((trend: any, index: number) => (
                  <ListItem key={index}>
                    <ListIcon as={MdCheckCircle} color="green.500" />
                    {trend.metric}: {trend.value}
                  </ListItem>
                ))}
              </List>
            </Box>

            {analysis.recommendations && analysis.recommendations.length > 0 && (
              <Box>
                <Heading size="sm" mb={2}>Recommendations</Heading>
                <List spacing={2}>
                  {analysis.recommendations.map((rec: string, index: number) => (
                    <ListItem key={index}>
                      <ListIcon as={MdCheckCircle} color="blue.500" />
                      {rec}
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}
          </VStack>
        )}
      </VStack>
    </Box>
  )
}
