#!/usr/bin/env python
# from typing import List

import argparse
import os

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import AmazonTextractPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.messages import ChatMessage
from langserve import add_routes
import uvicorn

# We need to add these input/output schemas because the current AgentExecutor
# is lacking in schemas.

class Input(BaseModel):
    input: str
    chat_history: list[ChatMessage]


class Output(BaseModel):
    output: str

def load_retriever(tool_type):
    directory = os.path.dirname(os.path.realpath(__file__))
    match tool_type:
        case 'pdf':
            loader = AmazonTextractPDFLoader(f"{directory}/assets/pdf/event.pdf") # PDF
        case 'image':
            loader = AmazonTextractPDFLoader(f"{directory}/assets/image/yoga.jpg") # image
        case default:
            loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    vector = FAISS.from_documents(documents, embeddings)
    retriever = vector.as_retriever()
    return retriever

def create_tools(tool_type):
    tools = []
    # Different retrievers
    print(f"Loading custom tool type: {tool_type}")
    retriever = load_retriever(tool_type)
    if tool_type == 'pdf':
        retriever_tool = create_retriever_tool(
            retriever,
            "new_year_event",
            "Search for information about New Year event. For any questions about New Year event, you must use this tool!",
        )
        tools.append(retriever_tool)
    elif tool_type == 'image':
        retriever_tool = create_retriever_tool(
            retriever,
            "free_yoga_event",
            "Search for information about Free Yoga event. For any questions about Free Yoga event, you must use this tool!",
        )
        tools.append(retriever_tool)

    # Add search retriever tool at the end
    search = TavilySearchResults()
    tools.append(search)
    return tools

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=__file__)
    parser.add_argument(
        '--source',
        choices=['default', 'pdf', 'image'],
        default='default',
        type=str.lower,
        help='Choose the source of content, could be from website, image, PDF, etc.'
    )
    args = parser.parse_args()
    print(f"Input args: {args}")

    # Load Retriever and Create Tools
    tools = create_tools(tool_type=args.source)

    # Create Agent
    prompt = hub.pull("hwchase17/openai-functions-agent")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # App definition
    app = FastAPI(
        title="LangChain Server",
        version="1.0",
        description="A simple API server using LangChain's Runnable interfaces",
    )
    add_routes(
        app,
        agent_executor.with_types(input_type=Input, output_type=Output),
        path="/agent",
    )

    # Start server
    print("Starting server...")
    uvicorn.run(app, host="localhost", port=8000)