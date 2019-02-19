from lib.base import BaseJiraAction

__all__ = [
    'AttachFileToJiraIssueAction'
]


class AttachFileToJiraIssueAction(BaseJiraAction):

    def run(self, issue_key, file_path, file_name=None, config_profile=None):

        super(AttachFileToJiraIssueAction, self)._run(config_profile)

        if not file_name:
            file_name = None

        with open(file_path, 'rb') as fp:
            attachment = self._client.add_attachment(
                issue=issue_key,
                attachment=fp,
                filename=file_name)

        result = {
            "issue": issue_key,
            "filename": attachment.filename,
            "size": attachment.size,
            "created_at": attachment.created
        }

        return result
