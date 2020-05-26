from util.JWTGenerator import JWTGenerator
import requests
import json
import jsonpath_rw_ext as jp

class Cycle_Resource:

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

    """Creates a cycle with given Cycle_name, project_Id and version_Id"""
    def create_cycle(self,cycle_name,project_Id,version_Id):

        end_point='cycle?expand=executionSummaries&clonedCycleId='
        canonical_path = 'POST&' + self.RELATIVE_PATH + 'cycle' + '&clonedCycleId=&expand=executionSummaries'
        token=self.jwt.generate_jwt(canonical_path)

        # REQUEST HEADER: to create cycle
        headers = {
            'Authorization': 'JWT ' + token,
            'Content-Type': 'application/json',
            'zapiAccessKey': self.access_key
        }

        # REQUEST PAYLOAD: to create cycle
        cycle = {
            'name': cycle_name,
            'projectId': project_Id,
            'versionId': version_Id
        }

        # MAKE REQUEST:
        print("Creating Cycle")
        raw_result = requests.post(self.ZAPI_CLOUD_URL + self.RELATIVE_PATH + end_point, headers=headers, json=cycle)
        if self.is_json(raw_result.text):
            # JSON RESPONSE: convert response to JSON
            json_result = json.loads(raw_result.text)

            # PRINT RESPONSE: pretty print with 4 indent
            #print(json.dumps(json_result, indent=4, sort_keys=True))

            #Get cycle ID
            cycle_id = jp.match1("id", json_result)
            print("Cycle created with ID: {}".format(cycle_id))
            return cycle_id

    """Returns the cycle_Id corresponding to cycle_name"""
    def get_cycle_with_name(self,version_Id,project_Id,cycle_name):
        end_point="cycles/search"
        canonical_path = 'GET&' + self.RELATIVE_PATH + end_point +'&expand=executionSummaries&projectId='+project_Id+'&versionId='+version_Id

        token = self.jwt.generate_jwt(canonical_path)

        # REQUEST HEADER: to create cycle
        headers = {
            'Authorization': 'JWT ' + token,
            'Content-Type': 'text/plain',
            'zapiAccessKey': self.access_key
        }

        print("Getting list of Cycles")
        raw_result = requests.get(self.ZAPI_CLOUD_URL + self.RELATIVE_PATH + end_point+'?versionId=' + version_Id
                                  +'&expand=executionSummaries'+ '&projectId=' + project_Id, headers=headers)

        if self.is_json(raw_result.text):
            # JSON RESPONSE: convert response to JSON
            json_result = json.loads(raw_result.text)

            # PRINT RESPONSE: pretty print with 4 indent
            # print(json.dumps(json_result, indent=4, sort_keys=True))

            #Get cycle id with name
            cycle_Id=jp.match1("$[?(name='"+ cycle_name +"')].id",json_result)
            print(cycle_Id)
            return cycle_Id