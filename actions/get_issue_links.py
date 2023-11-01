from lib.base import BaseJiraAction
from lib.formatters import to_links_dict

__all__ = [
    'GetJiraIssueLinksAction'
]


class GetJiraIssueLinksAction(BaseJiraAction):
    def run(self, issue_key):
        issue = self._client.issue(issue_key)

        result = [to_links_dict(i) for i in issue.fields.issuelinks]
        return result
