import mock
from jira.resources import DashboardItemProperty
from update_dashboard_item_property import UpdateDashboardItemPropertyAction

from tests.lib.actions import JIRABaseActionTestCase


class UpdateDashboardItemPropertyTests(JIRABaseActionTestCase):
    __test__ = True
    action_cls = UpdateDashboardItemPropertyAction

    @mock.patch("jira.resources.DashboardItemProperty.update")
    @mock.patch("requests.Session.request")
    @mock.patch("lib.base.JIRA.dashboard_item_property")
    def test_set_dashboard_item_property(
        self,
        mocked_dashboard_item_property,
        mocked_request,
        mocked_dashboard_property_update,
    ):
        updated_count = 10
        updated_data = {"num": updated_count}
        action = self.get_action_instance(self.full_auth_passwd_config)

        original_data = self.load_json_fixture("dashboard_item_property_key.json")
        original_item_property = DashboardItemProperty({}, {}, original_data)
        mocked_dashboard_item_property.return_value = original_item_property

        original_data.update(updated_data)
        mocked_dashboard_property_update.return_value = DashboardItemProperty(
            {}, {}, original_data
        )

        result = action.run("1", "2", "config", value=updated_data)
        self.assertEqual(result["num"], updated_count)
