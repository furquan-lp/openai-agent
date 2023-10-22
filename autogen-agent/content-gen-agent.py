import os
from autogen import config_list_from_json
import autogen

import requests
from bs4 import BeautifulSoup
import json

from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain import PromptTemplate
import openai
from dotenv import load_dotenv

load_dotenv()
config_list = config_list_from_json(env_or_file='OAI_CONFIG_LIST')
openai.api_key = os.getenv('OPENAI_API_KEY')


# research function
def search(query):
    url = 'https://google.serper.dev/search'

    payload = json.dumps({
        'q': query
    })
    headers = {
        'X-API-KEY': '584babe795cdececcc761e68443bb663a8a3dad7',
        'Content-Type': 'application/json'
    }

    response = requests.request('`POST', url, headers=headers, data=payload)
    return response.json()
