import mock
from get_dashboard_gadgets import GetDashboardGadgetsAction
from jira.resources import Dashboard, DashboardGadget

from tests.lib.actions import JIRABaseActionTestCase


class GetDashboardGadgetsTest(JIRABaseActionTestCase):
    __test__ = True
    action_cls = GetDashboardGadgetsAction

    @mock.patch("lib.base.JIRA.dashboard_gadgets")
    @mock.patch("requests.Session.request")
    def test_get_dashboard_gadgets(self, mocked_request, mocked_dashboard):
        dashboard = Dashboard({}, {}, raw=self.load_json_fixture("dashboard.json"))
        gadget = DashboardGadget({}, {}, raw=self.load_json_fixture("gadget.json"))

        dashboard.gadgets.append(gadget)
        mocked_dashboard.return_value = dashboard.gadgets

        action = self.get_action_instance(self.full_auth_passwd_config)
        result = action.run(dashboard.id)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0], gadget.raw)
