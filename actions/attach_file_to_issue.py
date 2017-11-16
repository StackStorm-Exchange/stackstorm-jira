from lib.base import BaseJiraAction

__all__ = [
    'AttachFileToJiraIssueAction'
]


class AttachFileToJiraIssueAction(BaseJiraAction):

    def run(self, issue_key, file_path, file_name=None):
        with open(file_path) as attach_file:
            if file_name == "":
                file_name = None 

            attachment = self._client.add_attachment(
                issue=issue_key, 
                attachment=attach_file,
                filename=file_name)
            
            result = {
                "issue": issue_key,
                "filename": attachment.filename,
                "size": attachment.size,
                "created_at": attachment.created
            }

            return result
            
        raise Exception("Failed attaching file %s to issue %s." % (file_path, issue_key))