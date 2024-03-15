from lib.base import BaseJiraAction

__all__ = ["UpdateJiraDashboardAutomaticRefreshAction"]


class UpdateJiraDashboardAutomaticRefreshAction(BaseJiraAction):
    def run(self, id, minutes):
        response = self._client.update_dashboard_automatic_refresh_seconds(id, minutes)
        result = {"status_code": response.status_code, "response_text": response.text}
        return bool(response.status_code == 204), result
