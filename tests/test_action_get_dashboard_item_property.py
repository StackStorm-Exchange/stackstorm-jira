import mock
from get_dashboard_item_property import GetDashboardItemPropertyAction
from jira.resources import DashboardItemProperty

from tests.lib.actions import JIRABaseActionTestCase


class GetDashboardItemPropertyTests(JIRABaseActionTestCase):
    __test__ = True
    action_cls = GetDashboardItemPropertyAction

    @mock.patch("requests.Session.request")
    @mock.patch("lib.base.JIRA.dashboard_item_property")
    def test_get_dashboard_item_property(
        self, mocked_dashboard_item_property, mocked_request
    ):
        action = self.get_action_instance(self.full_auth_passwd_config)
        item_property = DashboardItemProperty(
            {}, {}, self.load_json_fixture("dashboard_item_property_key.json")
        )
        mocked_dashboard_item_property.return_value = item_property
        result = action.run("1", "2", "config")
        self.assertEqual(result, item_property.raw)
