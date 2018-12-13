from lib.base import BaseJiraAction
from lib.formatters import to_comment_dict

__all__ = [
    'GetJiraIssueCommentsAction'
]


class GetJiraIssueCommentsAction(BaseJiraAction):
    def run(self, issue_key, config_profile=None):

        if config_profile:
            self._client = self._get_client(config_profile)

        issue = self._client.issue(issue_key)

        result = []

        for comment in issue.fields.comment.comments:
            item = to_comment_dict(comment)
            result.append(item)

        return result
