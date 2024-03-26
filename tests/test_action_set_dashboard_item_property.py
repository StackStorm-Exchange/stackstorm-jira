import mock
from jira.resources import DashboardItemProperty
from set_dashboard_item_property import SetDashboardItemPropertyAction

from tests.lib.actions import JIRABaseActionTestCase


class SetDashboardItemPropertyTests(JIRABaseActionTestCase):
    __test__ = True
    action_cls = SetDashboardItemPropertyAction

    @mock.patch("requests.Session.request")
    @mock.patch("lib.base.JIRA.set_dashboard_item_property")
    def test_get_dashboard_item_property(
        self, mocked_dashboard_item_property, mocked_request
    ):
        action = self.get_action_instance(self.full_auth_passwd_config)
        item_property = DashboardItemProperty(
            {}, {}, self.load_json_fixture("dashboard_item_property_key.json")
        )
        mocked_dashboard_item_property.return_value = item_property
        value = {"num": "5"}
        result = action.run("1", "2", "config", value=value)
        self.assertEqual(result, item_property.raw)
