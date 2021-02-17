from runner import UpdateZephyr

import argparse
import xmltodict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update XML report to Zephyr')
    parser.add_argument('--xml', metavar='N',
                        help='path to read the xml report')
    parser.add_argument('--cycle', metavar='N',
                        help='Zephyr Cycle Id. If not added, a new cycle will create.')
    parser.add_argument('--version', metavar='N', default='-1',
                        help='Version ID. (Default) UNSCHEDULED')
    parser.add_argument('--project', metavar='N',
                        help='Project ID.')

    args_parsed = parser.parse_args().__dict__

    # open file:
    with open(args_parsed['xml']) as xml_file:
        report = xmltodict.parse(xml_file.read())

    # get tags status
    issue_results = report['robot']['statistics']['tag']['stat']
    cycle_name = args_parsed['cycle']
    version_name = args_parsed['version']
    project_name = args_parsed['project']

    zephyr = UpdateZephyr(version_name, cycle_name, project_name)
