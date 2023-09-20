import os
import logging
import argparse

import kserve

from gpt4all import GPT4All


logger = logging.getLogger(__name__)

MODEL = "orca-mini-3b.ggmlv3.q4_0.bin"

PROMPT_TEMPLATE = """
### System:
{system}

### User:
{instruction}

{context}

### Input:
{input}

Response:

"""


class LLM(kserve.Model):
    def __init__(self, name: str, model: str, model_path: str):
        super().__init__(name)
        self.name = name

        logger.info(f"Initializing model: {model}")
        self._init_model(model, model_path)

        self.ready = True

    def _init_model(self, model, model_path):
        self.model = GPT4All(
            model_name=model, model_path=model_path, allow_download=True)

    def predict(self, request: dict, headers: dict) -> dict:
        data = request["instances"][0]

        # prompt parameters
        prompt_template = data.get("prompt_template", PROMPT_TEMPLATE)
        system = data.get("system", "")
        instruction = data["instruction"]
        context = data["context"]
        query = data["input"]

        logger.info(f"Received instruction: {instruction}")
        logger.info(f"Received input: {query}")

        # generation parameters
        temperature = data.get("temperature", .2)
        max_tokens = data.get("max_tokens", 200)
        top_k = data.get("top_k", 40)
        top_p = data.get("top_p", .4)
        
        logger.info("Creating the prompt...")
        prompt = prompt_template.format(
            system=system, instruction=instruction,
            context=context, input=query)
        
        response = self.model.generate(
            prompt, max_tokens=max_tokens,
            temp=temperature, top_k=top_k, top_p=top_p)

        logger.info(f"LLM response: {response}")

        return {"predictions": [response]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model", help="The name of the LLM model to use.",
        default=MODEL)
    parser.add_argument(
        "--model_path", help="The path to the model.",
        default=os.getcwd())
    args = parser.parse_args()

    model = LLM("llm", args.model, args.model_path)
    kserve.ModelServer(workers=1).start([model])
