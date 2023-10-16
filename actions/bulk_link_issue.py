import threading
from threading import Semaphore
from lib.base import BaseJiraAction

class BulkLinkJiraIssueAction(BaseJiraAction):
    def link_issues(self,semaphore, issue_key=None, target_issue=None, direction=None, link_type=None):
        with semaphore:
            if direction == 'outward':
                outward_issue_key = issue_key
                inward_issue_key = target_issue
                response = self._client.create_issue_link(link_type, inward_issue_key,outward_issue_key)

            if direction == 'inward':
                inward_issue_key = issue_key
                outward_issue_key = target_issue
                response = self._client.create_issue_link(link_type, inward_issue_key,outward_issue_key)
            response_output = {"issue": target_issue, "response": response}
        print(response_output)

    def run(self, issue_key_list, target_issue, direction, link_type):
        threads = list()
        semaphore = Semaphore(10)
        for issue_key in issue_key_list:
            x = threading.Thread(target=self.link_issues, args=(semaphore, issue_key, target_issue, direction, link_type))
            threads.append(x)
            x.start()

        for thread in threads:
                thread.join()