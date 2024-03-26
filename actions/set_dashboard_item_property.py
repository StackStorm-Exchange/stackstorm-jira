from lib.base import BaseJiraAction

__all__ = ["SetDashboardItemPropertyAction"]


class SetDashboardItemPropertyAction(BaseJiraAction):
    def run(self, dashboard_id, item_id, property_key, value):
        dashboard_item_property = self._client.set_dashboard_item_property(
            dashboard_id, item_id, property_key, value
        )
        return dashboard_item_property.raw
