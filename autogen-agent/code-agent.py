from autogen import config_list_from_json
import autogen

config_list = config_list_from_json(env_or_file='OAI_CONFIG_LIST')
llm_config = {'config_list': config_list, 'seed': 42, 'request_timeout': 120}
