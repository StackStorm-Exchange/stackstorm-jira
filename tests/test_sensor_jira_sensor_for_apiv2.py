import mock

from st2tests.base import BaseSensorTestCase

from jira_sensor_for_apiv2 import JIRASensorForAPIv2

JIRA_URL = "http://jira.hoge.com/"
PROJECT_NAME = "PROJECT"
ISSUE_ID = "112"
ISSUE_SELF = "http://jira.hoge.com/rest/api/2/issue/" + ISSUE_ID
ISSUE_KEY = "ISSUEKEY-1"

ISSUE = {
    "project": PROJECT_NAME,
    "id": ISSUE_ID,
    "expand": "html,editmeta,changelog",
    "fields": {
        "assignee": None,
        "creator": {
            "displayName": "user01@test",
            "name": "user-name"
        },
        "issuetype": {
            "name": "task"
        },
        "components": [
            {
                "id": "421203",
                "name": "test_components"
            }
        ]
    }
}

MOCK_ISSUE_RAW = ISSUE.copy()
MOCK_ISSUE_RAW["key"] = ISSUE_KEY
MOCK_ISSUE_RAW["self"] = ISSUE_SELF

PAYLOAD = ISSUE.copy()
PAYLOAD["issue_key"] = ISSUE_KEY
PAYLOAD["issue_url"] = ISSUE_SELF
PAYLOAD["issue_browse_url"] = JIRA_URL + '/browse/' + ISSUE_KEY

TRIGGER = {
    "trace_context": None,
    "trigger": "jira.issues_tracker_for_apiv2",
    "payload": PAYLOAD
}


class JIRASensorForAPIv2TestCase(BaseSensorTestCase):
    maxDiff = None
    sensor_cls = JIRASensorForAPIv2

    def test_poll(self):
        sensor = self.get_sensor_instance()
        sensor._jira_client = mock.Mock()
        sensor._jira_client.search_issues.return_value = []
        sensor._issues_in_project = {}

        # no issues
        sensor.poll()
        self.assertEqual(self.get_dispatched_triggers(), [])

        # 1 new issue
        issue = mock.Mock()
        issue.raw = MOCK_ISSUE_RAW
        issue.id = ISSUE_ID
        issue.self = ISSUE_SELF
        issue.key = ISSUE_KEY

        sensor._project = PROJECT_NAME
        sensor._jira_url = JIRA_URL
        sensor._jira_client.search_issues.return_value = [issue]

        sensor.poll()
        payload = self.get_dispatched_triggers()[0]['payload']
        self.assertEqual(payload, PAYLOAD)

        # 1 new issue
        issue = mock.Mock()
        issue.raw = MOCK_ISSUE_RAW
        issue.id = ISSUE_ID
        issue.self = ISSUE_SELF
        issue.key = ISSUE_KEY

        sensor._project = PROJECT_NAME
        sensor._jira_url = JIRA_URL
        sensor._jira_client.search_issues.return_value = [issue]

        sensor.poll()
        payload = self.get_dispatched_triggers()[0]['payload']
        self.assertEqual(payload, PAYLOAD)
