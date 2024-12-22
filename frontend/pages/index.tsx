import { Box, Container, Heading, Text, Button, VStack, useColorModeValue } from '@chakra-ui/react'
import { useAuth } from '../contexts/AuthContext'
import { useRouter } from 'next/router'
import Layout from '../components/Layout'

export default function Home() {
  const { user } = useAuth()
  const router = useRouter()
  const bgColor = useColorModeValue('gray.50', 'gray.900')

  return (
    <Layout>
      <Box bg={bgColor} minH="100vh" py={20}>
        <Container maxW="container.xl">
          <VStack spacing={8} textAlign="center">
            <Heading as="h1" size="2xl">
              AI Fitness Partner
            </Heading>
            <Text fontSize="xl" maxW="2xl">
              Your personalized AI-powered fitness companion that helps you achieve your health and fitness goals through customized workouts, nutrition plans, and real-time guidance.
            </Text>
            
            {!user ? (
              <VStack spacing={4}>
                <Button
                  colorScheme="blue"
                  size="lg"
                  onClick={() => router.push('/auth/register')}
                >
                  Get Started
                </Button>
                <Button
                  variant="outline"
                  size="lg"
                  onClick={() => router.push('/auth/login')}
                >
                  Login
                </Button>
              </VStack>
            ) : (
              <Button
                colorScheme="blue"
                size="lg"
                onClick={() => router.push('/dashboard')}
              >
                Go to Dashboard
              </Button>
            )}
          </VStack>
        </Container>
      </Box>
    </Layout>
  )
}
