from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# OpenAI key is here
config_list = config_list_from_json(env_or_file='OAI_CONFIG_LIST')

assistant = AssistantAgent(name='assistant', llm_config={
                           'config_list': config_list})

user_proxy = UserProxyAgent(
    name='user_proxy',
    code_execution_config={'work_dir': 'coding'})

user_proxy.initiate_chat(
    assistant, message='Plot a chart of BYD and TSLA stock price change YTD.')