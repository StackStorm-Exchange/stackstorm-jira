from lib.base import BaseJiraAction
from lib.formatters import to_issue_dict

__all__ = [
    'UpdateFieldValue'
]


class UpdatePriority(BaseJiraAction):
    def run(self, issue_key, new_priority, notify):
        issue = self._client.issue(issue_key)
        issue.update(fields={priority: new_priority}, notify=notify)
        return to_issue_dict(issue)
