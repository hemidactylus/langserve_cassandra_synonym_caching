import os

import cassio

import langchain
from langchain.schema import BaseMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnableLambda
from langchain.cache import CassandraCache

cassio.init(
    token=os.environ["ASTRA_DB_APPLICATION_TOKEN"],
    database_id=os.environ["ASTRA_DB_ID"],
    keyspace=os.environ.get("ASTRA_DB_KEYSPACE"),
)

# inits
langchain.llm_cache = CassandraCache(session=None, keyspace=None)
llm = ChatOpenAI()

# custom runnables
def msg_splitter(msg: BaseMessage):
    return [
        w.strip()
        for w in msg.content.split(",")
        if w.strip()
    ]

# synonym-route preparation
synonym_prompt = ChatPromptTemplate.from_template(
    "List up to five comma-separated synonyms of this word: {word}"
)

chain = synonym_prompt | llm | RunnableLambda(msg_splitter)