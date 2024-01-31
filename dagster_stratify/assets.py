from dagster import asset, PermissiveConfig, get_dagster_logger
from typing import Any
import json
import requests
from subprocess import Popen, PIPE

class MyPermissiveConfig(PermissiveConfig):
    name: Any

@asset
def config_validation(config: MyPermissiveConfig):
    my_logger = get_dagster_logger()

    port_forward_command = "kubectl port-forward insights-794659f7c-2hvpk -n strat 8000:8000"
    command_list = port_forward_command.split(" ")
    process = Popen(command_list, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    my_logger.info(stdout)
    my_logger.info(stderr)

    api_url = "http://localhost:8000/config_validate"

    config_json = {}
    for key, val in config:
        config_json[key] = val
    config_str = json.dumps(config_json)

    headers =  {"accept":"application/json"}
    response = requests.post(api_url, data=config_str, headers=headers)

    if response.json()['valid']:
        my_logger.info("Configuration is valid")
    else:
        my_logger.error("Configuration is not valid")

@asset
def computations(config: MyPermissiveConfig):
    my_logger = get_dagster_logger()

    api_url = "http://localhost:8000/run_job/stratify"

    config_json = {}
    for key, val in config:
        config_json[key] = val
    config_str = json.dumps(config_json)

    headers =  {"accept":"application/json"}
    response = requests.post(api_url, data=config_str, headers=headers)

    my_logger.info(f"Job {response.json()['job_id']} is running")