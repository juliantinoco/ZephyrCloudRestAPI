from models.Cycle import Cycle_Resource
from models.Execution import Execution_Resource
from models.JiraServerPlatform import JiraResources


# ACCOUNT ID
ACCOUNT_ID = ''
# ACCESS KEY
ACCESS_KEY = ''
# SECRET KEY
SECRET_KEY = ''
#TOKEN
TOKEN= ''
#USER
USER= ''
#URL
URL= ""


def create_fetch_execute_update():
    cycle=Cycle_Resource(ACCOUNT_ID,ACCESS_KEY,SECRET_KEY)
    execution=Execution_Resource(ACCOUNT_ID,ACCESS_KEY,SECRET_KEY)
    jira=JiraResources(URL,USER,TOKEN)

    #fetching project ID
    project_Id=jira.get_project_id_with_name("Project Name")
    #fetching version ID
    version_Id=jira.get_version_id_with_name("Version Name",project_Id)
    #fetching issue_ID
    issue_ID_RF2=jira.get_issue_id_with_key('issue_key')
    issue_ID_RF4=jira.get_issue_id_with_key('issue_key')

    # Creating cycle
    cycle_Id=cycle.create_cycle("Cycle Name",project_Id,version_Id)

    #Add tests to the cycle
    execution.add_tests_to_cycle(['issue_Keys'],cycle_Id,project_Id,version_Id)

    #Get list of executions by cycle
    execution_id=execution.get_list_of_execution_by_cycle(cycle_Id,project_Id,version_Id)

    #Updating Executin result

    statuses=[1]  # status for all the tests in the cycle
    issue_ID=["issueID's"]
    for i in  range(0,len(execution_id)):
        execution.update_execution(execution_id[i],project_Id,version_Id,cycle_Id,issue_ID[i],statuses[i])

def createTest_fetchCyle_createExecution():
    cycle = Cycle_Resource(ACCOUNT_ID, ACCESS_KEY, SECRET_KEY)
    execution = Execution_Resource(ACCOUNT_ID, ACCESS_KEY, SECRET_KEY)
    jira = JiraResources(URL, USER, TOKEN)

    # fetching project ID
    project_Id = jira.get_project_id_with_name("Project Name")
    # fetching version ID
    version_Id = jira.get_version_id_with_name("Version Name", project_Id)

    # Create test
    issue_list = jira.create_issue("10005", project_Id, "Summary",
                                   "Description")

    # Get Cycle
    cycle_Id=cycle.get_cycle_with_name(version_Id, project_Id, "Cycle Name")

    # Create Execution
    execution.create_execution(project_Id,version_Id,cycle_Id,issue_list[0][1],1)



if __name__ == '__main__':
    create_fetch_execute_update()
