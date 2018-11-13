import mock

from st2tests.base import BaseSensorTestCase

from jira_sensor import JIRASensor

JIRA_URL = "https://ja.atlassian.com/"

MOCK_PAYLOAD = {
    "issue_name": "ISSUEKEY-1",
    "issue_url": "https://ja.atlassian.com/api/hoge",
    "issue_browse_url": JIRA_URL + "/browse/ISSUEKEY-1",
    "project": "PROJECT",
    "created": "2018-11-12T11:20:54.000+0900",
    "assignee": "user01",
    "fix_versions": ["verA"],
    "issue_type": "task"
}

MOCK_TRIGGER = {
    "trace_context": None,
    "trigger": "jira.issues_tracker",
    "payload": MOCK_PAYLOAD
}

MOCK_ISSUE_RAW = {
    "fields": {
        "created": MOCK_PAYLOAD["created"],
        "assignee": MOCK_PAYLOAD["assignee"],
        "fixVersions": MOCK_PAYLOAD["fix_versions"],
        "issuetype": {
            "name": MOCK_PAYLOAD["issue_type"]
        }
    }
}


class JIRASensorTestCase(BaseSensorTestCase):
    sensor_cls = JIRASensor

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

        issue.key = MOCK_PAYLOAD["issue_name"]
        issue.self = MOCK_PAYLOAD["issue_url"]
        sensor._project = MOCK_PAYLOAD["project"]
        sensor._jira_url = JIRA_URL
        sensor._jira_client.search_issues.return_value = [issue]

        sensor.poll()
        self.assertEqual(self.get_dispatched_triggers(), [MOCK_TRIGGER])
