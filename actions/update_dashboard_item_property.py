from lib.base import BaseJiraAction

__all__ = ["UpdateDashboardItemPropertyAction"]


class UpdateDashboardItemPropertyAction(BaseJiraAction):
    def run(self, dashboard_id, item_id, property_key, value):
        dashboard_item_property = self._client.dashboard_item_property(
            dashboard_id,
            item_id,
            property_key,
        )
        dashboard_item_property = dashboard_item_property.update(
            dashboard_id, item_id, value
        )
        return dashboard_item_property.raw
