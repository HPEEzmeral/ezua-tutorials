import logging
import argparse

import kserve

from langchain.vectorstores import Chroma

from utils import download_directory
from embeddings import EmbeddingsClient


logger = logging.getLogger(__name__)

DEFAULT_NUM_DOCS = 2


class VectorStore(kserve.Model):
    def __init__(self, name: str, persist_uri: str):
        super().__init__(name)
        self.name = name
        self._prepare_vectorstore(persist_uri)

        self.ready = True

    def _prepare_vectorstore(self, uri: str):
        self.embeddings = EmbeddingsClient()
        persist_dir = download_directory(uri)
        self.vectordb = Chroma(persist_directory=persist_dir,
                               embedding_function=self.embeddings)

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
    parser = argparse.ArgumentParser(prog="VectorStore",
                                     description="VectorStore server")
    parser.add_argument("--persist-uri", type=str, required=True,
                        help="The location of the persisted VectorStore.")
    args = parser.parse_args()

    model = VectorStore("vectorstore", args.persist_uri)
    kserve.ModelServer(workers=1).start([model])
