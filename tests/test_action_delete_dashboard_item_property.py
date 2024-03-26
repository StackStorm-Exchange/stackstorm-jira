import mock
from delete_dashboard_item_property import DeleteDashboardItemPropertyAction
from jira.resources import DashboardItemProperty

from tests.lib.actions import JIRABaseActionTestCase


class DeleteDashboardItemPropertyTest(JIRABaseActionTestCase):
    __test__ = True
    action_cls = DeleteDashboardItemPropertyAction

    @mock.patch("jira.resources.DashboardItemProperty.delete")
    @mock.patch("lib.base.JIRA.dashboard_item_property")
    @mock.patch("requests.Session.request")
    def test_delete_dashboard_item_property(
        self,
        mocked_request,
        mocked_dashboard_item_property,
        mocked_dashboard_item_property_delete,
    ):
        status_code = 204
        text = ""

        dashboard_item_property = DashboardItemProperty(
            {}, {}, self.load_json_fixture("dashboard_item_property.json")
        )
        mocked_dashboard_item_property.return_value = dashboard_item_property
        mocked_dashboard_item_property_delete.return_value = mock.MagicMock(
            status_code=status_code, text=text
        )

        action = self.get_action_instance(self.full_auth_passwd_config)
        result, data = action.run("1", "2", "config")

        self.assertTrue(result)
        self.assertEqual(data["status_code"], status_code)
        self.assertEqual(data["response_text"], text)
