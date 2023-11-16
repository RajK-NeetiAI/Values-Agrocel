import os

from dotenv import load_dotenv, find_dotenv
from qdrant_client import QdrantClient
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI

load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

COLLECTION_NAME = 'values_database'
QDRANT_URL = 'http://localhost:6333'

ERROR_MESSAGE = 'We are facing technical issue at this moment.'

client = QdrantClient(
    host='localhost',
    port=6333
)

embedding_function = OpenAIEmbeddings(
    openai_api_key=OPENAI_API_KEY
)

chat_model = ChatOpenAI(
    temperature=0,
    openai_api_key=OPENAI_API_KEY,
    model_name='gpt-4'
)
