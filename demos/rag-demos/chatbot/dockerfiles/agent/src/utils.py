import re
from typing import List, Tuple, Any

import sqlglot

from langchain.schema import AIMessage, HumanMessage
from langchain_community.utilities import SQLDatabase


db = SQLDatabase.from_uri("sqlite:///cmd.db", sample_rows_in_table_info=0)


def debug(x: Any) -> Any:
    """Print the given object and return it unchanged.

    Parameters:
    - x (Any): The object to print.

    Returns:
    - Any: The input object.
    """
    print(x)
    return x


def stringify(x: Any) -> str:
    """Convert the given object to a string.

    Parameters:
    - x (Any): The object to convert to a string.

    Returns:
    - str: The string representation of the object.
    """
    return x.to_string()


def get_schema(_) -> str:
    """Return table schema for sqlite database"""
    return db.get_table_info()


def run_sql(query: str, dialect: str) -> str:
    """Transpile and execute an SQL query using the specified dialect.

    Parameters:
    - query (str): The SQL query to be transpiled and executed.
    - dialect (str): The target SQL dialect for transpilation and execution.

    Returns:
    - str: The result of executing the transpiled SQL query.

    Example:
    ```
    result = run_sql("SELECT * FROM my_table", "sqlite")
    print(result)
    ```
    """
    query = sqlglot.transpile(query, read="postgres", write=dialect)[0]
    print(query)
    return db.run(query)


def trim_chat_history(
    chat_history: List[Tuple[str, str]],
    keep_messages: int
) -> List:
    """Trim the given chat history to retain only the last `keep_messages`
    interactions.

    Parameters:
    - chat_history (List[Tuple[str, str]]): A list of tuples representing the 
      conversation history. Each tuple contains a human message and its 
      corresponding AI response.
    - keep_messages (int): The number of message pairs to retain from the end 
      of the chat history.

    Returns:
    - List: A list containing the trimmed chat history with only the last
      `keep_messages` interactions.Each interaction is represented as a tuple 
      containing a HumanMessage and an AIMessage.
    """
    if not chat_history:
        return chat_history

    buffer = []
    for human, ai in chat_history[-keep_messages:]:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))

    return buffer


def extract_json(content: str) -> str:
    """Extract the first valid JSON object found within the given content.

    Parameters:
    - content (str): The string containing JSON objects.

    Returns:
    - str: The first valid JSON object found in the content, or an empty string
      if none is found.

    Example:
    ```python
    content = '{"name": "John", "age": 25} Some text {"city": "New York"}'
    result = extract_json(content)
    print(result)  # Output: '{"name": "John", "age": 25}'
    ```
    
    Note:
    The function uses a regular expression to find the first occurrence of a
    valid JSON object in the content. If no valid JSON object is found, an
    empty string is returned.
    """
    pattern = re.compile(r"\{(?:[^{}]|)*\}", re.MULTILINE)
    matches = pattern.findall(content)
    match = "{}" if not matches else matches[0]
    return match
