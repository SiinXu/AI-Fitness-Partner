import { ChakraProvider } from '@chakra-ui/react'
import { AppProps } from 'next/app'
import { AuthProvider } from '../contexts/AuthContext'
import { ApiProvider } from '../contexts/ApiContext'
import theme from '../styles/theme'

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ChakraProvider theme={theme}>
      <AuthProvider>
        <ApiProvider>
          <Component {...pageProps} />
        </ApiProvider>
      </AuthProvider>
    </ChakraProvider>
  )
}

export default MyApp
