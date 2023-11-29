import gradio as gr

from conversation import create_llm_conversation, handle_user_query, handle_user_voice_query

with gr.Blocks() as text_chat:
    chatbot = gr.Chatbot(label='Talk to the Douments', bubble_full_width=False)
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

with gr.Blocks() as voice_chat:
    chatbot = gr.Chatbot(label='Talk to the Douments', bubble_full_width=False)
    voice_chat_audio_file_path = gr.Audio(
        sources=["microphone"], label='Record your query', type='filepath')
    with gr.Row():
        voice_chat_submit = gr.Button('Submit', variant='primary')
        voice_chat_clear = gr.ClearButton(
            [voice_chat_audio_file_path, chatbot], variant='stop')

    voice_chat_submit.click(
        handle_user_voice_query,
        [voice_chat_audio_file_path, chatbot],
        [voice_chat_audio_file_path, chatbot]
    ).then(
        create_llm_conversation,
        [chatbot],
        [chatbot]
    )


demo = gr.TabbedInterface([text_chat, voice_chat],
                          ['Text Chat', 'Voice Chat'], css='footer {visibility: hidden}')

demo.queue()
