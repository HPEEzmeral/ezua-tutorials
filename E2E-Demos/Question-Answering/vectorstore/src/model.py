import os
import logging
import argparse

import kserve

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

from utils import download_directory


logger = logging.getLogger(__name__)

EMBED_MODEL_NAME = os.getenv("EMBED_MODEL_NAME", "all-MiniLM-L6-v2")


class VectorStore(kserve.Model):
    def __init__(self, name: str, persist_uri: str):
        super().__init__(name)
        self.name = name
        self._prepare_vectorstore(persist_uri)

    def _prepare_vectorstore(self, uri: str):
        embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
        persist_dir = download_directory(uri)
        self.vectordb = Chroma(persist_directory=persist_dir,
                               embedding_function=embeddings)

    def predict(self, request: dict) -> dict:
        data = request["instances"]
        question = data[0]["question"]

        logger.info(f"Received question: {question}")

        docs = self.vectordb.similarity_search(question)

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
