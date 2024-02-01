#!/usr/bin/env python
# from typing import List

import argparse
import os

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
# Document loaders
from langchain_community.document_loaders import AmazonTextractPDFLoader
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_loaders import WebBaseLoader

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
    print(f"Loading retriever: {tool_type}")
    directory = os.path.dirname(os.path.realpath(__file__))
    if tool_type == 'pdf':
        print(f"    loading PDF retriever")
        loader = AmazonTextractPDFLoader(f"{directory}/assets/pdf/event.pdf") # PDF
    elif tool_type == 'image':
        print(f"    loading image retriever")
        loader = AmazonTextractPDFLoader(f"{directory}/assets/image/yoga.jpg") # image
    elif tool_type == 'web':
        print(f"    loading web retriever")
        loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
    elif tool_type == 'html':
        print(f"    loading HTML retriever")
        urls = [
            "https://medium.com/@alexandre.j_37811/phishing-attacks-part-1-b1ecef36a2e5",
            "https://medium.com/edureka/what-is-ddos-attack-9b73bd7b9ba1"
        ]
        loader = AsyncHtmlLoader(urls)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    vector = FAISS.from_documents(documents, embeddings)
    retriever = vector.as_retriever()
    return retriever

def create_tools(tool_types):
    tools = []
    # Different retrievers
    print(f"Loading custom tool type: {tool_types}")
    for tool_type in tool_types:
        retriever = load_retriever(tool_type)
        if tool_type == 'pdf':
            print("    loading PDF tool")
            retriever_tool = create_retriever_tool(
                retriever,
                "PDF_retriever_tool",
                "Search for information about the 2024 Chinese New Year event. For any questions about 2024 Chinese New Year event, you must use this tool!",
            )
            tools.append(retriever_tool)
        elif tool_type == 'image':
            print("    loading image tool")
            retriever_tool = create_retriever_tool(
                retriever,
                "Image_retriever_tool",
                "Search for information about Free Yoga event. For any questions about Free Yoga event, you must use this tool!",
            )
            tools.append(retriever_tool)
        elif tool_type == 'web':
            print("    loading web tool")
            retriever_tool = create_retriever_tool(
                retriever,
                "Web_retriever_tool",
                "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
            )
            tools.append(retriever_tool)
        elif tool_type == 'html':
            print("    loading html tool")
            retriever_tool = create_retriever_tool(
                retriever,
                "Html_retriever_tool",
                "Search for information about DDoS and Phishing Attack. For any questions about DDoS and Phishing Attack, you must use this tool!",
            )
            tools.append(retriever_tool)
    # Add search retriever tool at the end
    search = TavilySearchResults()
    tools.append(search)
    for tool in tools:
        print(f"Finished loading tools: {tool.name}")
    return tools

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=__file__)
    parser.add_argument(
        '--source',
        type=str.lower,
        action='append',
        help='Choose the source of content, supported options: {image, PDF}.'
    )
    args = parser.parse_args()
    print(f"Input args: {args}")

    # Load Retriever and Create Tools
    tools = create_tools(tool_types=args.source)

    # Create Agent
    prompt = hub.pull("hwchase17/openai-functions-agent")
    llm = ChatOpenAI(model="gpt-4", temperature=0)
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