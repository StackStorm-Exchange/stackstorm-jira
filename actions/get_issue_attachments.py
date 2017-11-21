from lib.base import BaseJiraAction
from lib.formatters import to_attachment_dict

__all__ = [
    'GetJiraIssueAttachmentsAction'
]


class GetJiraIssueAttachmentsAction(BaseJiraAction):
    def run(self, issue_key):
        issue = self._client.issue(issue_key)

        result = []

        for attachment in issue.fields.attachment:
            item = to_attachment_dict(attachment)
            result.append(item)

        return result
