import mock
from create_dashboard import CreateJiraDashboardAction
from jira.resources import Dashboard

from tests.lib.actions import JIRABaseActionTestCase


class CreateDashboardTests(JIRABaseActionTestCase):
    __test__ = True
    action_cls = CreateJiraDashboardAction

    @mock.patch("requests.Session.request")
    @mock.patch("lib.base.JIRA.create_dashboard")
    def test_create_dashboard(self, mock_create_dashboard, mock_request):
        board_name = "Test Board"
        description = "This Board is a Test Board"

        action = self.get_action_instance(self.full_auth_passwd_config)
        mock_create_dashboard.return_value = Dashboard(
            {}, {}, raw=self.load_json_fixture("dashboard.json")
        )
        result = action.run(name="Test Board", description="The Funnest Board Around")
        self.assertEqual(result["name"], board_name)
        self.assertEqual(result["description"], description)
