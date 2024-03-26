import mock
from jira.resources import Dashboard
from update_dashboard import UpdateJiraDashboardAction

from tests.lib.actions import JIRABaseActionTestCase


class UpdateDashboardTests(JIRABaseActionTestCase):
    __test__ = True
    action_cls = UpdateJiraDashboardAction

    @mock.patch("lib.base.JIRA.dashboard")
    @mock.patch("requests.Session.request")
    @mock.patch("jira.resources.Dashboard.update")
    def test_update_dashboard(
        self, mock_update_dashboard, mock_request, mocked_dashboard
    ):
        board_name = "Test Board Updated"
        description = "This Board is a Test Board that has been updated"
        update_data = {"name": board_name, "description": description}
        original_data = self.load_json_fixture("dashboard.json")

        action = self.get_action_instance(self.full_auth_passwd_config)
        original_dashboard = Dashboard({}, {}, raw=original_data)
        mocked_dashboard.return_value = original_dashboard

        original_data.update(update_data)

        mock_update_dashboard.return_value = Dashboard({}, {}, raw=original_data)
        result = action.run(original_dashboard.id, **update_data)
        self.assertEqual(result["name"], board_name)
        self.assertEqual(result["description"], description)
