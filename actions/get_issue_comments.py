from lib.base import BaseJiraAction
from lib.formatters import to_comment_dict

__all__ = [
    'GetJiraIssueCommentsAction'
]


class GetJiraIssueCommentsAction(BaseJiraAction):
    def run(self, issue_key):
        issue = self._client.issue(issue_key)

        result = []

        for comment in issue.fields.comment.comments:
            item = to_comment_dict(comment)
            result.append(item)

        return result
