import gradio as gr
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from gradio_ui import demo
from conversation import create_llm_conversation_backend

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ValuesChatRequest(BaseModel):
    query: str
    chat_history: list[list]


@app.get('/')
def home():
    return {
        'status': 1,
        'response': 'API is working, Gradio UI is running at /gradio'
    }


@app.post('/values/chat')
def values_chat(values_chat_request: ValuesChatRequest):
    query = values_chat_request.query
    chat_history = values_chat_request.chat_history
    print(f'Query - {query}')
    response = create_llm_conversation_backend(chat_history, query)
    print(f'Response - {response}')
    return {
        'status': 1,
        'response': response,
        'thread_id': ''
    }


app = gr.mount_gradio_app(app, demo, '/gradio')
