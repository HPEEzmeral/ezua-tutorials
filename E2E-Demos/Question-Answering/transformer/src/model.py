import os
import json
import argparse
import logging
import argparse
import requests

import httpx

from kserve import Model, ModelServer, model_server


logger = logging.getLogger(__name__)

EZAF_ENV = os.getenv("EZAF_ENV")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

PREDICTOR_URL_FORMAT = "http://{0}/v1/models/{1}:predict"


class Transformer(Model):
    def __init__(self, name: str, predictor_host: str, protocol: str,
                 use_ssl: bool, vectorstore_name: str = "vectorstore"):
        super().__init__(name)
        self.name = name
        self.predictor_host = predictor_host
        self.protocol = protocol
        self.use_ssl = use_ssl
        self.vs_name = vectorstore_name
        self.vs_url = self._build_vectorstore_url()
        self.token = self._get_token()
        self.ready = True

    def _get_namespace(self):
        return (open(
            "/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r")
            .read())

    def _build_vectorstore_url(self):
        namespace = self._get_namespace()
        svc = f'{self.vs_name}-predictor-default.{namespace}.{EZAF_ENV}.com'
        return f"https://{svc}/v1/models/{self.vs_name}:predict"

    def _get_token(self):
        token_url = (f"https://keycloak.{EZAF_ENV}.com/"
                     f"realms/UA/protocol/openid-connect/token")

        data = {
            "username" : USERNAME,
            "password" : PASSWORD,
            "grant_type" : "password",
            "client_id" : "ua-grant",
        }

        token_responce = requests.post(token_url, data=data,
                                       allow_redirects=True, verify=False)

        return token_responce.json()["access_token"]

    @property
    def _http_client(self):
        if self._http_client_instance is None:
            headers = {"Authorization": f"Bearer {self.token}"}
            self._http_client_instance = httpx.AsyncClient(headers=headers, verify=False)
        return self._http_client_instance

    def preprocess(self, request: dict, headers: dict) -> dict:
        data = request["instances"]
        question = data[0]["question"]

        logger.info(f"Received question: {question}")

        data = {
            "instances": [{
                "question": question
            }]
        }

        headers = {"Authorization": f"Bearer {self.token}"}

        logger.info(f"Receiving relevant docs from: {self.vs_url}")

        response = requests.post(self.vs_url, json=data, headers=headers,
                                 verify=False)
        
        response = json.loads(response.text) 
        
        context = "\n".join(response["predictions"])

        logger.info(f"Received documents: {context}")

        return {"instances": [{"context": context, "question": question}]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(parents=[model_server.parser])
    parser.add_argument(
        "--predictor_host", help="The URL for the model predict function",
        required=True)
    parser.add_argument(
        "--protocol", help="The protocol for the predictor", default="v1")
    parser.add_argument(
        "--model_name", help="The name that the model is served under.")
    parser.add_argument(
    "--use_ssl", help="Use ssl for connecting to the predictor", action='store_true')
    args, _ = parser.parse_known_args()

    logger.info(args)
    print(args)

    print(f"Predictor host: {args.predictor_host}")

    model = Transformer(args.model_name, args.predictor_host,
                        args.protocol, args.use_ssl)
    ModelServer().start([model])

