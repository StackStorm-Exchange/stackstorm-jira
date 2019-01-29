from lib.base import BaseJiraAction

__all__ = [
    'AssignJiraIssueAction'
]


class AssignJiraIssueAction(BaseJiraAction):

    def run(self, issue_key, assignee_name):
        result = self._client.assign_issue(issue_key, assignee_name)
        return result
