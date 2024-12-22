import {
  Box,
  Button,
  Text,
  VStack,
  useToast,
  Icon,
  HStack,
} from '@chakra-ui/react'
import { useState, useRef, useEffect } from 'react'
import { MdMic, MdStop, MdPlayArrow } from 'react-icons/md'
import api from '../utils/api'

export default function VoiceInteraction() {
  const [isRecording, setIsRecording] = useState(false)
  const [isPlaying, setIsPlaying] = useState(false)
  const [loading, setLoading] = useState(false)
  const [lastResponse, setLastResponse] = useState<{text: string; audio: string} | null>(null)
  const mediaRecorder = useRef<MediaRecorder | null>(null)
  const audioChunks = useRef<Blob[]>([])
  const audioPlayer = useRef<HTMLAudioElement | null>(null)
  const toast = useToast()

  useEffect(() => {
    // Create audio player
    audioPlayer.current = new Audio()
    audioPlayer.current.onended = () => setIsPlaying(false)

    return () => {
      if (audioPlayer.current) {
        audioPlayer.current.pause()
        audioPlayer.current = null
      }
    }
  }, [])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorder.current = new MediaRecorder(stream)
      audioChunks.current = []

      mediaRecorder.current.ondataavailable = (event) => {
        audioChunks.current.push(event.data)
      }

      mediaRecorder.current.onstop = async () => {
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/wav' })
        await sendAudioToServer(audioBlob)
      }

      mediaRecorder.current.start()
      setIsRecording(true)
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to access microphone',
        status: 'error',
        duration: 5000,
        isClosable: true,
      })
    }
  }

  const stopRecording = () => {
    if (mediaRecorder.current && isRecording) {
      mediaRecorder.current.stop()
      setIsRecording(false)
      mediaRecorder.current.stream.getTracks().forEach(track => track.stop())
    }
  }

  const sendAudioToServer = async (audioBlob: Blob) => {
    setLoading(true)
    try {
      const formData = new FormData()
      formData.append('audio', audioBlob)

      const response = await api.post('/fitness/voice', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setLastResponse(response.data)
    } catch (error) {
      toast({
        title: 'Error',
        description: error.response?.data?.error || 'Failed to process voice command',
        status: 'error',
        duration: 5000,
        isClosable: true,
      })
    } finally {
      setLoading(false)
    }
  }

  const playResponse = () => {
    if (lastResponse?.audio && audioPlayer.current) {
      // Convert base64 to audio
      const audio = `data:audio/wav;base64,${lastResponse.audio}`
      audioPlayer.current.src = audio
      audioPlayer.current.play()
      setIsPlaying(true)
    }
  }

  return (
    <Box p={6} bg="white" borderRadius="lg" boxShadow="sm">
      <VStack spacing={4} align="stretch">
        <HStack spacing={4} justify="center">
          <Button
            leftIcon={<Icon as={MdMic} />}
            colorScheme={isRecording ? 'red' : 'blue'}
            onClick={isRecording ? stopRecording : startRecording}
            isLoading={loading}
          >
            {isRecording ? 'Stop Recording' : 'Start Recording'}
          </Button>

          {lastResponse && (
            <Button
              leftIcon={<Icon as={MdPlayArrow} />}
              onClick={playResponse}
              isDisabled={isPlaying}
              colorScheme="green"
            >
              Play Response
            </Button>
          )}
        </HStack>

        {lastResponse && (
          <Box mt={4}>
            <Text fontWeight="bold">AI Response:</Text>
            <Text>{lastResponse.text}</Text>
          </Box>
        )}

        <Text fontSize="sm" color="gray.600" textAlign="center">
          Click the microphone button and speak your fitness-related question or command
        </Text>
      </VStack>
    </Box>
  )
}
