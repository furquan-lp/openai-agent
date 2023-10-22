from autogen import config_list_from_json
import autogen

config_list = config_list_from_json(env_or_file='OAI_CONFIG_LIST')
llm_config = {'config_list': config_list, 'seed': 42, 'request_timeout': 120}

user_proxy = autogen.UserProxyAgent(
    name='User_proxy',
    system_message='A human admin who will give the idea and run the code provided by Coder.',
    code_execution_config={'last_n_messages': 2, 'work_dir': 'groupchat'},
    human_input_mode='ALWAYS',
)
coder = autogen.AssistantAgent(
    name='Coder',
    llm_config=llm_config,
)
pm = autogen.AssistantAgent(
    name='product_manager',
    system_message='You will help break down the initial idea into a well scoped requirement for the coder; Do not involve in future conversations or error fixing',
    llm_config=llm_config,
)
