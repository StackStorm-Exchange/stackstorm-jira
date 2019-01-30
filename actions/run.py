from lib.base import BaseJiraAction

__all__ = [
    'ActionManager'
]


class ActionManager(BaseJiraAction):

    def run(self, **kwargs):
        action = kwargs.pop('action')
        return getattr(self, action)(**kwargs)
