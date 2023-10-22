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
        separators=['\n\n', '\n'], chunk_size=8000, chunk_overlap=500)

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


def research(query):
    llm_config_researcher = {
        'functions': [
            {
                'name': 'search',
                'description': 'Google search for relevant information',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'query': {
                            'type': 'string',
                            'description': 'Google search for query',
                        }
                    },
                    'required': ['query'],
                },
            },
            {
                'name': 'scrape_website',
                'description': 'Scraping website content based on URL',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'url': {
                            'type': 'string',
                            'description': 'Scrapes website URL',
                        }
                    },
                    'required': ['url'],
                },
            },
        ],
        'config_list': config_list}

    researcher = autogen.AssistantAgent(
        name='researcher',
        system_message='Research about a given query, collect as many information as possible, and generate detailed research results with loads of technique details with all reference links attached; Add TERMINATE to the end of the research report;',
        llm_config=llm_config_researcher,
    )
    user_proxy = autogen.UserProxyAgent(
        name='User_proxy',
        code_execution_config={'last_n_messages': 2, 'work_dir': 'coding'},
        is_termination_msg=lambda x: x.get('content', '') and x.get(
            'content', '').rstrip().endswith('TERMINATE'),
        human_input_mode='TERMINATE',
        function_map={
            'search': search,
            'scrape': scrape_website,
        }
    )

    user_proxy.initiate_chat(researcher, message=query)
    user_proxy.stop_reply_at_receive(researcher)
    user_proxy.send(
        'Give me the research report that just generated again, return ONLY the report & reference links', researcher)

    return user_proxy.last_message()['content']


result = research('What is Microsoft autogen?')
print("RES:", result)
