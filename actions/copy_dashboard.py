from lib.base import BaseJiraAction
from lib.utils import remove_empty_attributes

__all__ = ["CopyJiraDashboardAction"]


class CopyJiraDashboardAction(BaseJiraAction):
    def run(
        self,
        id,
        name,
        description=None,
        edit_permissions=None,
        share_permissions=None,
    ):
        data = remove_empty_attributes(
            {
                "id": id,
                "name": name,
                "description": description,
                "edit_permissions": edit_permissions,
                "share_permissions": share_permissions,
            }
        )

        dashboard = self._client.copy_dashboard(**data)
        return dashboard.raw
