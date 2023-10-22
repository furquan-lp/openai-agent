import os
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationSummaryBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from bs4 import BeautifulSoup

import requests
import json
import streamlit as sl
from langchain.schema import SystemMessage

load_dotenv()
browserless_api_key = os.getenv('AGENT_BROWSERLESS_API')
serper_api_key = os.getenv('AGENT_SERP_API')

def google_search(query):
    url = 'https://google.serper.dev/search'

    payload = json.dumps({
        'q': query
    })

    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request('POST', url, headers=headers, data=payload)

    print(response.text)
    return response.text

google_search('What is the speed of light?')