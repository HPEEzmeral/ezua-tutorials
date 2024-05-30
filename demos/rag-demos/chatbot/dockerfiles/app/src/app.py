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

URL = "http://agent.{0}:9000/{1}"

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
    response = requests.post(
        URL.format(NAMESPACE, "invoke"), json=inputs, headers=headers)

    logger.info(f"Response: {response.text}")

    bot_message = response.json()["output"]

    logger.info(f"Bot message: {bot_message}")

    chat_history.append((message, bot_message))
    
    return "", chat_history


def upload_document(files, request: gr.Request):
    headers = {"Authorization": request.headers.get("authorization")}

    # Create a list of documents (when valid)
    list_file_path = [x.name for x in files if x is not None]

    for file_path in list_file_path:
        logger.info(f"Uploading file: {file_path}")
    
        f = {'file': open(file_path, 'rb')}

        response = requests.post(
            URL.format(NAMESPACE,"uploadpdf"), files=f, headers=headers)
        
    if response.status_code == 200:
        logger.info("PDF file uploaded successfully.")
        return "PDF file uploaded successfully!"

    return "An error occurred while uploading the PDF file."


def main():
    with gr.Blocks(theme=EzmeralTheme(), css=custom_css) as app:
        with gr.Tab("Chat"):
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
        with gr.Tab("Private Knowledge Base"):
            with gr.Column(scale = 86):
                gr.Markdown(
                    "<b>Upload a new PDF file and extend the private knowledge base.</b>"
                )
                with gr.Row():
                    document = gr.Files(
                        height=300, file_count="multiple",
                        file_types=["pdf"], interactive=True,
                        label="Upload PDF documents")
                with gr.Row():
                    upload_btn = gr.Button("Upload PDF")
                with gr.Row():
                    db_progress = gr.Textbox(
                        value="Waiting...", show_label=False)

        inputs = [msg, chatbot, ctx, temperature, max_tokens]

        submit_btn.click(chat_service, inputs, [msg, chatbot])
        upload_btn.click(
            upload_document, inputs=[document], outputs=[db_progress])
        clear_btn.click

        msg.submit(chat_service, inputs, [msg, chatbot])

    app.launch(server_name="0.0.0.0", server_port=8080)


if __name__ == "__main__":
    main()
