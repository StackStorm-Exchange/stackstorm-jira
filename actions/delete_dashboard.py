from lib.base import BaseJiraAction

__all__ = ["DeleteJiraDashboardAction"]


class DeleteJiraDashboardAction(BaseJiraAction):
    def run(self, dashboard_id):
        dashboard = self._client.dashboard(dashboard_id)
        response = dashboard.delete()
        result = {"status_code": response.status_code, "response_text": response.text}
        return bool(response.status_code == 204), result
