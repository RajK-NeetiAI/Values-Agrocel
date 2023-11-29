from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain.vectorstores.qdrant import Qdrant
from langchain.chains import LLMChain
from langchain.schema.document import Document

import config
from utils import *


def format_context(documents: list[Document]) -> str:
    formated_context = ''
    for doc in documents:
        formated_context += f'\n{doc.page_content}\n'
    return formated_context


def format_chat_history(chat_history: list[list[str, str]]) -> str:
    chat_history = chat_history[:-1]
    formated_chat_history = ''
    for ch in chat_history:
        formated_chat_history += f'HUMAN: {ch[0]}\nAI: {ch[1]}\n'
    return formated_chat_history


def condense_user_query(query: str, chat_history: list[list]) -> tuple:
    system_prompt = '''Given the following CHAT HISTORY and a FOLLOW UP QUESTION, \
rephrase the FOLLOW UP QUESTION to be a STANDALONE QUESTION in its original language. \
Keep the context of the CHAT HISTORY in the standalone question.'''
    instruction = "CHAT HISTORY:\n\n{chat_history}\n\nFOLLOW UP QUESTION: {question}\n\nSTANDALONE QUESTION:"
    template = f'{system_prompt}\n{instruction}'
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(template)
        ]
    )
    if len(chat_history) <= 1:
        return query
    formated_chat_history = format_chat_history(chat_history)
    llm_chain = LLMChain(
        llm=config.chat_model,
        prompt=prompt,
        verbose=True
    )
    response = llm_chain.predict(
        question=query, chat_history=formated_chat_history)
    response = response.strip()
    return response


def create_llm_conversation(chat_history: list) -> list[list]:
    try:
        query = chat_history[-1][0]
        vector_db = Qdrant(client=config.qdrant_client, embeddings=config.embedding_function,
                           collection_name=config.COLLECTION_NAME)
        system_prompt = '''You are a helpful assistant. \
Use the following pieces of CONTEXT and CHAT HISTORY to answer the QUESTION at the end. \
Keep all you answers short and concise. \
If you don't know the answer and the CONTEXT doesn't contain the answer truthfully say I don't know. \
Keep an informative tone.'''
        instruction = "CONTEXT: {context}\n\nCHAT HISTORY:\n\n{chat_history}\n\nHUMAN: {question}\n\nAI:"
        template = f'{system_prompt}\n{instruction}'
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(template)
            ]
        )
        llm_chain = LLMChain(
            llm=config.chat_model,
            prompt=prompt,
            verbose=True
        )
        condense_query = condense_user_query(query, chat_history)
        searched_docs = vector_db.similarity_search(condense_query)
        formated_chat_history = format_chat_history(chat_history)
        formated_context = format_context(searched_docs)
        response = llm_chain.predict(
            question=query, context=formated_context, chat_history=formated_chat_history)
        response = response.strip()
        chat_history[-1][1] = response
        return chat_history
    except:
        chat_history.append((chat_history[-1][0], config.ERROR_MESSAGE))
        return chat_history


def create_llm_conversation_audio(chat_history: list, audio_msg: str) -> list[list]:
    try:
        query = chat_history[-1][0]
        vector_db = Qdrant(client=config.qdrant_client, embeddings=config.embedding_function,
                           collection_name=config.COLLECTION_NAME)
        system_prompt = '''You are a helpful assistant. \
Use the following pieces of CONTEXT and CHAT HISTORY to answer the QUESTION at the end. \
Keep all you answers short and concise. \
If you don't know the answer and the CONTEXT doesn't contain the answer truthfully say I don't know. \
Keep an informative tone.'''
        instruction = "CONTEXT: {context}\n\nCHAT HISTORY:\n\n{chat_history}\n\nHUMAN: {question}\n\nAI:"
        template = f'{system_prompt}\n{instruction}'
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(template)
            ]
        )
        llm_chain = LLMChain(
            llm=config.chat_model,
            prompt=prompt,
            verbose=True
        )
        condense_query = condense_user_query(query, chat_history)
        searched_docs = vector_db.similarity_search(condense_query)
        formated_chat_history = format_chat_history(chat_history)
        formated_context = format_context(searched_docs)
        response = llm_chain.predict(
            question=query, context=formated_context, chat_history=formated_chat_history)
        response = response.strip()
        chat_history[-1][1] = response
        return chat_history, response
    except:
        chat_history.append((chat_history[-1][0], config.ERROR_MESSAGE))
        return chat_history, config.ERROR_MESSAGE


def handle_user_query(message: str, chat_history: list[tuple]) -> tuple:
    chat_history += [[message, None]]
    return '', chat_history


def handle_user_voice_query(audio_file_path: str, chat_history: list[tuple]) -> tuple:
    audio_to_text = transcribe_audio(audio_file_path)
    chat_history += [[audio_to_text, None]]
    return None, chat_history


def set_audio_output(text: str) -> str:
    audio_file_path = create_speech(text)
    return audio_file_path
