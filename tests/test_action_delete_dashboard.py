import mock
from delete_dashboard import DeleteJiraDashboardAction

from tests.lib.actions import JIRABaseActionTestCase


class DeleteDashboardTests(JIRABaseActionTestCase):
    __test__ = True
    action_cls = DeleteJiraDashboardAction

    @mock.patch("requests.Session.request")
    @mock.patch("jira.resources.Dashboard.delete")
    def test_delete_dashboard(self, mocked_delete_dashboard, mocked_request):
        status_code = 204
        text = ""
        mocked_delete_dashboard.return_value = mock.MagicMock(
            status_code=status_code, text=text
        )
        action = self.get_action_instance(self.full_auth_passwd_config)

        result, data = action.run("id")

        self.assertTrue(result)
        self.assertEqual(data["status_code"], status_code)
        self.assertEqual(data["response_text"], text)
