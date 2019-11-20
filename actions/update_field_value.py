from lib.base import BaseJiraAction

__all__ = [
    'UpdateFieldValue'
]


class UpdateFieldValue(BaseJiraAction):
    def run(self, issue_key, field, value, notify):
        issue = self._client.issue(issue_key)
        issue.update(fields={field: value}, notify=notify)
        result = issue.fields.labels
        return result
