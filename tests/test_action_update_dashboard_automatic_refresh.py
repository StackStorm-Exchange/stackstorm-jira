import mock
from update_dashboard_automatic_refresh import UpdateJiraDashboardAutomaticRefreshAction

from tests.lib.actions import JIRABaseActionTestCase


class UpdateJiraDashboardAutomaticRefreshActionDashboardTests(JIRABaseActionTestCase):
    __test__ = True
    action_cls = UpdateJiraDashboardAutomaticRefreshAction

    @mock.patch("requests.Session.request")
    @mock.patch("lib.base.JIRA.update_dashboard_automatic_refresh_seconds")
    def test_update_dashboard_automatic_refresh(
        self, mock_automatic_refresh, mock_request
    ):
        dashboard_id = 1
        minutes = 5
        status_code = 204
        text = ""
        mock_automatic_refresh.return_value = mock.MagicMock(
            status_code=status_code, text=text
        )

        action = self.get_action_instance(self.full_auth_passwd_config)
        result, data = action.run(dashboard_id, minutes)

        self.assertTrue(result)
        self.assertEqual(data["status_code"], status_code)
        self.assertEqual(data["response_text"], text)
