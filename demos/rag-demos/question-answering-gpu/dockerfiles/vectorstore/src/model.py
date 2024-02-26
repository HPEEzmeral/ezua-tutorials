import logging
import argparse

import kserve

from langchain.vectorstores import Chroma

from utils import download_directory
from embeddings import EmbeddingsClient


logger = logging.getLogger(__name__)

DEFAULT_NUM_DOCS = 2


class VectorStore(kserve.Model):
    def __init__(
        self, name: str, persist_uri: str, model_endpoint: str, model_name: str
    ):
        super().__init__(name)
        self.name = name
        self._prepare_vectorstore(persist_uri, model_endpoint, model_name)

        self.ready = True

    def _prepare_vectorstore(
            self, uri: str, model_endpoint: str, model_name: str, ):
        self.embeddings = EmbeddingsClient(model_endpoint, model_name)
        persist_dir = download_directory(uri)
        self.vectordb = Chroma(
            persist_directory=persist_dir, embedding_function=self.embeddings
        )

    def predict(self, request: dict, headers: dict) -> dict:
        authorization = headers["authorization"]
        self.embeddings.authorization = authorization

        data = request["instances"][0]
        query = data["input"]
        num_docs = data.get("num_docs", DEFAULT_NUM_DOCS)

        logger.info(f"Received question: {query}")

        docs = self.vectordb.similarity_search(query, k=num_docs)

        logger.info(f"Retrieved context: {docs}")

        return {"predictions": [doc.page_content for doc in docs]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="VectorStore", description="VectorStore server"
    )
    parser.add_argument(
        "--persist-uri",
        type=str,
        required=True,
        help="The location of the persisted VectorStore.",
    )
    parser.add_argument(
        "--model-endpoint",
        type=str,
        default="bge-predictor",
        help="The endpoint of the embeddings model inference service.",
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default="bge",
        help="The name of the embeddings model.",
    )
    args = parser.parse_args()

    model = VectorStore(
        "vectorstore", args.persist_uri, args.model_endpoint, args.model_name
    )
    kserve.ModelServer(workers=1).start([model])
