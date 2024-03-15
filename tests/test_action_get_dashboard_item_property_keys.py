import mock
from get_dashboard_item_property_keys import GetDashboardItemPropertyKeysAction
from jira.resources import DashboardItemPropertyKey

from tests.lib.actions import JIRABaseActionTestCase


class GetDashboardItemPropertyKeysTests(JIRABaseActionTestCase):
    __test__ = True
    action_cls = GetDashboardItemPropertyKeysAction

    @mock.patch("requests.Session.request")
    @mock.patch("lib.base.JIRA.dashboard_item_property_keys")
    def test_get_dashboard_item_property_keys(
        self, mocked_dashboard_item_property_keys, mocked_request
    ):
        action = self.get_action_instance(self.full_auth_passwd_config)
        key = DashboardItemPropertyKey(
            {}, {}, self.load_json_fixture("dashboard_item_property_key.json")
        )
        mocked_dashboard_item_property_keys.return_value = [key]
        result = action.run("1", "2")
        self.assertIsInstance(result, list)
        self.assertEqual(result[0], key.raw)
