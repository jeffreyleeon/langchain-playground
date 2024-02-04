from typing import List

from langserve import RemoteRunnable
from langchain_core.messages import ChatMessage

remote_chain = RemoteRunnable("http://0.0.0.0:8000/agent/")

questions = [
    "Can LangSmith help test my LLM applications?", # Web search from specific webpage
    "When is superbowl in 2024?", # Web search from Tavily
    "What is HTTP Client Error 404?", # PDF demo
    "What are some HTTP security concerns?", # PDF demo
    "Who is the organizer of free yoga?", # Image demo
    "What is a mailbomb DDoS attack?", # HTML demo
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
