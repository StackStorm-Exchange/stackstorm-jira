from lib.base import BaseJiraAction

__all__ = ["GetAvailableGadgetsAction"]


class GetAvailableGadgetsAction(BaseJiraAction):
    def run(self):
        gadgets = self._client.gadgets()
        return [gadget.raw for gadget in gadgets]
