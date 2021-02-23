from utils.JWTGenerator import JWTGenerator
from utils import tools

import json
import requests
import jsonpath_rw_ext as jp
import config


class ExecutionResource:

    ZAPI_CLOUD_URL = config.ZAPI_CLOUD_URL
    RELATIVE_PATH = config.RELATIVE_PATH

    def __init__(self, account_id, access_key,secret_key):
        self.account_id = account_id
        self.access_key = access_key
        self.secret_key = secret_key
        self.jwt = JWTGenerator(self.account_id,self.access_key,self.secret_key)

    """Add's the test items to the cycle"""
    def add_tests_to_cycle(self, issues, cycle_id, project_id, version_id):

        end_point = 'executions/add/cycle/'
        canonical_path = F'POST&{self.RELATIVE_PATH}{end_point}{cycle_id}&'

        token = self.jwt.generate_jwt(canonical_path)

        headers = {
            'Authorization': f'JWT {token}',
            'Content-Type': 'application/json',
            'zapiAccessKey': self.access_key
        }

        # REQUEST PAYLOAD: to add test
        add_test = {
            'issues': issues,
            'method': '1',
            'projectId': int(project_id),
            'versionId': int(version_id)
        }

        # ADD test to Cycle
        print("Adding tests to the cycle")
        raw_result = requests.post(self.ZAPI_CLOUD_URL + self.RELATIVE_PATH + end_point + cycle_id,
                                   headers=headers, json=add_test)

        if tools.get_json_results(raw_result):
            print(f"Tests {issues} are added to cycle")
        else:
            raise Exception(f"An error was detected. Details in: {raw_result}")

        return raw_result.text

    """Returns the list of Execution ID's for the cycle"""
    def get_list_of_execution_by_cycle(self, cycle_id, project_id, version_id):

        end_point = 'executions/search/cycle/'
        canonical_path = f"GET&{self.RELATIVE_PATH}{end_point}{cycle_id}&projectId={project_id}&versionId={version_id}"

        token = self.jwt.generate_jwt(canonical_path)

        headers = {
            'Authorization': f'JWT {token}',
            'Content-Type': 'text/plain',
            'zapiAccessKey': self.access_key
        }

        # Get List of Executions By Cycle
        print("Getting list of execution ID's by Cycle")
        raw_result = requests.get(self.ZAPI_CLOUD_URL + self.RELATIVE_PATH + end_point + cycle_id + '?versionId=' + version_id
                                  + '&projectId=' + project_id, headers=headers)
        assert raw_result.status_code == 200

        if tools.is_json(raw_result.text):

            # JSON RESPONSE: convert response to JSON
            json_result = json.loads(raw_result.text)

            # PRINT RESPONSE: pretty print with 4 indent
            # print(json.dumps(json_result, indent=4, sort_keys=True))
            # Getting Execution ID Lists
            execution_ids = jp.match("$.searchObjectList[*].execution.id", json_result)
            print(f"Execution ID's are {execution_ids}")
            return execution_ids

    """Updates the result for test exeution for the execution ID"""
    def update_execution(self, execution_id, project_id, version_id, cycle_id, issue_id, status):

        end_point = 'execution/'
        canonical_path = f"PUT&{self.RELATIVE_PATH}{end_point}{execution_id}&"

        token = self.jwt.generate_jwt(canonical_path)

        headers = {
            'Authorization': f'JWT {token}',
            'Content-Type': 'application/json',
            'zapiAccessKey': self.access_key
        }

        # REQUEST PAYLOAD: to update execution
        update_test = {
            'status': {"id": status},
            'issueId': int(issue_id),
            'projectId': int(project_id),
            'versionId': int(version_id),
            'cycleId':  cycle_id
        }
        counter = 0
        status_flag = 0
        raw_result = None

        while status_flag != 200 and counter < 3:
            raw_result = requests.put(self.ZAPI_CLOUD_URL + self.RELATIVE_PATH + end_point + execution_id,
                                      headers=headers, json=update_test)
            status_flag = raw_result.status_code
            counter = counter + 1

        # print(raw_result.text)
        if raw_result:
            if tools.is_json(raw_result.text):

                # JSON RESPONSE: convert response to JSON
                json_result = json.loads(raw_result.text)
                status_code = jp.match1("$.execution.status.id", json_result)
                assert status_code == status
                print("Test run updated successfully for issue id {}".format(issue_id))
                # PRINT RESPONSE: pretty print with 4 indent
                # print(json.dumps(json_result, indent=4, sort_keys=True))
        else:
            print("The request didn't run")

    """Creates an execution for an particular issue_ID"""
    def create_execution(self, issue_id, project_id, version_id, cycle_id, status=tools.Status.PASS.value):
        end_point = 'execution'
        canonical_path = f"POST&{self.RELATIVE_PATH}{end_point}&"

        token = self.jwt.generate_jwt(canonical_path)

        headers = {
            'Authorization': f'JWT {token}',
            'Content-Type': 'application/json',
            'zapiAccessKey': self.access_key
        }

        # REQUEST PAYLOAD: to Create Execution
        create_execution = {
            'status': {"id": status},
            'issueId': issue_id,
            'projectId': int(project_id),
            'versionId': int(version_id),
            'cycleId': cycle_id
        }
        print("Creating Execution")
        raw_result = requests.post(self.ZAPI_CLOUD_URL + self.RELATIVE_PATH + end_point, headers=headers,
                                   json=create_execution)

        if tools.is_json(raw_result.text):
            json_result = json.loads(raw_result.text)

            print(json.dumps(json_result, indent=4, sort_keys=True))

            return raw_result.json()

    def get_steps_results(self, execution_id, issue_id):
        """
        This function return all StepsResults associated to a execution_id and issue_id
        """
        print("Getting StepsResults")
        end_point = "stepresult/search"
        canonical_path = f"GET&{self.RELATIVE_PATH}{end_point}&executionId={execution_id}&issueId={issue_id}"
        token = self.jwt.generate_jwt(canonical_path)

        headers = {
            'Authorization': f"JWT {token}",
            'content-Type': None,
            'zapiAccessKey': self.access_key
        }

        # Get stepsResults
        raw_result = requests.get(f"{self.ZAPI_CLOUD_URL}{self.RELATIVE_PATH}{end_point}",
                                  params={
                                      "executionId": execution_id,
                                      "issueId": int(issue_id),
                                  },
                                  headers=headers)

        return raw_result.json()

    def update_step_result(self, execution_id, issue_id, step_id, step_result_id, status):
        print("Updating StepsResults")
        # UPDATE STATUS FOR EACH STEP
        end_point = "stepresult/"
        canonical_path = f"PUT&{self.RELATIVE_PATH}{end_point}{step_result_id}&"
        token = self.jwt.generate_jwt(canonical_path)

        headers = {
            'Authorization': f"JWT {token}",
            'content-Type': 'application/json',
            'zapiAccessKey': self.access_key
        }

        raw_result = requests.put(f"{self.ZAPI_CLOUD_URL}{self.RELATIVE_PATH}{end_point}{step_result_id}",
                                  json={
                                      'status': {'id': status},
                                      'issueId': int(issue_id),
                                      'stepId': step_id,
                                      'executionId': execution_id,
                                  },
                                  headers=headers)

        return raw_result.text
