from backend.agents.data_analyst import DataAnalyst
from backend.agents.fitness_coach import FitnessCoach
from backend.services.voice_service import VoiceService
import os
import json
from flask import current_app
from PyPDF2 import PdfReader
import docx
import markdown
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

class AgentManager:
    def __init__(self):
        self.data_analyst = DataAnalyst()
        self.fitness_coach = FitnessCoach()
        self.voice_service = VoiceService()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.embeddings = HuggingFaceEmbeddings()
        self.vector_store = None
        self._load_vector_store()

    def _load_vector_store(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            vector_store_path = os.path.join(base_dir, 'data', 'vector_store')
            
            if not os.path.exists(vector_store_path):
                knowledge_base_path = os.path.join(base_dir, 'data', 'knowledge_base.json')
                if not os.path.exists(knowledge_base_path):
                    current_app.logger.warning('Knowledge base not found')
                    return
                
                with open(knowledge_base_path, 'r') as f:
                    knowledge_base = json.load(f)
                
                texts = [item['content'] for item in knowledge_base]
                metadatas = [{'source': item['source']} for item in knowledge_base]
                
                self.vector_store = FAISS.from_texts(
                    texts=texts,
                    embedding=self.embeddings,
                    metadatas=metadatas
                )
                
                os.makedirs(os.path.dirname(vector_store_path), exist_ok=True)
                self.vector_store.save_local(vector_store_path)
            else:
                self.vector_store = FAISS.load_local(
                    vector_store_path,
                    self.embeddings
                )
        except Exception as e:
            current_app.logger.error(f'Error loading vector store: {str(e)}')
            self.vector_store = None

    def process_knowledge_file(self, filepath, category):
        try:
            text = self._extract_text(filepath)
            
            chunks = self.text_splitter.split_text(text)
            
            texts_with_metadata = [
                {
                    'text': chunk,
                    'metadata': {
                        'source': os.path.basename(filepath),
                        'category': category
                    }
                }
                for chunk in chunks
            ]
            
            if self.vector_store is None:
                self.vector_store = FAISS.from_texts(
                    texts=[t['text'] for t in texts_with_metadata],
                    embedding=self.embeddings,
                    metadatas=[t['metadata'] for t in texts_with_metadata]
                )
            else:
                self.vector_store.add_texts(
                    texts=[t['text'] for t in texts_with_metadata],
                    metadatas=[t['metadata'] for t in texts_with_metadata]
                )
            
            vector_store_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'vector_store')
            os.makedirs(os.path.dirname(vector_store_path), exist_ok=True)
            self.vector_store.save_local(vector_store_path)
            
        except Exception as e:
            current_app.logger.error(f'Error processing file {filepath}: {str(e)}')
            raise

    def _extract_text(self, filepath):
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext == '.pdf':
            with open(filepath, 'rb') as file:
                reader = PdfReader(file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text()
                return text
                
        elif ext in ['.doc', '.docx']:
            doc = docx.Document(filepath)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            
        elif ext == '.md':
            with open(filepath, 'r', encoding='utf-8') as file:
                return markdown.markdown(file.read())
                
        elif ext == '.txt':
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
                
        else:
            raise ValueError(f'Unsupported file type: {ext}')

    def process_audio(self, audio_file):
        return self.voice_service.speech_to_text(audio_file)

    def process_voice_command(self, text, user_id):
        try:
            if self.vector_store:
                docs = self.vector_store.similarity_search(text, k=3)
                context = '\n'.join([doc.page_content for doc in docs])
            else:
                context = ''

            response = self.fitness_coach.process_command(text, context, user_id)
            return response
        except Exception as e:
            current_app.logger.error(f'Error processing voice command: {str(e)}')
            return "I'm sorry, I couldn't process your command. Please try again."

    def generate_voice_response(self, text):
        return self.voice_service.text_to_speech(text)

    def get_workout_feedback(self, workout):
        return self.fitness_coach.analyze_workout(workout)

    def get_recommendations(self, user):
        return self.fitness_coach.get_recommendations(user)

    def get_fitness_coach(self) -> FitnessCoach:
        return self.fitness_coach

    def get_data_analyst(self) -> DataAnalyst:
        return self.data_analyst
