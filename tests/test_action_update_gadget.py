import mock
from jira.resources import Dashboard, Gadget
from update_gadget import UpdateGadgetAction

from tests.lib.actions import JIRABaseActionTestCase


class UpdateGadgetTests(JIRABaseActionTestCase):
    __test__ = True
    action_cls = UpdateGadgetAction

    @mock.patch("jira.resources.Gadget.update")
    @mock.patch("requests.Session.request")
    @mock.patch("lib.base.JIRA.dashboard")
    def test_update_gadget(
        self, mocked_dashboard, mocked_request, mocked_update_gadget
    ):
        updated_color = "blue"
        updated_title = "Updated Title"
        update_data = {"color": updated_color, "title": updated_title}

        original_gadget_data = self.load_json_fixture("gadget.json")

        action = self.get_action_instance(self.full_auth_passwd_config)
        original_gadget = Gadget({}, {}, raw=original_gadget_data)
        dashboard = Dashboard({}, {}, raw=self.load_json_fixture("dashboard.json"))
        dashboard.gadgets.append(original_gadget)

        original_gadget_data.update(update_data)

        mocked_dashboard.return_value = dashboard
        mocked_update_gadget.return_value = Gadget({}, {}, raw=original_gadget_data)

        result = action.run(dashboard.id, str(original_gadget.id), **update_data)
        self.assertEqual(result["color"], updated_color)
        self.assertEqual(result["title"], updated_title)
