import json
import logging

import argparse
import gradio as gr
import requests
from theme import EzmeralTheme


DOMAIN_NAME = "svc.cluster.local"
NAMESPACE = open(
    "/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r").read()


HEADER = """
    <div style='text-align: center;'>
        <img src='file/app-header.png' alt='ai-enabled-search' 
             style='max-width: 100%; margin-left: auto; margin-right: auto;
             height: auto;'>
    </div>
"""


EXAMPLES = [
    ["What is EzPresto?"],
    ["How do I get started with Ezmeral Unified Analytics?"],
    ["What are the major deep learning frameworks that Determined is compatible with?"],
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

subdomain = None
model_name = None


def llm_service(
    question,
    temperature,
    num_docs,
    max_tokens,
    top_k,
    top_p,
    context_check,
    request: gr.Request,
):
    SVC = f"{subdomain}.{NAMESPACE}.{DOMAIN_NAME}"
    URL = f"https://{SVC}/v1/models/{model_name}:predict"

    data = {
        "input": question,
        "max_tokens": int(max_tokens),
        "top_k": int(top_k),
        "top_p": top_p,
        "num_docs": int(num_docs),
        "temperature": temperature,
    }

    if not context_check:
        data = {**data, **{"context": " "}}

    payload = {"instances": [data]}

    headers = {"Authorization": request.headers.get("authorization")}
    response = requests.post(URL, json=payload, headers=headers, verify=False)

    text = json.loads(response.text)["outputs"][2]["data"][0]
    trimmed_text = (
        text.split("[INST]", 1)[-1].split("[/INST]", 1)[0]
        if "[INST]" in text and "[/INST]" in text
        else text
    )
    result = (
        text.replace(trimmed_text, "")
        .replace("[INST]", "")
        .replace("[/INST]", "")
        .strip()
    )

    return result


def main(llm_server_subdomain, llm_name):
    global subdomain, model_name
    subdomain = llm_server_subdomain
    model_name = llm_name

    with gr.Blocks(theme=EzmeralTheme()) as app:
        # Application Header
        gr.HTML(HEADER)

        # Main Section
        with gr.Row():
            question = gr.Textbox(label="Question", autofocus=True)
        with gr.Row():
            with gr.Column():
                submit_btn = gr.Button("Submit", variant="primary")
            with gr.Column():
                clear_btn = gr.ClearButton(value="Reset", variant="secondary")
        
        # Advanced Settings
        with gr.Accordion("Advanced options", open=False):
            with gr.Row():
                with gr.Column():
                    temperature = gr.Slider(
                        label="Temperature",
                        minimum=0.0,
                        maximum=1.0,
                        value=0.2,
                        info="The model temperature. Larger values increase"
                             " creativity but decrease factuality.",
                    )
                    max_tokens = gr.Number(
                        label="Max Tokens",
                        minimum=10,
                        maximum=1000,
                        value=100,
                        info="The maximum number of tokens to generate.",
                    )
                    num_docs = gr.Number(
                        label="Number of documents to retrieve",
                        minimum=1,
                        maximum=4,
                        value=4,
                        info="The maximum number of documents to retrieve"
                             " from the vector store.",
                    )
                with gr.Column():
                    top_k = gr.Number(
                        label="Top k",
                        minimum=5,
                        maximum=200,
                        value=40,
                        info="Randomly sample from the top_k most likely"
                             " tokens at each generation step. Set this to 1"
                             " for greedy decoding.",
                    )
                    top_p = gr.Slider(
                        label="Top p",
                        minimum=0.1,
                        maximum=1.0,
                        value=0.4,
                        info="Randomly sample at each generation step from the"
                             " top most likely tokens whose probabilities add"
                             " up to top_p.",
                    )
            with gr.Row():
                context_check = gr.Checkbox(
                    value=True,
                    label="Use knowledge base",
                    info="Do you want to retrieve and use relevant context"
                         " from your knowledge database?",
                )
        
        # Output Section
        output = gr.Textbox(label="Answer")

        # Examples Section
        gr.Examples(examples=EXAMPLES, inputs=[question])

        # Event Handlers
        submit_btn.click(
            fn=llm_service,
            inputs=[
                question,
                temperature,
                num_docs,
                max_tokens,
                top_k,
                top_p,
                context_check,
            ],
            outputs=[output],
        )

        clear_btn.click(
            lambda: [None, 0.2, 4, 100, 40, 0.4, True, None],
            [],
            outputs=[
                question,
                temperature,
                num_docs,
                max_tokens,
                top_k,
                top_p,
                context_check,
                output,
            ],
        )

    app.launch(server_name="0.0.0.0", server_port=8080)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--llm-server-subdomain", type=str,
                        default="ensemble-transformer")
    parser.add_argument("--llm-name", type=str, default="ensemble")
    args = parser.parse_args()

    logger.info("LLM Server Subdomain: %s", args.llm_server_subdomain)
    logger.info("Model Name: %s", args.llm_name)

    main(args.llm_server_subdomain, args.llm_name)
