from typing import List

from langserve import RemoteRunnable
from langchain_core.messages import ChatMessage

remote_chain = RemoteRunnable("http://localhost:8000/agent/")

questions = [
    "Can LangSmith help test my LLM applications?", # Web search from specific webpage
    "What's the weather like today in San Francisco?", # Web search from Tavily
    "When is the New Year celebration, where it is?", # PDF demo
    "Who is the organizer of free yoga?", # Image demo
]
chat_history = []

for question in questions:
    print(f"Question: {question}")
    response = remote_chain.invoke({
        "input": question,
        "chat_history": chat_history
    })
    answer = response['output']
    print(f"Answer: {answer}")
    # Record chat history
    chat_history.append(ChatMessage(content=question, type='chat', role='user'))
    chat_history.append(ChatMessage(content=answer, type='chat', role='assistant'))
    print('================================================\n')
