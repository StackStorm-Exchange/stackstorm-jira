from lib.base import BaseJiraAction

__all__ = ["GetDashboardItemPropertyAction"]


class GetDashboardItemPropertyAction(BaseJiraAction):
    def run(self, dashboard_id, item_id, property_key):
        dashboard_item_property = self._client.dashboard_item_property(
            dashboard_id, item_id, property_key
        )
        return dashboard_item_property.raw
