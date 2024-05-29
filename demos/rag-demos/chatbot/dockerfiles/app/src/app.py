import logging

import gradio as gr
import requests
from theme import EzmeralTheme


LOGO = """
[![Robot-final-comp.gif](https://i.postimg.cc/pry2R4S8/Robot-final-comp.gif)](https://postimg.cc/T5M8c7fY)
"""

NAMESPACE = open(
    "/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r"
).read()

# NAMESPACE = ""

URL = f"http://agent.{NAMESPACE}:9000/invoke"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

custom_css = """
#chatbot {
    height: calc(65vh - 50px) !important; /* Adjust the height as needed */
    overflow: auto;
}
"""


def chat_service(
        message,
        chat_history,
        ctx,
        temperature,
        max_tokens,
        request: gr.Request):
    headers = {"Authorization": request.headers.get("authorization")}

    logger.info(f"Message: {message}")
    logger.info(f"Chat history: {chat_history}")
    logger.info(f"Context: {ctx}")

    inputs = {"input": 
        {
            "question": message,
            "chat_history": chat_history,
            "ctx": ctx,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
    }
    response = requests.post(URL, json=inputs, headers=headers)

    logger.info(f"Response: {response.text}")

    bot_message = response.json()["output"]

    logger.info(f"Bot message: {bot_message}")

    chat_history.append((message, bot_message))
    
    return "", chat_history


def main():
    with gr.Blocks(theme=EzmeralTheme(), css=custom_css) as app:
        # Main Section
        with gr.Row():
            chatbot = gr.Chatbot(
                label="HPE Portfolio Assistant",
                show_copy_button=True,
                elem_id="chatbot",
                placeholder=LOGO,
            )
        with gr.Row():
            ctx = gr.Checkbox(
                value=True,
                label="Use Private Knowledge Base",
                info="Do you want to retrieve and use relevant context"
                        " from your private knowledge database?",
            )
        with gr.Row():
            msg = gr.Textbox(
                placeholder="Enter your message...",
                show_label=False,
                autofocus=True)
        with gr.Row():
            with gr.Column():
                submit_btn = gr.Button("Submit", variant="primary")
            with gr.Column():
                clear_btn = gr.ClearButton([msg, chatbot])
        with gr.Accordion("Advanced options", open=False):
            with gr.Row():
                with gr.Column():
                    temperature = gr.Slider(
                        label="Temperature",
                        minimum=0.0,
                        maximum=1.0,
                        value=0.1,
                        info="The model temperature. Larger values increase"
                             " creativity but decrease factuality.",
                    )
                with gr.Column():
                    max_tokens = gr.Number(
                        label="Max Tokens",
                        minimum=10,
                        maximum=1000,
                        value=200,
                        info="The maximum number of tokens to generate.",
                    )

        inputs = [msg, chatbot, ctx, temperature, max_tokens]

        submit_btn.click(chat_service, inputs, [msg, chatbot])
        clear_btn.click

        msg.submit(chat_service, inputs, [msg, chatbot])

    app.launch(server_name="0.0.0.0", server_port=8080)


if __name__ == "__main__":
    main()
