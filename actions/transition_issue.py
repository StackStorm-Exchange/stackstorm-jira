from lib.base import BaseJiraAction

__all__ = [
    'TransitionJiraIssueAction'
]


class TransitionJiraIssueAction(BaseJiraAction):

    def run(self, issue_key, transition, config_profile=None):
        
        if config_profile:
            self._client = self._get_client(config_profile)

        result = self._client.transition_issue(issue_key, transition)
        return result
