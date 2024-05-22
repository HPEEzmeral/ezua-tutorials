# Standard library imports
import os
import logging
from typing import List, Tuple, Dict, Any

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from fastapi import FastAPI

from langserve import add_routes
from chains import get_avatar_chain


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
