import os

from dotenv import load_dotenv, find_dotenv
from qdrant_client import QdrantClient
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from openai import OpenAI

load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

ERROR_MESSAGE = 'We are facing a technical issue at this moment.'

COLLECTION_NAME = 'values_knowledge'
QDRANT_URL = os.getenv('QDRANT_URL')

qdrant_client = QdrantClient(url=QDRANT_URL)

embedding_function = OpenAIEmbeddings(
    openai_api_key=OPENAI_API_KEY
)

chat_model = ChatOpenAI(
    temperature=0,
    openai_api_key=OPENAI_API_KEY,
    model_name='gpt-4'
)

openai_client = OpenAI(
    api_key=OPENAI_API_KEY
)
