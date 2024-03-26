from lib.base import BaseJiraAction
from lib.utils import remove_empty_attributes

__all__ = ["UpdateGadgetAction"]


class UpdateGadgetAction(BaseJiraAction):
    def run(self, dashboard_id, gadget_id, color=None, position=None, title=None):
        data = remove_empty_attributes(
            {
                "dashboard_id": dashboard_id,
                "color": color,
                "position": position,
                "title": title,
            }
        )

        dashboard = self._client.dashboard(dashboard_id)
        gadget = next(
            gadget for gadget in dashboard.gadgets if str(gadget.id) == gadget_id
        )
        gadget = gadget.update(**data)

        return gadget.raw
