SQL_SUM_SYS_MSG = """
Given an input question and SQL response, convert it to a natural language
answer. Give a human-like response.
"""

SQL_SUM_TEMPLATE = """
Based on the table schema below, question, sql query, and sql response, write a
natural language response. Do not explain the SQL response or the SQL query,
just provide a human like response.
{schema}

Question: {question}
SQL Query: {sqlquery}
SQL Response: {response}"""


SQL_GEN_TEMPLATE = """
### Task
Generate a SQLite query to answer, with the following requirements:
- use the LIMIT clause to limit the output to 5 results at most
- Always use ILIKE on TEXT columns.
- TEXT columns with CHECK constraints should be treated like ENUMs.
- Group results by the session title column.
[QUESTION]{question}[/QUESTION]

### Instructions
- Always provide all the columns, If you cannot answer the question with the
available database schema, return 'I do not know.'

### Database Schema
The query will run on a database with the following schema:
{schema}

### Answer
Given the database schema,
here is the SQLite query that answers [QUESTION]{question}[/QUESTION]:
[SQL]
"""

RAG_TEMPLATE = """Answer the question based only on the following context:
{context}

Question: {question}
"""

RAG_TEMPLATE = """Answer the question based only on the following context:
{context}

Question: {question}
"""

CHAT_TEMPLATE = """Answer the question as if you are a respectful customer
service representative.

Question: {question}
"""

NO_CONTEXT_TEMPLATE = """Answer the user question but if you don't know the
answer, apologize, indicate you aren't sure, and you need more information.
Don't try to make up an answer.

Example-1:

Question: Get me the instance type of the compute instances with more than 1 GPUs.
Answer: I'm sorry, I don't have that information. Could you provide more context?

Example-2:

Question: Get me the instance type of the servers with more than 1 GPUs.
Answer: I'm sorry, I don't have that information. Could you provide more context?

Question: {question}
"""

CONDENSE_QUESTION_TEMPLATE = """Given the following conversation and a follow
up question, rephrase the follow up question to be a standalone question,
in its original language.
Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""


TOOL_PICKER_TEMPLATE = """You are a helpful AI assistant, you have access to
the following tools:

- greet: Responds to greetings from the user
- sql: Searches the SQL database to provide information about HPE products
- search: Searches for HPE product documentation

Using only these tools and always respond in valid JSON format containing the
key "tool_name".
Below are few examples:

Example-1

Question: Hey, how are you?
Answer:{{"tool_name": "greet"}}

Example-2

Question: Get me the instance type of the compute instances with more than 1 GPUs.
Answer:{{"tool_name": "sql"}}

Example-3

Question: Sorry, I forgot to provide context... Get me the instance type of the compute instances with more than 1 GPUs.
Answer:{{"tool_name": "sql"}}

Example-4

Question: What is the base model for the instance type Z4i.z4md?
Answer:{{"tool_name": "sql"}}

Example-5

Question: What type of CPU does the HPE DL380a Gen11 server have, in the Z4i.z4md configuration?
Answer:{{"tool_name": "search"}}

Example-6

Question: What is the HPE DL380a Gen11 4DW CTO Svr server good for?
Answer:{{"tool_name": "search"}}

Example-7

Question: How much does the HPE DL380a Gen11 4DW CTO Svr server cost?
Answer:{{"tool_name": "sql"}}

Let's get started. Always answer the question in valud JSON format and nothing
else, no details, no other words. Just valid JSON.
So, your answer should either be {{"tool_name": "search"}},
{{"tool_name": "sql"}} or {{"tool_name": "greet"}}.
Pay attention to the examples to understand when to use
{{"tool_name": "search"}}, {{"tool_name": "sql"}} or {{"tool_name": "greet"}}.

Question: {question}
Answer:
"""

DB_MISSING_PROMPT = """
Nothing relevant was found in the database. Please apologize and indicate you
aren't sure.
"""
