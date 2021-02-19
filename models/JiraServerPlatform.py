from utils import tools

import requests
import json
import jsonpath_rw_ext as jp


class JiraResources:

    def __init__(self, url, user, token):
        self.url = url
        self.user = user
        self.token = token

    """Returns the project_Id corresponding to project_name"""
    def get_project_id_with_name(self, project_name):

        end_point = "rest/api/2/project"
        response = requests.get(self.url + end_point, auth=(self.user, self.token))
        assert response.status_code == 200

        if tools.is_json(response.text):
            # JSON RESPONSE: convert response to JSON
            json_result = json.loads(response.text)

            # PRINT RESPONSE: pretty print with 4 indent
            # print(json.dumps(json_result, indent=4, sort_keys=True))

            project_id = jp.match1("$[?(name='"+project_name+"')].id", json_result)
            print(f"Project ID {project_id} with Name {project_name}")
            return project_id

    """Returns the version_Id corresponding to version name in an project"""
    def get_version_id_with_name(self, version_name, project_id):

        end_point = f"rest/api/2/project/{project_id}/version"
        response = requests.get(self.url + end_point, auth=(self.user, self.token))
        assert response.status_code == 200

        if tools.is_json(response.text):
            # JSON RESPONSE: convert response to JSON
            json_result = json.loads(response.text)

            # PRINT RESPONSE: pretty print with 4 indent
            # print(json.dumps(json_result, indent=4, sort_keys=True))

            version_id = jp.match1("$.values[?(name='" + version_name + "')].id", json_result)
            print(f"Version ID {version_id} with Name {version_name}")
            return version_id

    """Returns the issue for corresponding issue_Key"""
    def get_issue_id_with_key(self, key):
        end_point = '/rest/api/2/search'
        response = requests.get(self.url + end_point, auth=(self.user, self.token))
        assert response.status_code == 200

        if tools.is_json(response.text):
            # JSON RESPONSE: convert response to JSON
            json_result = json.loads(response.text)

            # PRINT RESPONSE: pretty print with 4 indent
            # print(json.dumps(json_result, indent=4, sort_keys=True))
            issue_id = jp.match1("$.issues[?(key='"+key+"')].id", json_result)
            print(f"Issue id for key {key} is:{issue_id}")
            return issue_id

    """Prints the metaData required for issue creation"""
    def get_create_issue_meta_data(self):
        end_point = '/rest/api/2/issue/createmeta'
        response = requests.get(self.url+end_point, auth=(self.user, self.token))

        if tools.is_json(response.text):
            # JSON RESPONSE: convert response to JSON
            json_result = json.loads(response.text)

            # PRINT RESPONSE: pretty print with 4 indent
            print(json.dumps(json_result, indent=4, sort_keys=True))

    """Creates an issue and returns a tuple of issue_key and issue_Id"""
    def create_issue(self, issue_type_id, project_id, summary, description):
        end_point = "rest/api/2/issue"
        payload = {
            "fields": {
                "project": {
                    "id": project_id
                },
                "summary": summary,
                "description": description,
                "issuetype": {
                    "id": issue_type_id
                }
            }
        }
        response = requests.post(self.url + end_point, auth=(self.user, self.token), json=payload)

        if tools.is_json(response.text):
            # JSON RESPONSE: convert response to JSON
            json_result = json.loads(response.text)
            # PRINT RESPONSE: pretty print with 4 indent
            print(json.dumps(json_result, indent=4, sort_keys=True))

            issue_key = jp.match1("key", json_result)
            issue_id = jp.match1("id", json_result)

            print(f"Issure create with key {issue_key} and ID {issue_id}")
            return issue_key, issue_id

    def get_issue_id_with_issue_name(self, issue_name):
        end_point = f"/rest/api/latest/issue/{issue_name}"
        response = requests.get(self.url + end_point, auth=(self.user, self.token))
        assert response.status_code == 200

        if tools.is_json(response.text):
            # JSON RESPONSE: convert response to JSON
            json_result = json.loads(response.text)

            # PRINT RESPONSE: pretty print with 4 indent
            # print(json.dumps(json_result, indent=4, sort_keys=True))
            issue_id = jp.match1("id", json_result)
            print(f"Issue id for key {issue_name} is:{issue_id}")
            return issue_id
