from lib.base import BaseJiraAction

__all__ = ["GetDashboardGadgetsAction"]


class GetDashboardGadgetsAction(BaseJiraAction):
    def run(self, dashboard_id):
        gadgets = self._client.dashboard_gadgets(dashboard_id)
        return [gadget.raw for gadget in gadgets]
