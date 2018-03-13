from lib.base import BaseJiraAction
from lib.formatters import to_issue_dict

__all__ = [
    'GetJiraIssueAction'
]


class GetJiraIssueAction(BaseJiraAction):
    def run(self, issue_key, include_comments=False, include_attachments=False,
            include_customfields=False):
        issue = self._client.issue(issue_key)
        result = to_issue_dict(issue=issue, include_comments=include_comments,
                               include_attachments=include_attachments,
                               include_customfields=include_customfields)
        return result
