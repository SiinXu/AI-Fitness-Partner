import {
  Box,
  Button,
  Container,
  FormControl,
  FormLabel,
  Heading,
  Input,
  Select,
  Stack,
  Text,
  useToast,
  useColorModeValue,
} from '@chakra-ui/react'
import { useState } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { useRouter } from 'next/router'
import Link from 'next/link'

export default function Register() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    fitness_level: 'beginner',
  })
  const [loading, setLoading] = useState(false)
  const { register } = useAuth()
  const router = useRouter()
  const toast = useToast()

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (formData.password !== formData.confirmPassword) {
      toast({
        title: 'Error',
        description: 'Passwords do not match',
        status: 'error',
        duration: 5000,
        isClosable: true,
      })
      return
    }

    setLoading(true)

    try {
      await register({
        username: formData.username,
        email: formData.email,
        password: formData.password,
        fitness_level: formData.fitness_level,
      })
      router.push('/dashboard')
    } catch (error) {
      toast({
        title: 'Error',
        description: error.response?.data?.error || 'Failed to register',
        status: 'error',
        duration: 5000,
        isClosable: true,
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Container maxW="lg" py={{ base: '12', md: '24' }} px={{ base: '0', sm: '8' }}>
      <Stack spacing="8">
        <Stack spacing="6">
          <Stack spacing={{ base: '2', md: '3' }} textAlign="center">
            <Heading size={{ base: 'xs', md: 'sm' }}>Create your account</Heading>
            <Text color="fg.muted">
              Already have an account?{' '}
              <Link href="/auth/login" passHref>
                <Box as="span" color="blue.500" cursor="pointer">
                  Sign in
                </Box>
              </Link>
            </Text>
          </Stack>
        </Stack>
        <Box
          py={{ base: '0', sm: '8' }}
          px={{ base: '4', sm: '10' }}
          bg={useColorModeValue('white', 'gray.700')}
          boxShadow={{ base: 'none', sm: 'md' }}
          borderRadius={{ base: 'none', sm: 'xl' }}
        >
          <form onSubmit={handleSubmit}>
            <Stack spacing="6">
              <Stack spacing="5">
                <FormControl>
                  <FormLabel>Username</FormLabel>
                  <Input
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Email</FormLabel>
                  <Input
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Password</FormLabel>
                  <Input
                    name="password"
                    type="password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Confirm Password</FormLabel>
                  <Input
                    name="confirmPassword"
                    type="password"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    required
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Fitness Level</FormLabel>
                  <Select
                    name="fitness_level"
                    value={formData.fitness_level}
                    onChange={handleChange}
                  >
                    <option value="beginner">Beginner</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                  </Select>
                </FormControl>
              </Stack>
              <Button
                type="submit"
                colorScheme="blue"
                size="lg"
                fontSize="md"
                isLoading={loading}
              >
                Create Account
              </Button>
            </Stack>
          </form>
        </Box>
      </Stack>
    </Container>
  )
}
