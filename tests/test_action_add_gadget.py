import mock
from add_gadget import AddGadgetAction
from jira.resources import DashboardGadget

from tests.lib.actions import JIRABaseActionTestCase


class AddGadgetTests(JIRABaseActionTestCase):
    __test__ = True
    action_cls = AddGadgetAction

    @mock.patch("requests.Session.request")
    @mock.patch("lib.base.JIRA.add_gadget_to_dashboard")
    def test_add_gadget(self, mocked_add_gadget, mocked_request):
        dashboard_id = 1

        action = self.get_action_instance(self.full_auth_passwd_config)
        mocked_add_gadget.return_value = DashboardGadget(
            {}, {}, self.load_json_fixture("gadget.json")
        )
        result = action.run(dashboard_id)
        self.assertEqual(result["color"], "cyan")
