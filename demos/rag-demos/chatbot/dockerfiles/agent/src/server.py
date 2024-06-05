# Standard library imports
import os
import io
import logging
import tempfile
from typing import Dict, Any

import uvicorn
from pydantic import BaseModel
from fastapi import (FastAPI, APIRouter, Request,
                     UploadFile, File, HTTPException)
from langchain.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langserve import add_routes
from chains import get_avatar_chain, get_vector_store


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HOST = os.environ.get("LANGSERVE_HOST")
PORT = int(os.environ.get("LANGSERVE_PORT"))


app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's"
                " Runnable interfaces",
)
router = APIRouter()


@app.post("/uploadpdf/")
async def upload_pdf(file: UploadFile, req: Request):
    os.environ["AUTH_TOKEN"] = req.headers["authorization"]

    print(req.headers)

    # Read the uploaded file into memory
    file_content = await file.read()

    # Use BytesIO to handle the file in memory
    pdf_stream = io.BytesIO(file_content)

    # Create a temporary file to store the PDF content
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_stream.getbuffer())
        tmp_file_path = tmp_file.name

    # Use LangChain's PyPDFLoader to read the PDF contents from the temporary file
    loader = PyPDFLoader(file_path=tmp_file_path)
    documents = loader.load()

    print(f"Loaded {len(documents)} documents from the PDF file.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    vectorstore = get_vector_store()
    vectorstore.add_documents(docs)

    # Extract text from the documents
    contents = "\n".join([doc.page_content for doc in documents])

    return {"contents": contents}


app.include_router(router)


def set_auth_token(config: Dict[str, Any], req: Request) -> Dict[str, Any]:
    logger.info(f"Request headers: {req.headers}")

    if "authorization" in req.headers:
        os.environ["AUTH_TOKEN"] = req.headers["authorization"]
    else:
        raise HTTPException(401, "No authorization token provided.")

    return config


def main():
    chain = get_avatar_chain()
    add_routes(
        app,
        chain.with_types(input_type=Dict, output_type=str),
        per_req_config_modifier=set_auth_token)
    uvicorn.run(app, host=HOST, port=int(PORT))


if __name__ == "__main__":
    main()
