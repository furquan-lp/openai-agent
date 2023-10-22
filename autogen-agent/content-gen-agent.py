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
from langchain.prompts import PromptTemplate
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
    post_url = 'https://chrome.browserless.io/content?token=ce347263-8e76-442e-93b3-db28a0570fcc'
    response = requests.post(post_url, headers=headers, data=data_json)

    if response.status_code == 200:
        # Extracts the text from the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        print('SCRAPED CONTENT:', text)

        if len(text) > 8000:
            output = summary(objective, text)
            return output
        else:
            return text
    else:
        print(f'HTTP request failed with status code {response.status_code}')


def summary(objective, content):
    llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo-16k-0613')

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=8000, chunk_overlap=500)

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
