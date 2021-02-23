from utils.JWTGenerator import JWTGenerator
from utils import tools

import requests
import json
import jsonpath_rw_ext as jp
import config


class CycleResource:

    ZAPI_CLOUD_URL = config.ZAPI_CLOUD_URL
    RELATIVE_PATH = config.RELATIVE_PATH

    def __init__(self, account_id, access_key,secret_key):
        self.account_id = account_id
        self.access_key = access_key
        self.secret_key = secret_key
        self.jwt = JWTGenerator(self.account_id, self.access_key, self.secret_key)

    """Creates a cycle with given Cycle_name, project_Id and version_Id"""
    def create_cycle(self, cycle_name, project_id, version_id):

        end_point = 'cycle?expand=executionSummaries&clonedCycleId='
        canonical_path = 'POST&' + self.RELATIVE_PATH + 'cycle' + '&clonedCycleId=&expand=executionSummaries'
        token = self.jwt.generate_jwt(canonical_path)

        # REQUEST HEADER: to create cycle
        headers = {
            'Authorization': f"JWT {token}",
            'Content-Type': 'application/json',
            'zapiAccessKey': self.access_key
        }

        # REQUEST PAYLOAD: to create cycle
        cycle = {
            'name': cycle_name,
            'projectId': project_id,
            'versionId': version_id
        }

        # MAKE REQUEST:
        print("Creating Cycle")
        raw_result = requests.post(self.ZAPI_CLOUD_URL + self.RELATIVE_PATH + end_point, headers=headers, json=cycle)
        json_result = tools.get_json_results(raw_result)

        if json_result:
            cycle_id = jp.match1("id", json_result)
            print(f"Cycle created with ID: {cycle_id}")
            return cycle_id
        else:
            raise Exception(f"An error was detected. Details in: {raw_result}")

    """Returns the cycle_Id corresponding to cycle_name"""
    def get_cycle_with_name(self, version_id, project_id, cycle_name):
        end_point = "cycles/search"
        canonical_path = f"GET&{self.RELATIVE_PATH}{end_point}&expand=executionSummaries&projectId={project_id}" \
                         f"&versionId={version_id}"

        token = self.jwt.generate_jwt(canonical_path)

        # REQUEST HEADER: to create cycle
        headers = {
            'Authorization': f"JWT {token}",
            'Content-Type': 'text/plain',
            'zapiAccessKey': self.access_key
        }

        print("Getting list of Cycles")
        raw_result = requests.get(f"{self.ZAPI_CLOUD_URL}{self.RELATIVE_PATH}{end_point}?versionId={version_id}"
                                  f"&expand=executionSummaries&projectId={project_id}", headers=headers)

        json_result = tools.get_json_results(raw_result)

        if json_result:
            cycle_id = jp.match1("$[?(name='" + cycle_name + "')].id", json_result)
            print(cycle_id)
            return cycle_id
        else:
            raise Exception(f"An error was detected. Details in: {raw_result}")
