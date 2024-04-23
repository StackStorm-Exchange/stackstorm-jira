from lib.base import BaseJiraAction
from lib.formatters import to_issue_dict

__all__ = [
    'GetJiraIssueAction'
]


class GetJiraIssueAction(BaseJiraAction):
    def run(self, issue_key, include_comments=False, include_attachments=False,
            include_customfields=False, include_components=False, include_subtasks=False,
            include_links=False, sanitize_formatting=False):
        issue = self._client.issue(issue_key)
        result = to_issue_dict(issue=issue, include_comments=include_comments,
                               include_attachments=include_attachments,
                               include_customfields=include_customfields,
                               include_components=include_components,
                               include_subtasks=include_subtasks,
                               include_links=include_links)

        def strip_braces(data):
            if isinstance(data, dict):
                return {k: strip_braces(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [strip_braces(element) for element in data]
            elif isinstance(data, str):
                return data.replace("{{", "").replace("}}", "")
            else:
                return data

        if sanitize_formatting:
            return strip_braces(result)
        else:
            return result
