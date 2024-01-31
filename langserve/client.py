from typing import List

from langserve import RemoteRunnable
from langchain_core.messages import ChatMessage

remote_chain = RemoteRunnable("http://localhost:8000/agent/")

questions = [
    "Can LangSmith help test my LLM applications?"
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
