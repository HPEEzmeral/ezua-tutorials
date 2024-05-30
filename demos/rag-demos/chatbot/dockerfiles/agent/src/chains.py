import os

from operator import itemgetter
from typing import List, Tuple, Dict, Union

from langchain_community.llms import VLLMOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableSerializable,
    RunnableBranch,
    RunnableLambda,
    RunnableAssign
)

from models import ChatModelClient, EmbeddingsClient
from utils import (
    trim_chat_history,
    extract_json,
    stringify,
    get_schema,
    run_sql,
    debug
)
from prompts import (
    CONDENSE_QUESTION_TEMPLATE,
    TOOL_PICKER_TEMPLATE,
    SQL_GEN_TEMPLATE,
    SQL_SUM_SYS_MSG,
    SQL_SUM_TEMPLATE,
    DB_MISSING_PROMPT,
    CHAT_TEMPLATE,
    NO_CONTEXT_TEMPLATE,
    RAG_TEMPLATE
)


SQL_URL = os.getenv("SQL_URL")
LLM_URL = os.getenv("LLM_URL")
EMBEDDINGS_URL = os.getenv("EMBEDDINGS_URL")
CHAT_MODEL = os.getenv("CHAT_MODEL", "llama2-7b-chat")
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "NV-Embed-QA")
SQL_MODEL = os.getenv("SQL_MODEL", "defog/sqlcoder-7b-2")
NUM_DOCS = os.getenv("NUM_DOCS", 5)

vectorstore = None


def get_sql_chain(
    sql_model: str,
    chat_model: str
) -> RunnableSerializable[Dict[str, Union[str, List[Tuple[str, str]]]], str]:
    """
    Constructs a language model chain for generating SQL queries and summarizing results.

    Parameters::
        sqlcoder_url (str): The base URL of the sqlcoder model
        chat_model_name (str): The base URL of the sqlcoder model

    Returns:
        RunnableSerializable: A sql summarizing lcel runnable

    Example:
        model_url = "https://your-model-api.com"
        chain = get_sql_chain(model_url)
        result = chain.invoke({"question": "Can you recommend some sessions about cybersecurity?"})
        print(result)
    """
    prompt = PromptTemplate.from_template(SQL_GEN_TEMPLATE)

    sql_response = (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | sql_model.bind(stop=["[/SQL]"])
        | StrOutputParser()
    )

    prompt_response = ChatPromptTemplate.from_messages([
        ("system", SQL_SUM_SYS_MSG,),
        ("human", SQL_SUM_TEMPLATE),
    ])

    get_response = lambda x: run_sql(x["sqlquery"], "sqlite") or DB_MISSING_PROMPT

    return (
        RunnablePassthrough.assign(sqlquery=sql_response)
        | RunnablePassthrough.assign(schema=get_schema, response=get_response)
        | RunnablePassthrough.assign(answer = prompt_response | stringify | chat_model | StrOutputParser())
    )


def get_embeddings():
    embeddings = EmbeddingsClient(
        model_name=EMBEDDINGS_MODEL,
        embeddings_url=EMBEDDINGS_URL
    )

    return embeddings


def get_vector_store():
    global vectorstore
    embeddings = get_embeddings()

    print("Loading vectorstore...")

    if not vectorstore:
        try:
            vectorstore = FAISS.load_local(
                "vectorstore", embeddings,
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            print(e)
            assert vectorstore, "No vectorstore initialized."

    return vectorstore


def get_retriever(top_k: int = NUM_DOCS):
    vectorstore = get_vector_store()
    return vectorstore.as_retriever(search_kwargs={'k': top_k})


def get_rag_chain(
    chat_model: object,
    num_docs: int = NUM_DOCS
) -> RunnableSerializable[Dict[str, Union[str, List[Tuple[str, str]]]], str]:
    prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)
    retriever = get_retriever(top_k=num_docs)
    rag_chain = (
        RunnableLambda(lambda x: x["question"])
        | {"context": retriever, "question": RunnablePassthrough()}
        | RunnablePassthrough.assign(answer = prompt | stringify | chat_model | StrOutputParser())
    )

    return rag_chain


def route(
    info
) -> RunnableSerializable[Dict[str, Union[str, List[Tuple[str, str]]]], str]:
    """Takes the input question and chat history condenses it into single
    question and routes it to the appropriate chain depending on the input question.

    Parameters:
    - info (dict): Input information containing "question" and "chat_history"
      keys.

    Returns:
    - RunnableSerializable[Dict[str, Union[str, List[Tuple[str, str]]]], str]:
      A serializable runnable representing the processing chain outcome.
    """
    chat_model = ChatModelClient(
        model_name=CHAT_MODEL,
        infer_endpoint=f"{LLM_URL}/chat/completions",
        num_tokens=info.get("max_tokens", 200),
        temperature=info.get("temperature", 0.1)
    )

    embeddings = get_embeddings()

    sql_model = VLLMOpenAI(
        openai_api_key="EMPTY",
        openai_api_base=SQL_URL,
        model_name=SQL_MODEL,
    )

    # If there is a chat_history, then trim and condense it. 
    # Otherwise, output the question.
    # Effectively, {"chat_history" or "question"} -> text 
    condense_question_chain = RunnableBranch(
        (
            lambda x: bool(x.get("chat_history")),
            RunnablePassthrough.assign(
                chat_history=lambda x: trim_chat_history(x["chat_history"], 3)
            )
            | PromptTemplate.from_template(CONDENSE_QUESTION_TEMPLATE)
            | stringify
            | chat_model
            | StrOutputParser(),
        ),
        itemgetter("question"),
    )

    tool_picker_chain = (
        PromptTemplate.from_template(TOOL_PICKER_TEMPLATE)
        | stringify
        | chat_model
        | debug
        | RunnableLambda(lambda x: extract_json(x))
    )
    no_context_chain = (
        ChatPromptTemplate.from_template(NO_CONTEXT_TEMPLATE)
        | stringify
        | chat_model
        | debug
        | StrOutputParser()
    )
    chat_chain = (
        ChatPromptTemplate.from_template(CHAT_TEMPLATE)
        | stringify
        | chat_model
        | debug
        | StrOutputParser()
    )
    sql_chain = get_sql_chain(sql_model, chat_model) | itemgetter("answer")
    rag_chain = (
        get_rag_chain(chat_model, NUM_DOCS)
        | debug
        | itemgetter("answer")
    )

    print("Router: ", info)

    router = (
        RunnableAssign({"question": condense_question_chain})
        | RunnableAssign({"tool": tool_picker_chain})
        | RunnableBranch(
            ((lambda x: "greet" in x["tool"]), chat_chain),
            ((lambda x: x["ctx"] == False), no_context_chain),
            ((lambda x: "sql" in x["tool"]), sql_chain),
            ((lambda x: "search" in x["tool"]), rag_chain),
            itemgetter("question") | chat_chain
        )
    )
    
    return router


def get_avatar_chain() -> (
    RunnableSerializable[Dict[str, Union[str, List[Tuple[str, str]]]], str]
):
    """Get the router"""
    chain = {
        "question": lambda x: x["question"],
        "chat_history": lambda x: x["chat_history"],
        "temperature": lambda x: x["temperature"],
        "max_tokens": lambda x: x["max_tokens"],
        "ctx": lambda x: x["ctx"],
    } | RunnableLambda(route)
    return chain
