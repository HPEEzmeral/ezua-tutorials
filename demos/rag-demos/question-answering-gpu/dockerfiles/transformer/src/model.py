import json
import logging
import argparse
import requests

import httpx

from kserve import Model, ModelServer, model_server

PROMPT_TEMPLATE = """
[INST]
You are an AI assistant. You will be given a task. You must generate a detailed
answer.

Use the following pieces of context to answer the question at the end. If you
don't know the answer, just say that you don't know, don't try to make up an
answer.

{context}

{input}
[/INST]
"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Transformer(Model):
    def __init__(
        self,
        name: str,
        predictor_host: str,
        protocol: str,
        use_ssl: bool,
        vectorstore_endpoint: str,
        vectorstore_name: str,
    ):
        super().__init__(name)

        # KServe specific arguments
        self.name = name
        self.predictor_host = predictor_host
        self.protocol = protocol
        self.use_ssl = use_ssl
        self.ready = True

        # Transformer specific arguments
        self.vectorstore_endpoint = vectorstore_endpoint
        self.vectorstore_name = vectorstore_name

        self.vectorstore_url = self._build_vectorstore_url()

    def _get_namespace(self):
        return open(
            "/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r"
        ).read()

    def _build_vectorstore_url(self):
        domain_name = "svc.cluster.local"
        namespace = self._get_namespace()
        deployment_name = self.vectorstore_endpoint
        model_name = self.vectorstore_name

        # Build the vectorstore URL
        svc = f"{deployment_name}.{namespace}.{domain_name}"
        url = f"https://{svc}/v1/models/{model_name}:predict"
        return url

    def _build_request(
        self,
        query: str,
        context: str,
        max_tokens: int,
        top_k: int,
        top_p: float,
        temperature: float,
    ):
        prompt = PROMPT_TEMPLATE.format(context=context, input=query)

        inference_request = {
            "inputs": [
                {
                    "name": "text_input",
                    "datatype": "BYTES",
                    "shape": [1, 1],
                    "data": [f"{prompt}"],
                },
                {
                    "name": "max_tokens",
                    "datatype": "INT32",
                    "shape": [1, 1],
                    "data": [max_tokens],
                },
                {
                    "name": "top_k",
                    "datatype": "INT32",
                    "shape": [1, 1],
                    "data": [top_k],
                },
                {
                    "name": "top_p",
                    "datatype": "FP32",
                    "shape": [1, 1],
                    "data": [top_p],
                },
                {
                    "name": "temperature",
                    "datatype": "FP32",
                    "shape": [1, 1],
                    "data": [temperature],
                },
            ]
        }

        return inference_request

    @property
    def _http_client(self):
        headers = {"Authorization": self.authorization}
        self._http_client_instance = httpx.AsyncClient(
            headers=headers, verify=False
        )
        return self._http_client_instance

    def preprocess(self, request: dict, headers: dict) -> dict:
        self.authorization = headers["authorization"]

        data = request["instances"][0]
        query = data["input"]

        max_tokens = data.get("max_tokens", None)
        if not max_tokens:
            logger.warning("`max_tokens` not provided. Defaulting to 100")
            max_tokens = 100

        top_k = data.get("top_k", None)
        if not top_k:
            logger.warning("`top_k` not provided. Defaulting to 4")
            top_k = 4

        top_p = data.get("top_p", None)
        if not top_p:
            logger.warning("`top_p` not provided. Defaulting to 0.4")
            top_p = 0.4

        temperature = data.get("temperature", None)
        if not temperature:
            logger.warning("`temperature` not provided. Defaulting to 0.1")
            temperature = 0.1

        num_docs = data.get("num_docs", None)
        if not num_docs:
            logger.warning("`num_docs` not provided. Defaulting to 2")
            num_docs = 2

        context = data.get("context", None)

        if context:
            logger.info("Skipping retrieval step...")
            return self._build_request(
                query, context, max_tokens, top_k, top_p, temperature
            )
        else:
            payload = {"instances": [{"input": query, "num_docs": num_docs}]}
            headers = {"Authorization": self.authorization}

            logger.info(
                f"Receiving relevant docs from: {self.vectorstore_url}")

            response = requests.post(
                self.vectorstore_url, json=payload, headers=headers, verify=False
            )
            response = json.loads(response.text)

            context = "\n".join(response["predictions"])

            logger.info(f"Received documents: {context}")

            return self._build_request(
                query, context, max_tokens, top_k, top_p, temperature
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(parents=[model_server.parser])
    parser.add_argument(
        "--predictor_host", help="The URL for the model predict function",
        required=True
    )
    parser.add_argument(
        "--protocol", help="The protocol for the predictor", default="v1"
    )
    parser.add_argument(
        "--model_name", help="The name that the model is served under."
    )
    parser.add_argument(
        "--use_ssl", help="Use ssl for connecting to the predictor",
        action="store_true"
    )
    parser.add_argument(
        "--vectorstore_endpoint",
        default="vectorstore-predictor",
        help="The endpoint of the Vector Store Inference Service",
    )
    parser.add_argument(
        "--vectorstore_name",
        default="vectorstore",
        help="The name of the Vector Store Inference Service",
    )
    args, _ = parser.parse_known_args()

    logger.info(args)

    model = Transformer(
        args.model_name,
        args.predictor_host,
        args.protocol,
        args.use_ssl,
        args.vectorstore_endpoint,
        args.vectorstore_name,
    )
    ModelServer().start([model])
