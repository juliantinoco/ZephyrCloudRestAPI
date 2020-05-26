import requests
import json
import jsonpath_rw_ext as jp

class JiraResources:

    def __init__(self,url,user,token):
        self.url = url
        self.user = user
        self.token = token

    def is_json(self,data):
        try:
            json.loads(data)
        except ValueError:
            return False
        return True

    """Returns the project_Id corresponding to project_name"""
    def get_project_id_with_name(self,project_name):

        end_point = "rest/api/2/project"
        response = requests.get(self.url + end_point, auth=(self.user, self.token))
        assert response.status_code == 200
        if self.is_json(response.text):
            # JSON RESPONSE: convert response to JSON
            json_result = json.loads(response.text)

            # PRINT RESPONSE: pretty print with 4 indent
            # print(json.dumps(json_result, indent=4, sort_keys=True))

            project_id = jp.match1("$[?(name='"+project_name+"')].id", json_result)
            print("Project ID {} with Name {}".format(project_id,project_name))
            return project_id

    """Returns the version_Id corresponding to version name in an project"""
    def get_version_id_with_name(self,version_name,project_id):

        end_point= "rest/api/2/project/" + project_id +"/version"
        response = requests.get(self.url + end_point, auth=(self.user, self.token))
        assert response.status_code == 200
        if self.is_json(response.text):
            # JSON RESPONSE: convert response to JSON
            json_result = json.loads(response.text)

            # PRINT RESPONSE: pretty print with 4 indent
            # print(json.dumps(json_result, indent=4, sort_keys=True))

            version_id=jp.match1("$.values[?(name='"+ version_name + "')].id",json_result)
            print("Version ID {} with Name {}".format(version_id,version_name))
            return version_id

    """Returns the issue for corresponding issue_Key"""
    def get_issue_id_with_key(self,key):
        end_point='/rest/api/2/search'
        response = requests.get(self.url + end_point, auth=(self.user, self.token))
        assert response.status_code == 200
        if self.is_json(response.text):
            # JSON RESPONSE: convert response to JSON
            json_result = json.loads(response.text)

            # PRINT RESPONSE: pretty print with 4 indent
            # print(json.dumps(json_result, indent=4, sort_keys=True))
            issue_id=jp.match1("$.issues[?(key='"+key+"')].id",json_result)
            print("Issue id for key {} is:{}".format(key,issue_id))
            return issue_id

    """Prints the metaData required for issue creation"""
    def get_create_issue_meta_data(self):
        end_point='/rest/api/2/issue/createmeta'
        response=requests.get(self.url+end_point,auth=(self.user,self.token))
        if self.is_json(response.text):
            # JSON RESPONSE: convert response to JSON
            json_result = json.loads(response.text)

            # PRINT RESPONSE: pretty print with 4 indent
            print(json.dumps(json_result, indent=4, sort_keys=True))

    """Creates an issue and returns a tuple of issue_key and issue_Id"""
    def create_issue(self,issue_type_Id,project_Id,summary,description):
        end_point = "rest/api/2/issue"
        payload = {
            "fields": {
                "project": {
                    "id": project_Id
                },
                "summary": summary,
                "description": description,
                "issuetype": {
                    "id": issue_type_Id
                }
            }
        }
        response = requests.post(self.url + end_point, auth=(self.user, self.token), json=payload)

        if self.is_json(response.text):
            # JSON RESPONSE: convert response to JSON
            json_result = json.loads(response.text)
            # PRINT RESPONSE: pretty print with 4 indent
            print(json.dumps(json_result, indent=4, sort_keys=True))

            issue_Key=jp.match1("key",json_result)
            issue_Id=jp.match1("id",json_result)

            print("Issure create with key {} and ID {}".format(issue_Key, issue_Id))
            return (issue_Key,issue_Id)
