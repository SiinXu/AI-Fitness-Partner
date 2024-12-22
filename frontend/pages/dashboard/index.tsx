import {
  Box,
  Container,
  Grid,
  Heading,
  Text,
  useColorModeValue,
  VStack,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  SimpleGrid,
  Tabs,
  TabList,
  Tab,
  TabPanels,
  TabPanel,
} from '@chakra-ui/react'
import { useAuth } from '../../contexts/AuthContext'
import Layout from '../../components/Layout'
import { useEffect, useState } from 'react'
import axios from 'axios'
import UploadWorkout from '../../components/UploadWorkout'
import WorkoutAnalysis from '../../components/WorkoutAnalysis'
import WorkoutPlan from '../../components/WorkoutPlan'
import FitnessGoals from '../../components/FitnessGoals'
import KnowledgeBase from '../../components/KnowledgeBase'
import VoiceInteraction from '../../components/VoiceInteraction'

export default function Dashboard() {
  const { user } = useAuth()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const bgColor = useColorModeValue('white', 'gray.700')

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await axios.get('/api/fitness/stats')
        setStats(response.data)
      } catch (error) {
        console.error('Failed to fetch stats:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
  }, [])

  return (
    <Layout>
      <Container maxW="container.xl" py={8}>
        <VStack spacing={8} align="stretch">
          <Box>
            <Heading size="lg">Welcome back, {user?.username}!</Heading>
            <Text mt={2} color="gray.600">
              Here's your fitness overview
            </Text>
          </Box>

          <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
            <Box p={6} bg={bgColor} borderRadius="lg" boxShadow="sm">
              <Stat>
                <StatLabel>Total Workouts</StatLabel>
                <StatNumber>{stats?.totalWorkouts || 0}</StatNumber>
                <StatHelpText>This month</StatHelpText>
              </Stat>
            </Box>
            <Box p={6} bg={bgColor} borderRadius="lg" boxShadow="sm">
              <Stat>
                <StatLabel>Active Minutes</StatLabel>
                <StatNumber>{stats?.activeMinutes || 0}</StatNumber>
                <StatHelpText>This week</StatHelpText>
              </Stat>
            </Box>
            <Box p={6} bg={bgColor} borderRadius="lg" boxShadow="sm">
              <Stat>
                <StatLabel>Current Streak</StatLabel>
                <StatNumber>{stats?.currentStreak || 0}</StatNumber>
                <StatHelpText>Days</StatHelpText>
              </Stat>
            </Box>
          </SimpleGrid>

          <Tabs variant="enclosed">
            <TabList>
              <Tab>Upload Workout</Tab>
              <Tab>Analysis</Tab>
              <Tab>Workout Plan</Tab>
              <Tab>Fitness Goals</Tab>
              <Tab>Knowledge Base</Tab>
              <Tab>Voice Assistant</Tab>
            </TabList>

            <TabPanels>
              <TabPanel>
                <UploadWorkout />
              </TabPanel>
              <TabPanel>
                <WorkoutAnalysis />
              </TabPanel>
              <TabPanel>
                <WorkoutPlan />
              </TabPanel>
              <TabPanel>
                <FitnessGoals />
              </TabPanel>
              <TabPanel>
                <KnowledgeBase />
              </TabPanel>
              <TabPanel>
                <VoiceInteraction />
              </TabPanel>
            </TabPanels>
          </Tabs>
        </VStack>
      </Container>
    </Layout>
  )
}
