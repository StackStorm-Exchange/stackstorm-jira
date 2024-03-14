from lib.base import BaseJiraAction

__all__ = ["RemoveGadgetAction"]


class RemoveGadgetAction(BaseJiraAction):
    def run(self, dashboard_id, gadget_id):
        dashboard = self._client.dashboard(dashboard_id)
        gadget = next(
            gadget for gadget in dashboard.gadgets if str(gadget.id) == gadget_id
        )
        response = gadget.delete(dashboard_id)
        result = {"status_code": response.status_code, "response_text": response.text}
        return bool(response.status_code == 204), result
