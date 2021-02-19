from models.Cycle import CycleResource
from models.Execution import ExecutionResource
from models.JiraServerPlatform import JiraResources
from utils import tools

# ZEPHYR INFORMATION

ACCOUNT_ID = ''
ACCESS_KEY = ''
SECRET_KEY = ''

# JIRA INFORMATION
TOKEN = ''
USER = ''
URL = ""


class Runner(object):
    def __init__(self, version_name, cycle_name, project_name):
        self.jira = JiraResources(URL, USER, TOKEN)
        self.cycle = CycleResource(ACCOUNT_ID, ACCESS_KEY, SECRET_KEY)

        self.project_id = self.jira.get_project_id_with_name(project_name)

        if version_name == "-1":
            self.version_id = version_name
        else:
            self.version_id = self.jira.get_version_id_with_name(version_name, self.project_id)

        self.cycle_id = self.cycle.create_cycle(cycle_name, self.project_id, self.version_id)
        self.execution = ExecutionResource(ACCOUNT_ID, ACCESS_KEY, SECRET_KEY)

    def create_fetch_execute_update(self, issues_id):
        # Add tests to the cycle
        self.execution.add_tests_to_cycle(issues_id, self.cycle_id, self.project_id, self.version_id)

        # Get list of executions by cycle
        execution_id = self.execution.get_list_of_execution_by_cycle(self.cycle_id, self.project_id, self.version_id)

        # Updating Execution result

        statuses = [1]  # status for all the tests in the cycle

        if not issues_id:
            for i in range(0, len(execution_id)):
                self.execution.update_execution(execution_id[i], self.project_id, self.version_id, self.cycle_id,
                                                issues_id[i], statuses[i])

    def create_test_fetch_cyle_create_execution(self):

        # Create test
        issue_list = self.jira.create_issue("10005", self.project_id, "Summary", "Description")

        # Get Cycle
        cycle_id = self.cycle.get_cycle_with_name(self.version_id, self.project_id, "Cycle Name")

        # Create Execution
        self.execution.create_execution(self.project_id, self.version_id, self.cycle_id, issue_list[0][1], 1)

    def get_issues_id(self, issues):
        issues_id = []

        for issue in issues:
            for key in issue.keys():
                issues_id.append(self.jira.get_issue_id_with_issue_name(key))

        return issues_id

    def set_issues_id(self, issues):

        for issue in issues:
            for key in issue.keys():
                issue[key]['id'] = self.jira.get_issue_id_with_issue_name(key)

        return issues

    def create_executions_for_cycle(self, issues):
        """
        Create executions by Issue_id for the self.cycle
        """
        for issue in issues:
            for key, value in issue.items():
                print(f"Adding the issue {key} into the cycle {self.cycle_id}")
                self.execution.create_execution(value['id'], self.project_id, self.version_id, self.cycle_id,
                                                status=value['status_id'])

        return True
