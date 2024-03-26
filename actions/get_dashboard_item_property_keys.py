from lib.base import BaseJiraAction

__all__ = ["GetDashboardItemPropertyKeysAction"]


class GetDashboardItemPropertyKeysAction(BaseJiraAction):
    def run(self, dashboard_id, item_id):
        dashboard_item_property_keys = self._client.dashboard_item_property_keys(
            dashboard_id, item_id
        )
        return [
            item_property_key.raw for item_property_key in dashboard_item_property_keys
        ]
