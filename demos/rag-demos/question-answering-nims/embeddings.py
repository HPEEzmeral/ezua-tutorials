import json
import requests


class EmbeddingsModelClient:
    def __init__(
        self,
        model_name: str,
        domain_name: str,
        deployment_name: str,
        namespace: str,
        token: str,
    ):
        svc = f"{deployment_name}.{namespace}.{domain_name}"
        self.url = f"https://{svc}/v1/embeddings"
        self.model_name = model_name
        self.headers = {"Authorization": f"Bearer {token}"}
        
    def __call__(self, texts):
        return self.embed_documents(texts)
    
    def embed_query(self, query):
        return self.embed_documents(query)[0]

    def embed_documents(self, texts):
        data = {
          "input": texts,
          "model": self.model_name,
          "input_type": "query"
        }

        response = requests.post(
            self.url, json=data, headers=self.headers, verify=False)
        result = json.loads(response.text)["data"]
        embeddings = [item["embedding"] for item in result]

        return embeddings
