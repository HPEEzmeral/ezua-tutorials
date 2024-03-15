import json
import requests

import gradio as gr
from theme import EzmeralTheme


DOMAIN_NAME = "svc.cluster.local"
NAMESPACE = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r").read()
DEPLOYMENT_NAME = "llm"
MODEL_NAME = DEPLOYMENT_NAME
SVC = f"{DEPLOYMENT_NAME}-transformer.{NAMESPACE}.{DOMAIN_NAME}"
URL = f"https://{SVC}/v1/models/{MODEL_NAME}:predict"

HEADER = """
    <div style='text-align: center;'>
        <img src='file/app-header.png' alt='ai-enabled-search' 
             style='max-width: 100%; margin-left: auto; margin-right: auto;
             height: auto;'>
    </div>
"""

example_questions = [
    ["When was Ada Lovelace born?"],
    ["What are Linux cgroups?"],
    ["What was the name of the first Computer?"]
]


def llm_service(question, temperature, num_docs, max_tokens,
                top_k, top_p, context_check, request: gr.Request):

    data = {
            "input": question,
            "max_tokens": int(max_tokens),
            "top_k": int(top_k),
            "top_p": top_p,
            "num_docs": int(num_docs),
            "temperature": temperature
        }
    
    if not context_check:
        data = {**data, **{"context": " "}}

    payload = {"instances": [data]}

    headers = {"Authorization": request.headers.get("authorization")}
    response = requests.post(URL, json=payload, headers=headers, verify=False)

    return json.loads(response.text)["predictions"][0]


if __name__ == "__main__":
    with gr.Blocks(theme=EzmeralTheme()) as app:
        # Application Header
        gr.HTML(HEADER)
        with gr.Row():
            question = gr.Textbox(label="Question", autofocus=True)
        with gr.Row():
            with gr.Column():
                submit_btn = gr.Button("Submit", variant="primary")
            with gr.Column():
                clear_btn = gr.ClearButton(value="Reset", variant="secondary")
        with gr.Accordion("Advanced options", open=False):
            with gr.Row():
                with gr.Column():
                    temperature = gr.Slider(
                        label="Temperature",
                        minimum=0.0, maximum=1.0, value=0.2,
                        info="The model temperature. Larger values increase"
                            " creativity but decrease factuality.")
                    max_tokens = gr.Number(
                        label="Max Tokens",
                        minimum=10, maximum=1000, value=100,
                        info="The maximum number of tokens to generate.")
                    num_docs = gr.Number(
                        label="Number of documents to retrieve",
                        minimum=1, maximum=4, value=1,
                        info="The maximum number of documents to retrieve"
                             " from the vector store.")
                with gr.Column():
                    top_k = gr.Number(
                        label="Top k", minimum=5, maximum=200, value=40,
                        info="Randomly sample from the top_k most likely"
                             " tokens at each generation step. Set this to 1"
                             " for greedy decoding.")
                    top_p = gr.Slider(
                        label="Top p", minimum=0.1, maximum=1.0, value=0.4,
                        info="Randomly sample at each generation step from the"
                            " top most likely tokens whose probabilities add"
                            " up to top_p.")
            with gr.Row():
                context_check = gr.Checkbox(
                    value=True, label="Use knowledge base",
                    info="Do you want to retrieve and use relevant context"
                         " from your knowledge database?")

        output = gr.Textbox(label="Answer")

        examples = gr.Examples(examples=example_questions, inputs=[question])
                
        submit_btn.click(fn=llm_service,
                         inputs=[question, temperature,
                                 num_docs, max_tokens, top_k, top_p,
                                 context_check],
                         outputs=[output])
        clear_btn.click(
            lambda: [None, .2, 1, 100, 40, .4, True, None], [],
            outputs=[question, temperature, num_docs,
                     max_tokens, top_k, top_p, context_check, output])

    app.launch(server_name="0.0.0.0", server_port=8080)
