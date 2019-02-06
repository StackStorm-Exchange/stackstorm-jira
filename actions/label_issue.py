from lib.base import BaseJiraAction

__all__ = [
    'AddLabelJiraIssue'
]


class AddLabelJiraIssue(BaseJiraAction):
    def run(self, issue_key, label_text):
        issue = self._client.issue(issue_key)
        issue.add_field_value("labels", label_text)
        result = issue.fields.labels
        return result
