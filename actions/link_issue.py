from lib.base import BaseJiraAction

__all__ = [
    'LinkJiraIssueAction'
]


class LinkJiraIssueAction(BaseJiraAction):
    def run(self, inward_issue_key=None, outward_issue_key=None, link_type=None):
        issue = self._client.create_issue_link(link_type, inward_issue_key, outward_issue_key)
        return issue
