from lib.base import BaseJiraAction

__all__ = [
    'ActionManager'
]


class ActionManager(BaseJiraAction):

    def run(self, action, **kwargs):
        return getattr(self._client, action)(**kwargs)
