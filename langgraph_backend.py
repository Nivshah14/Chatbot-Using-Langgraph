from langgraph.graph import StateGraph,START,END
from typing import Annotated,TypedDict,Literal
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.runnables import RunnableConfig
from dotenv import load_dotenv
import sqlite3
load_dotenv()

from langgraph.graph.message import add_messages

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]
    
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def chat_node(state:ChatState):
    messages=state['messages']
    response=llm.invoke(messages)
    
    return {'messages':[response]}

conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)

checkpointer=SqliteSaver(conn=conn)

graph = StateGraph(ChatState)

# add nodes
graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)    



