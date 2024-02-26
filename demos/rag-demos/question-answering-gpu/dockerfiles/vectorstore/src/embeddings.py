import json
import logging
import requests


logger = logging.getLogger(__name__)


class EmbeddingsClient:
    def __init__(self, model_endpoint: str, model_name: str) -> None:
        self._url = self._build_url(model_endpoint, model_name)

    @property
    def authorization(self):
        return self._authorization

    @authorization.setter
    def authorization(self, authorization):
        self._authorization = authorization

    def _get_namespace(self):
        return open(
            "/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r"
        ).read()

    def _build_url(self, model_endpoint, model_name,):
        domain_name = "svc.cluster.local"
        namespace = self._get_namespace()

        svc = f"{model_endpoint}.{namespace}.{domain_name}"
        url = f"https://{svc}/v2/models/{model_name}/infer"

        return url

    def embed_query(self, query):
        headers = {"Authorization": self.authorization}

        logger.info(f"Sending request to {self._url} with query {query}...")

        inference_request = {
            "inputs": [
                {
                    "name": "text_input",
                    "datatype": "BYTES",
                    "shape": [1, 1],
                    "data": [f"{query}"],
                }
            ]
        }

        response = requests.post(
            self._url, json=inference_request, headers=headers, verify=False
        )

        logger.info(f"Received response: {response.text}")

        if response.status_code == 200:
            return json.loads(response.text)["outputs"][0]["data"]
