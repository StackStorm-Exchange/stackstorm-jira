from lib.base import BaseJiraAction
from lib.formatters import to_comment_dict

__all__ = [
    'CommentJiraIssueAction'
]


class CommentJiraIssueAction(BaseJiraAction):

    def run(self, issue_key, comment_text, config_profile=None):

        if config_profile:
            self._client = self._get_client(config_profile)

        comment = self._client.add_comment(issue_key, comment_text)
        result = to_comment_dict(comment)
        return result
