from lib.base import BaseJiraAction

__all__ = [
    'TransitionJiraIssueAction'
]


class TransitionJiraIssueAction(BaseJiraAction):

    def run(self, issue_key, transition, fields):
        result = self._client.transition_issue(issue_key, transition, fields=fields)
        return result
