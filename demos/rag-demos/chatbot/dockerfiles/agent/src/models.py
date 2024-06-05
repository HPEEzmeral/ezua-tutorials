import os
import json
import aiohttp
import logging
import requests

from langchain_core.pydantic_v1 import BaseModel
from langchain_core.embeddings import Embeddings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatModelClient():
    def __init__(
        self,
        model_name: str,
        infer_endpoint: str,
        num_tokens: int,
        temperature: float
    ):
        self.model_name = model_name
        self.infer_endpoint = infer_endpoint
        self.temperature = temperature
        self.num_tokens = num_tokens
        
    def __call__(self, query: str):
        return self.invoke(query)

    def invoke(self, query: str):
        data = {
          "model": self.model_name,
          "messages": [{
              "role": "user",
              "content": query,
              }],
          "max_tokens": self.num_tokens,
          "temperature": self.temperature
        }

        headers = {"Authorization": os.getenv("AUTH_TOKEN")}
        response = requests.post(
            self.infer_endpoint, json=data, headers=headers, verify=False)
    
        result = json.loads(response.text)
        
        return result["choices"][0]["message"]["content"].strip()


class EmbeddingsClient(Embeddings):
    def __init__(
            self,
            model_name: str,
            embeddings_url: str,
        ) -> None:
        self.model_name = model_name
        self._url = f"{embeddings_url}/embeddings"
        
    def __call__(self, texts: str):
        return self.embed_documents(texts)

    def embed_documents(self, texts):
        headers = {"Authorization": os.getenv("AUTH_TOKEN")}

        data = {
            "input": texts,
            "model": self.model_name,
            "input_type": "query"
        }

        response = requests.post(
            self._url, json=data, headers=headers, verify=False)

        result = json.loads(response.text)["data"]
        embeddings = [item["embedding"] for item in result]
        return embeddings

    async def aembed_documents(self, documents):
        pass

    async def aembed_query(self, query: str):
        headers = {"Authorization": os.getenv("AUTH_TOKEN")}

        inference_request = {
                "input": [query],
                "model": self.model_name,
                "input_type": "query"
            }

        print(f"Sending request to {self._url}")
        logger.info(f"Request: {inference_request}")

        async with aiohttp.ClientSession() as session:
            async with session.post(self._url, json=inference_request, headers=headers, ssl=False) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["data"][0]["embedding"]

                print(f"Failed to get embeddings for query: {query}")
                response_text = await response.text()
                print(f"Response: {response_text}")
    
                return response

    def embed_query(self, query: str):
        pass
