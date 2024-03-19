import gradio as gr

from conversation import *

with gr.Blocks(css='footer {visibility: hidden}') as demo:
    chatbot = gr.Chatbot(label='Values Knowledge', bubble_full_width=False)
    msg = gr.Textbox(label='Query', placeholder='Enter text and press enter')
    text_chat_clear = gr.ClearButton([msg, chatbot], variant='stop')

    msg.submit(
        handle_user_query,
        [msg, chatbot],
        [msg, chatbot]
    ).then(
        create_llm_conversation,
        [chatbot],
        [chatbot]
    )

demo.queue()
