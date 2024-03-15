import mock
from copy_dashboard import CopyJiraDashboardAction
from jira.resources import Dashboard

from tests.lib.actions import JIRABaseActionTestCase


class CopyDashboardTests(JIRABaseActionTestCase):
    __test__ = True
    action_cls = CopyJiraDashboardAction

    @mock.patch("requests.Session.request")
    @mock.patch("lib.base.JIRA.copy_dashboard")
    def test_copy_dashboard(self, mock_copy_dashboard, mock_request):
        board_name = "Test Board Copied"
        description = "This Board is a Test Board that has been copied"
        copy_data = {"name": board_name, "description": description}
        original_data = self.load_json_fixture("dashboard.json")

        action = self.get_action_instance(self.full_auth_passwd_config)

        original_data.update(copy_data)

        mock_copy_dashboard.return_value = Dashboard({}, {}, raw=original_data)
        result = action.run("id", **copy_data)
        self.assertEqual(result["name"], board_name)
        self.assertEqual(result["description"], description)
