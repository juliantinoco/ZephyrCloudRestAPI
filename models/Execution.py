from util.JWTGenerator import JWTGenerator
import requests
import json
import jsonpath_rw_ext as jp

class Execution_Resource:

    ZAPI_CLOUD_URL = "https://prod-api.zephyr4jiracloud.com/connect"

    RELATIVE_PATH = '/public/rest/api/1.0/'

    def __init__(self, account_id, access_key,secret_key):
        self.account_id = account_id
        self.access_key = access_key
        self.secret_key= secret_key
        self.jwt=JWTGenerator(self.account_id,self.access_key,self.secret_key)

    def is_json(self,data):
        try:
            json.loads(data)
        except ValueError:
            return False
        return True

    """Add's the test items to the cycle"""
    def add_tests_to_cycle(self,issues,cycle_Id,project_Id,version_Id):

        end_point='executions/add/cycle/'
        canonical_path = 'POST&' + self.RELATIVE_PATH + end_point + cycle_Id + '&'

        token = self.jwt.generate_jwt(canonical_path)

        headers = {
            'Authorization': 'JWT ' + token,
            'Content-Type': 'application/json',
            'zapiAccessKey': self.access_key
        }

        # REQUEST PAYLOAD: to add test
        addTest = {
            'issues': issues,
            'method': '1',
            'projectId': int(project_Id),
            'versionId': int(version_Id)
        }

        # ADD test to Cycle
        print("Adding tests to the cycle")
        raw_result = requests.post(self.ZAPI_CLOUD_URL + self.RELATIVE_PATH + end_point + cycle_Id, headers=headers, json=addTest)
        # print(raw_result.text)
        assert raw_result.status_code == 200
        print("Tests {}  are added to cycle".format(issues))

    """Returns the list of Execution ID's for the cycle"""
    def get_list_of_execution_by_cycle(self,cycle_Id,project_Id,version_Id):

        end_point='executions/search/cycle/'
        canonical_path='GET&'+ self.RELATIVE_PATH + end_point + cycle_Id+'&projectId='+project_Id+'&versionId='+version_Id

        token = self.jwt.generate_jwt(canonical_path)

        headers = {
            'Authorization': 'JWT ' + token,
            'Content-Type': 'text/plain',
            'zapiAccessKey': self.access_key
        }

        # Get List of Executions By Cycle
        print("Getting list of execution ID's by Cycle")
        raw_result = requests.get(self.ZAPI_CLOUD_URL + self.RELATIVE_PATH + end_point  + cycle_Id + '?versionId=' + version_Id
                                  + '&projectId=' + project_Id, headers=headers)
        assert raw_result.status_code == 200
        if self.is_json(raw_result.text):

            # JSON RESPONSE: convert response to JSON
            json_result = json.loads(raw_result.text)

            # PRINT RESPONSE: pretty print with 4 indent
            # print(json.dumps(json_result, indent=4, sort_keys=True))
            # Getting Execution ID Lists
            execution_Ids = jp.match("$.searchObjectList[*].execution.id", json_result)
            print("Execution ID's are {}".format(execution_Ids))
            return execution_Ids

    """Updates the result for test exeution for the execution ID"""
    def update_execution(self,execution_Id,project_Id,version_Id,cycle_Id,issue_Id,status):

        end_point='execution/'
        canonical_path='PUT&'+ self.RELATIVE_PATH + end_point + execution_Id+'&'

        token = self.jwt.generate_jwt(canonical_path)

        headers = {
            'Authorization': 'JWT ' + token,
            'Content-Type': 'application/json',
            'zapiAccessKey': self.access_key
        }

        # REQUEST PAYLOAD: to update execution
        updateTest = {
            'status': {"id": status},
            'issueId': int(issue_Id),
            'projectId': int(project_Id),
            'versionId': int(version_Id),
            'cycleId':  cycle_Id
        }
        counter = 0
        status_flag = 0
        while(status_flag != 200 and counter < 3):
            raw_result = requests.put(self.ZAPI_CLOUD_URL + self.RELATIVE_PATH + end_point + execution_Id,
                                      headers=headers, json=updateTest)
            status_flag = raw_result.status_code
            counter = counter + 1

        #print(raw_result.text)
        if self.is_json(raw_result.text):

            # JSON RESPONSE: convert response to JSON
            json_result = json.loads(raw_result.text)
            status_code=jp.match1("$.execution.status.id",json_result)
            assert status_code == status
            print("Test run updated successfully for issue id {}".format(issue_Id))
            # PRINT RESPONSE: pretty print with 4 indent
            # print(json.dumps(json_result, indent=4, sort_keys=True))

    """Creates an execution for an particular issue_ID"""
    def create_execution(self,project_Id,version_Id,cycle_Id,issue_Id,status):
        end_point='execution'
        canonical_path = 'POST&' + self.RELATIVE_PATH + end_point  + '&'

        token = self.jwt.generate_jwt(canonical_path)

        headers = {
            'Authorization': 'JWT ' + token,
            'Content-Type': 'application/json',
            'zapiAccessKey': self.access_key
        }

        # REQUEST PAYLOAD: to Create Execution
        createExecution = {
            'status': {"id": status},
            'issueId': int(issue_Id),
            'projectId': int(project_Id),
            'versionId': int(version_Id),
            'cycleId': cycle_Id
        }
        print("Creating Execution")
        raw_result = requests.post(self.ZAPI_CLOUD_URL + self.RELATIVE_PATH + end_point,
                                      headers=headers, json=createExecution)

        if(self.is_json(raw_result.text)):
            json_result = json.loads(raw_result.text)

            print(json.dumps(json_result, indent=4, sort_keys=True))