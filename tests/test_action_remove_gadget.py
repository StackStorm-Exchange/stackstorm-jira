import mock
from jira.resources import Dashboard, DashboardGadget
from remove_gadget import RemoveGadgetAction

from tests.lib.actions import JIRABaseActionTestCase


class RemoveGadgetTests(JIRABaseActionTestCase):
    __test__ = True
    action_cls = RemoveGadgetAction

    @mock.patch("lib.base.JIRA.dashboard")
    @mock.patch("requests.Session.request")
    @mock.patch("jira.resources.DashboardGadget.delete")
    def test_remove_gadget(
        self, mocked_delete_gadget, mocked_request, mocked_dashboard
    ):
        status_code = 204
        text = ""

        gadget = DashboardGadget({}, {}, raw=self.load_json_fixture("gadget.json"))
        dashboard = Dashboard({}, {}, raw=self.load_json_fixture("dashboard.json"))
        dashboard.gadgets.append(gadget)
        mocked_dashboard.return_value = dashboard

        mocked_delete_gadget.return_value = mock.MagicMock(
            status_code=status_code, text=text
        )
        action = self.get_action_instance(self.full_auth_passwd_config)
        result, data = action.run(dashboard.id, str(gadget.id))

        self.assertTrue(result)
        self.assertEqual(data["status_code"], status_code)
        self.assertEqual(data["response_text"], text)
