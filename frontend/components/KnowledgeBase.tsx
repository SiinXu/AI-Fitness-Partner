import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  useToast,
  Text,
  Icon,
  List,
  ListItem,
  HStack,
  IconButton,
  Select,
} from '@chakra-ui/react'
import { useState, useRef } from 'react'
import { MdUpload, MdDelete } from 'react-icons/md'
import api from '../utils/api'

export default function KnowledgeBase() {
  const [loading, setLoading] = useState(false)
  const [files, setFiles] = useState<File[]>([])
  const [category, setCategory] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)
  const toast = useToast()

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const newFiles = Array.from(e.target.files)
      setFiles(prev => [...prev, ...newFiles])
    }
  }

  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index))
  }

  const handleUpload = async () => {
    if (!category) {
      toast({
        title: 'Error',
        description: 'Please select a category',
        status: 'error',
        duration: 5000,
        isClosable: true,
      })
      return
    }

    if (files.length === 0) {
      toast({
        title: 'Error',
        description: 'Please select at least one file',
        status: 'error',
        duration: 5000,
        isClosable: true,
      })
      return
    }

    setLoading(true)
    const formData = new FormData()
    formData.append('category', category)
    files.forEach(file => {
      formData.append('files', file)
    })

    try {
      await api.post('/fitness/knowledge', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      
      toast({
        title: 'Success',
        description: 'Knowledge base updated successfully',
        status: 'success',
        duration: 5000,
        isClosable: true,
      })
      
      // Reset form
      setFiles([])
      setCategory('')
    } catch (error) {
      toast({
        title: 'Error',
        description: error.response?.data?.error || 'Failed to update knowledge base',
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
        <FormControl isRequired>
          <FormLabel>Knowledge Category</FormLabel>
          <Select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            placeholder="Select category"
          >
            <option value="exercise_techniques">Exercise Techniques</option>
            <option value="nutrition">Nutrition</option>
            <option value="workout_plans">Workout Plans</option>
            <option value="recovery">Recovery & Injury Prevention</option>
            <option value="supplements">Supplements</option>
            <option value="scientific_research">Scientific Research</option>
          </Select>
        </FormControl>

        <FormControl>
          <FormLabel>Upload Files</FormLabel>
          <Input
            type="file"
            display="none"
            ref={fileInputRef}
            onChange={handleFileChange}
            multiple
            accept=".pdf,.doc,.docx,.txt,.md"
          />
          <Button
            leftIcon={<Icon as={MdUpload} />}
            onClick={() => fileInputRef.current?.click()}
            width="full"
          >
            Select Files
          </Button>
          <Text mt={2} fontSize="sm" color="gray.600">
            Supported formats: PDF, DOC, DOCX, TXT, MD
          </Text>
        </FormControl>

        {files.length > 0 && (
          <Box>
            <Text fontWeight="bold" mb={2}>
              Selected Files:
            </Text>
            <List spacing={2}>
              {files.map((file, index) => (
                <ListItem key={index}>
                  <HStack justify="space-between">
                    <Text>{file.name}</Text>
                    <IconButton
                      aria-label="Remove file"
                      icon={<Icon as={MdDelete} />}
                      size="sm"
                      colorScheme="red"
                      variant="ghost"
                      onClick={() => removeFile(index)}
                    />
                  </HStack>
                </ListItem>
              ))}
            </List>
          </Box>
        )}

        <Button
          colorScheme="blue"
          onClick={handleUpload}
          isLoading={loading}
          loadingText="Uploading..."
          isDisabled={files.length === 0 || !category}
        >
          Upload to Knowledge Base
        </Button>
      </VStack>
    </Box>
  )
}
