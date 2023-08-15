from lib.base import BaseJiraAction
from lib.formatters import to_issue_dict

__all__ = [
    'AddFieldValue'
]


class AddFieldValue(BaseJiraAction):
    def run(self, issue_key, field, value):
        issue = self._client.issue(issue_key)
        issue.add_field_value(field, value)
        return to_issue_dict(issue)
