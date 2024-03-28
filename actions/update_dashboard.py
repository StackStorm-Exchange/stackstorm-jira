from lib.base import BaseJiraAction
from lib.utils import remove_empty_attributes

__all__ = ["UpdateJiraDashboardAction"]


class UpdateJiraDashboardAction(BaseJiraAction):
    def run(
        self,
        dashboard_id,
        name,
        description=None,
        edit_permissions=None,
        share_permissions=None,
    ):
        data = remove_empty_attributes(
            {
                "name": name,
                "description": description,
                "editPermissions": edit_permissions,
                "sharePermissions": share_permissions,
            }
        )

        dashboard = self._client.dashboard(dashboard_id)
        dashboard.update(**data)
        return dashboard.raw
