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

# Search Google through Serper and return the results
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

# Scrape the website URL and summarize content based on the given objective
def scrape_website(objective: str, url: str):
    print('Scraping...')

    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json'
    }

    data = {
        'url': url
    }

    data_json = json.dumps(data)
    # Send the request to Browserless
    post_url = f'https://chrome.browserless.io/content?token={browserless_api_key}'
    response = requests.post(post_url, headers=headers, data=data_json)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser') # Extracts the text from the HTML
        text = soup.get_text()
        print('SCRAPED CONTENT:', text)

        if len(text) > 10000:
            output = summary(objective, text)
            return output
        else:
            return text
    else:
        print(f'HTTP request failed with status code {response.status_code}')

def summary(objective, content):
    llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo-16k-0613')

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=10000, chunk_overlap=500)

    docs = text_splitter.create_documents([content])
    map_prompt = """
    Write a summary of the following text for {objective}:
    "{text}"
    SUMMARY:
    """
    map_prompt_template = PromptTemplate(
        template=map_prompt, input_variables=['text', 'objective'])
    
    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type='map_reduce',
        map_prompt=map_prompt_template,
        combine_prompt=map_prompt_template,
        verbose=True
    )

    output = summary_chain.run(input_documents=docs, objective=objective)
    return output

class ScrapeWebsiteInput(BaseModel):
    """Inputs for scrape_website function"""
    objective: str = Field(description="The objective & task that users give to the agent")
    url: str = Field(description="The url of the website to be scraped")

class ScrapeWebsiteTool(BaseTool):
    name = "scrape_website"
    description = "When data is needed from a website URL, passing both the URL and the objective for the prompt to the function."
    args_schema: Type[BaseModel] = ScrapeWebsiteInput

    def _run(self, objective: str, url: str):
        return scrape_website(objective, url)
    
    def _arun(self, url: str):
        raise NotImplementedError("Functionality not implemented yet")

tools = [
    Tool(
        name="Search",
        func=search,
        description="Useful for when you need to answer questions about current events, data. You should ask targeted questions."
    ),
    ScrapeWebsiteTool()
]