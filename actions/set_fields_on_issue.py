from lib.base import BaseJiraAction


__all__ = [
    'SetFieldsForIssueAction'
]


class SetFieldsForIssueAction(BaseJiraAction):

    def run(self, issue, assignee=None, status=None,
            fix_version=None, labels=None, components=None):

        fields = {}

        if assignee:
            fields['assignee'] = assignee

        if status:
            fields['status'] = status

        if fix_version:
            fields['fix_version'] = fix_version

        update_items = {}

        if labels:
            update_items.update({'labels': labels})

        if components:
            update_items.update({'components': components})

        issue = self._client.issue(issue)
        issue.update(fields=fields, update=update_items)

        return (True, 'Updated issue %s' % issue)
