from lib.base import BaseJiraAction
from utils import remove_empty_attributes

__all__ = ["AddGadgetAction"]


class AddGadgetAction(BaseJiraAction):
    def run(
        self,
        dashboard_id,
        color=None,
        ignore_uri_and_module_key_validation=None,
        module_key=None,
        position=None,
        title=None,
        uri=None,
    ):
        data = remove_empty_attributes(
            {
                "dashboard_id": dashboard_id,
                "color": color,
                "ignore_uri_and_module_key_validation": ignore_uri_and_module_key_validation,
                "module_key": module_key,
                "position": position,
                "title": title,
                "uri": uri,
            }
        )

        gadget = self._client.add_gadget_to_dashboard(**data)
        return gadget.raw
