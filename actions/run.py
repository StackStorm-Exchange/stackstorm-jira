from jira.exceptions import JIRAError
from lib.base import BaseJiraAction

__all__ = [
    'ActionManager'
]


class ActionManager(BaseJiraAction):

    def run(self, action, **kwargs):
        try:
            if action == 'transition_issue_by_name':
                action = 'transition_issue'
                kwargs['transition'] = self.transition_name_to_id(**kwargs)
                del kwargs['transition_name']
            return (True, getattr(self._client, action)(**kwargs))
        except JIRAError as e:
            return (False, str(e))
        except AttributeError as e:
            return (False, 'Action "%s" is not implemented' % action)

    def transition_name_to_id(self, issue, transition_name):
        transitions = self._client.transitions(issue)
        res = list(filter(lambda x: x.get("name") == transition_name,
                          transitions))
        if bool(res):
            return res[0].get("id")
        return None
