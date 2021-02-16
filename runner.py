from models.Cycle import CycleResource
from models.Execution import ExecutionResource
from models.JiraServerPlatform import JiraResources


# ZEPHYR INFORMATION

ACCOUNT_ID = ''
ACCESS_KEY = ''
SECRET_KEY = ''

# JIRA INFORMATION
TOKEN = ''
USER = ''
URL = ""


def create_fetch_execute_update():
    cycle = CycleResource(ACCOUNT_ID, ACCESS_KEY, SECRET_KEY)
    execution = ExecutionResource(ACCOUNT_ID, ACCESS_KEY, SECRET_KEY)
    jira = JiraResources(URL, USER, TOKEN)

    # fetching project ID
    project_id = jira.get_project_id_with_name("Project Name")
    # fetching version ID
    version_id = jira.get_version_id_with_name("Version Name",project_id)
    # fetching issue_ID

    # Creating cycle
    cycle_id = cycle.create_cycle("Cycle Name",project_id,version_id)

    # Add tests to the cycle
    execution.add_tests_to_cycle(['issue_Keys'],cycle_id,project_id,version_id)

    # Get list of executions by cycle
    execution_id = execution.get_list_of_execution_by_cycle(cycle_id,project_id,version_id)

    # Updating Execution result

    statuses = [1]  # status for all the tests in the cycle
    issues_id = ["issueID's"]

    for i in range(0, len(execution_id)):
        execution.update_execution(execution_id[i], project_id, version_id, cycle_id, issues_id[i], statuses[i])


def create_test_fetch_cyle_create_execution():

    cycle = CycleResource(ACCOUNT_ID, ACCESS_KEY, SECRET_KEY)
    execution = ExecutionResource(ACCOUNT_ID, ACCESS_KEY, SECRET_KEY)
    jira = JiraResources(URL, USER, TOKEN)

    # fetching project ID
    project_id = jira.get_project_id_with_name("Project Name")
    # fetching version ID
    version_id = jira.get_version_id_with_name("Version Name", project_id)

    # Create test
    issue_list = jira.create_issue("10005", project_id, "Summary", "Description")

    # Get Cycle
    cycle_id = cycle.get_cycle_with_name(version_id, project_id, "Cycle Name")

    # Create Execution
    execution.create_execution(project_id, version_id, cycle_id, issue_list[0][1], 1)


if __name__ == '__main__':
    create_fetch_execute_update()
