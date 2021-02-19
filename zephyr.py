from runner import Runner
from utils import tools

import argparse
import xmltodict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update XML report to Zephyr')
    parser.add_argument('--xml', metavar='N',
                        help='path to read the xml report')
    parser.add_argument('--cycle', metavar='N',
                        help='Zephyr Cycle Id. If not added, a new cycle will create.')
    parser.add_argument('--version', metavar='N', default='-1',
                        help='Version ID. (Default) UNSCHEDULED ID')
    parser.add_argument('--projectid', metavar='N',
                        help='Project ID.')
    parser.add_argument('--projectname', metavar='N', nargs="+",
                        help='Project Name.')
    parser.add_argument('--issues', metavar='N', nargs="+",
                        help='Add the list of the Issues')

    args_parsed = parser.parse_args().__dict__

    # open file:
    with open(args_parsed['xml']) as xml_file:
        report = xmltodict.parse(xml_file.read())

    if not args_parsed['issues']:
        # The issues are taken from Robot Framework (XML report)
        issue_results = report['robot']['statistics']['tag']['stat']
        issue_results = tools.organize_issues_id(issue_results)
    else:
        issue_results = args_parsed['issues']

    cycle_name = args_parsed['cycle']
    version_name = args_parsed['version']
    project_name = ' '.join(args_parsed['projectname'])

    zephyr = Runner(version_name, cycle_name, project_name)
    issues = zephyr.set_issues_id(issue_results)
    zephyr.create_executions_for_cycle(issues)
