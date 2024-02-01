from langchain_community.tools import ElevenLabsText2SpeechTool

text_to_speak = "Ideas are shit. Execution is the king."

tts = ElevenLabsText2SpeechTool()
print(tts.name)

# speech_file = tts.run(text_to_speak)
# tts.play(speech_file)

tts.stream_speech(text_to_speak)

'''
# Using an agent

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain_openai import OpenAI

llm = OpenAI(temperature=0)
tools = load_tools(["eleven_labs_text2speech"])
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
audio_file = agent.run("Tell me a joke and read it out for me.")
tts.play(audio_file)

'''