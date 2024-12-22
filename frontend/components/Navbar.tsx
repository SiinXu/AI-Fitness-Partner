import {
  Box,
  Flex,
  Button,
  useColorModeValue,
  Stack,
  useColorMode,
  Container,
  IconButton,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Avatar
} from '@chakra-ui/react'
import { MoonIcon, SunIcon } from '@chakra-ui/icons'
import { useAuth } from '../contexts/AuthContext'
import { useRouter } from 'next/router'

export default function Navbar() {
  const { colorMode, toggleColorMode } = useColorMode()
  const { user, logout } = useAuth()
  const router = useRouter()
  
  const bgColor = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')

  return (
    <Box
      bg={bgColor}
      borderBottom={1}
      borderStyle="solid"
      borderColor={borderColor}
      px={4}
    >
      <Container maxW="container.xl">
        <Flex h={16} alignItems="center" justifyContent="space-between">
          <Box
            cursor="pointer"
            fontWeight="bold"
            fontSize="xl"
            onClick={() => router.push('/')}
          >
            AI Fitness Partner
          </Box>

          <Flex alignItems="center">
            <Stack direction="row" spacing={7}>
              <Button onClick={toggleColorMode}>
                {colorMode === 'light' ? <MoonIcon /> : <SunIcon />}
              </Button>

              {user ? (
                <Menu>
                  <MenuButton
                    as={IconButton}
                    rounded="full"
                    variant="link"
                    cursor="pointer"
                    minW={0}
                  >
                    <Avatar size="sm" name={user.username} />
                  </MenuButton>
                  <MenuList>
                    <MenuItem onClick={() => router.push('/dashboard')}>
                      Dashboard
                    </MenuItem>
                    <MenuItem onClick={() => router.push('/profile')}>
                      Profile
                    </MenuItem>
                    <MenuItem onClick={logout}>
                      Logout
                    </MenuItem>
                  </MenuList>
                </Menu>
              ) : (
                <Stack direction="row" spacing={4}>
                  <Button
                    variant="ghost"
                    onClick={() => router.push('/auth/login')}
                  >
                    Login
                  </Button>
                  <Button
                    colorScheme="blue"
                    onClick={() => router.push('/auth/register')}
                  >
                    Sign Up
                  </Button>
                </Stack>
              )}
            </Stack>
          </Flex>
        </Flex>
      </Container>
    </Box>
  )
}
