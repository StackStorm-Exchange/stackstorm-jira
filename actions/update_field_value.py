from lib.base import BaseJiraAction
from lib.formatters import to_issue_dict

__all__ = [
    'UpdateFieldValue'
]


class UpdateFieldValue(BaseJiraAction):
    def run(self, issue_key, field, value, notify):
        issue = self._client.issue(issue_key)
        if field == "labels":
            value = value.split()
        issue.update(fields={field: value}, notify=notify)
        return to_issue_dict(issue)
