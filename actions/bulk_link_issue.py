from lib.base import BaseJiraAction

__all__ = [
    'BulkLinkJiraIssueAction'
]


class BulkLinkJiraIssueAction(BaseJiraAction):

    def run(self, issue_key_list=None, target_issue=None, direction=None, link_type=None):
        if direction == 'outward':
            inward_issue_key = target_issue
            for outward_issue_key in issue_key_list:
                issue = self._client.create_issue_link(link_type, inward_issue_key,
                                                       outward_issue_key)
        if direction == 'inward':
            outward_issue_key = target_issue
            for inward_issue_key in issue_key_list:
                issue = self._client.create_issue_link(link_type, inward_issue_key,
                                                       outward_issue_key)
        return issue
