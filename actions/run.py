from jira.exceptions import JIRAError
from lib.base import BaseJiraAction

__all__ = [
    'ActionManager'
]


class ActionManager(BaseJiraAction):

    def run(self, action, **kwargs):
        try:
            return (True, getattr(self._client, action)(**kwargs))
        except JIRAError as e:
            return (False, str(e))
        except AttributeError as e:
            return (False, 'Action "%s" is not implemented' % action)
