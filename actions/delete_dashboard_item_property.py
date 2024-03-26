from lib.base import BaseJiraAction

__all__ = ["DeleteDashboardItemPropertyAction"]


class DeleteDashboardItemPropertyAction(BaseJiraAction):
    def run(self, dashboard_id, item_id, property_key):
        dashboard_item_property = self._client.dashboard_item_property(
            dashboard_id,
            item_id,
            property_key,
        )
        response = dashboard_item_property.delete(dashboard_id, item_id)
        result = {"status_code": response.status_code, "response_text": response.text}
        return bool(response.status_code == 204), result
