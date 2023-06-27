import os
import logging
import argparse

import kserve

from langchain.llms import GPT4All
from langchain import LLMChain, PromptTemplate


logger = logging.getLogger(__name__)

LLM_PATH = 'ggml-gpt4all-l13b-snoozy.bin'
PROMPT_TEMPLATE = """
Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Answer:
"""


class LLM(kserve.Model):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.llm = GPT4All(model=f"{os.getcwd()}/ggml-gpt4all-j-v1.3-groovy.bin",
                           allow_download=True, temp=0.2)

    def predict(self, request: dict, headers: dict) -> dict:
        data = request["instances"]
        context = data[0]["context"]
        question = data[0]["question"]
        
        logger.info(f"Received context: {context}")
        logger.info(f"Received question: {question}")
        
        prompt = PromptTemplate(
            template=PROMPT_TEMPLATE, input_variables=["context", "question"])
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run({
                       "context": context,
                       "question": question})
        logger.info(f"LLM response: {response}")

        return {"predictions": [response]}


if __name__ == "__main__":
    model = LLM("llm")
    kserve.ModelServer(workers=1).start([model])
