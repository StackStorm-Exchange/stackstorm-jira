from lib.base import BaseJiraAction
from lib.formatters import to_issue_dict

__all__ = [
    'SearchJiraIssuesAction'
]


class SearchJiraIssuesAction(BaseJiraAction):
    def run(self, query, start_at=0, max_results=50,
            include_comments=False, include_attachments=False,
            include_customfields=False):
        issues = self._client.search_issues(query, startAt=start_at,
                                            maxResults=max_results)
        results = []

        for issue in issues:
            results.append(to_issue_dict(issue=issue,
                           include_comments=include_comments,
                           include_attachments=include_attachments,
                           include_customfields=include_customfields))

        return results
