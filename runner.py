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


class UpdateZephyr:
    def __int__(self, version_name, cycle_name, project_name):
        self.jira = JiraResources(URL, USER, TOKEN)
        self.version_id = self.jira.get_version_id_with_name(version_name, self.project_id)
        self.cycle = self.cycle.create_cycle(cycle_name, self.project_id, self.version_id)
        self.project_name = project_name
        self.project_id = self.jira.get_project_id_with_name(project_name)

    @staticmethod
    def get_cycle_id():
        return CycleResource(ACCOUNT_ID, ACCESS_KEY, SECRET_KEY)

    def get_project_id(self, project_name):
        return

    def create_fetch_execute_update(self, issues_id):

        execution = ExecutionResource(ACCOUNT_ID, ACCESS_KEY, SECRET_KEY)

        # Add tests to the cycle
        execution.add_tests_to_cycle(issues_id, self.cycle_id, self.project_id, self.version_id)

        # Get list of executions by cycle
        execution_id = execution.get_list_of_execution_by_cycle(self.cycle_id, self.project_id, self.version_id)

        # Updating Execution result

        statuses = [1]  # status for all the tests in the cycle

        if not issues_id:
            for i in range(0, len(execution_id)):
                execution.update_execution(execution_id[i], self.project_id, self.version_id, self.cycle_id,
                                           issues_id[i], statuses[i])

    def create_test_fetch_cyle_create_execution(self):
        execution = ExecutionResource(ACCOUNT_ID, ACCESS_KEY, SECRET_KEY)
        # Create test
        issue_list = self.jira.create_issue("10005", self.project_id, "Summary", "Description")

        # Get Cycle
        cycle_id = self.cycle.get_cycle_with_name(self.version_id, self.project_id, "Cycle Name")

        # Create Execution
        execution.create_execution(self.project_id, self.version_id, self.cycle_id, issue_list[0][1], 1)
