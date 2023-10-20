from lib.base import BaseJiraAction
from lib.formatters import fmt_field_value, to_issue_dict

__all__ = [
    'UpdateFieldValue'
]


class UpdateFieldValue(BaseJiraAction):
    def run(self, issue_key, field, value, notify):
        issue = self._client.issue(issue_key)
        issue.update(
            fields={field: fmt_field_value(field, value)},
            notify=notify,
        )
        return to_issue_dict(issue)
