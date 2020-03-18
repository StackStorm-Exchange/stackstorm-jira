from lib.base import BaseJiraAction

__all__ = [
    'UpdateReporterValue'
]


class UpdateReporterValue(BaseJiraAction):
    def run(self, issue_key, username, notify):
        issue = self._client.issue(issue_key)
        issue.update(reporter={'name': username}, notify=notify)
        result = issue.fields.labels
        return result
