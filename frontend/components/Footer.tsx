import {
  Box,
  Container,
  Stack,
  Text,
  useColorModeValue
} from '@chakra-ui/react'

export default function Footer() {
  return (
    <Box
      bg={useColorModeValue('gray.50', 'gray.900')}
      color={useColorModeValue('gray.700', 'gray.200')}
    >
      <Container
        as={Stack}
        maxW="container.xl"
        py={4}
        direction={{ base: 'column', md: 'row' }}
        spacing={4}
        justify={{ base: 'center', md: 'space-between' }}
        align={{ base: 'center', md: 'center' }}
      >
        <Text>© 2024 AI Fitness Partner. All rights reserved</Text>
        <Stack direction="row" spacing={6}>
          <Box as="a" href="#">
            Privacy
          </Box>
          <Box as="a" href="#">
            Terms
          </Box>
          <Box as="a" href="#">
            Contact
          </Box>
        </Stack>
      </Container>
    </Box>
  )
}
