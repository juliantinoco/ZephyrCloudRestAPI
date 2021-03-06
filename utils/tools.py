from enum import Enum

import json


class Status(Enum):
    UNEXECUTED = -1
    PASS = 1
    FAIL = 2
    WIP = 3
    BLOCKED = 4


def is_json(data):
    try:
        json.loads(data)
    except ValueError:
        return False
    return True


def organize_issues_id(issues_status):
    """
    Convert from the format OrderedDict([('@pass', '1'), ('@fail', '0'), ('#text', 'ISSUE')]) to
     [{'ISSUE': {'status_id': Status.value}}]
     These tags are taken from a XML report from Robot Framework
    """
    issues_formatted = []

    for issue_status in issues_status:
        current = {issue_status['#text']: {'status_id': Status.PASS.value}}

        if issue_status['@fail'] == '1':
            current[issue_status['#text']]['status_id'] = Status.FAIL.value

        issues_formatted.append(current)

    return issues_formatted


def get_json_results(result):
    """
    This function will return the answer if the answer code is 200.
    Otherwise, the error code is logged for troubleshooting
    """
    if result.status_code == 200 and is_json(result.text):
        return json.loads(result.text)

    else:
        print(f"The result code not successful. The error code is: {result.status_code}")
        return False
