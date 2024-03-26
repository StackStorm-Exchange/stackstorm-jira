from lib.base import BaseJiraAction
from utils import remove_empty_attributes

__all__ = ["CreateJiraDashboardAction"]


class CreateJiraDashboardAction(BaseJiraAction):
    def run(
        self, name, description=None, edit_permissions=None, share_permissions=None
    ):
        data = remove_empty_attributes(
            {
                "name": name,
                "description": description,
                "edit_permissions": edit_permissions,
                "share_permissions": share_permissions,
            }
        )

        dashboard = self._client.create_dashboard(**data)
        return dashboard.raw
