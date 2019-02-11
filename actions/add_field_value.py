from lib.base import BaseJiraAction

__all__ = [
    'AddFieldValue'
]


class AddFieldValue(BaseJiraAction):
    def run(self, issue_key, field, value):
        issue = self._client.issue(issue_key)
        issue.add_field_value(field, value)
        result = issue.fields.labels
        return result
