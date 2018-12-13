from lib.base import BaseJiraAction
from lib.formatters import to_attachment_dict

__all__ = [
    'GetJiraIssueAttachmentsAction'
]


class GetJiraIssueAttachmentsAction(BaseJiraAction):
    def run(self, issue_key,config_profile=None):

        if config_profile:
            self._client = self._get_client(config_profile)

        issue = self._client.issue(issue_key)

        result = []

        for attachment in issue.fields.attachment:
            item = to_attachment_dict(attachment)
            result.append(item)

        return result
