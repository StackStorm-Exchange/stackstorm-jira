import mock
from get_available_gadgets import GetAvailableGadgetsAction
from jira.resources import DashboardGadget

from tests.lib.actions import JIRABaseActionTestCase


class GetAvailableGadgetsTests(JIRABaseActionTestCase):
    __test__ = True
    action_cls = GetAvailableGadgetsAction

    @mock.patch("requests.Session.request")
    @mock.patch("lib.base.JIRA.all_dashboard_gadgets")
    def test_get_available_gadgets(self, mocked_gadgets, mocked_request):
        action = self.get_action_instance(self.full_auth_passwd_config)
        gadget = DashboardGadget({}, {}, self.load_json_fixture("gadget.json"))
        mocked_gadgets.return_value = [gadget]
        result = action.run()
        self.assertIsInstance(result, list)
        self.assertEqual(result[0], gadget.raw)
