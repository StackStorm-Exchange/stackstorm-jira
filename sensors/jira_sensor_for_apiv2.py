# See ./requirements.txt for requirements.
import os
import base64

from patched_search import JIRA

from st2reactor.sensor.base import PollingSensor


class JIRASensorForAPIv2(PollingSensor):
    '''
    Sensor will monitor for any new projects created in JIRA and
    emit trigger instance when one is created.
    '''
    def __init__(self, sensor_service, config=None, poll_interval=5):
        super(JIRASensorForAPIv2, self).__init__(sensor_service=sensor_service,
                                                 config=config,
                                                 poll_interval=poll_interval)

        self._jira_url = None
        # The Consumer Key created while setting up the "Incoming Authentication" in
        # JIRA for the Application Link.
        self._consumer_key = u''
        self._rsa_key = None
        self._jira_client = None
        self._access_token = u''
        self._access_secret = u''
        self._projects_available = None
        self._poll_interval = 30
        self._project = None
        self._latest_id = None
        self._jql_query = None
        self._trigger_name = 'issues_tracker_for_apiv2'
        self._trigger_pack = 'jira'
        self._trigger_ref = '.'.join([self._trigger_pack, self._trigger_name])

    def _read_cert(self, file_path):
        with open(file_path) as f:
            return f.read()

    def setup(self):
        self._jira_url = self._config['url']
        auth_method = self._config['auth_method']

        if auth_method == 'oauth':
            rsa_cert_file = self._config['rsa_cert_file']
            if not os.path.exists(rsa_cert_file):
                raise Exception('Cert file for JIRA OAuth not found at %s.' % rsa_cert_file)
            self._rsa_key = self._read_cert(rsa_cert_file)
            self._poll_interval = self._config.get('poll_interval', self._poll_interval)
            oauth_creds = {
                'access_token': self._config['oauth_token'],
                'access_token_secret': self._config['oauth_secret'],
                'consumer_key': self._config['consumer_key'],
                'key_cert': self._rsa_key
            }

            self._jira_client = JIRA(options={'server': self._jira_url},
                                     oauth=oauth_creds)
        elif auth_method == 'basic':
            basic_creds = (self._config['username'], self._config['password'])
            self._jira_client = JIRA(options={'server': self._jira_url},
                                     basic_auth=basic_creds)

        elif auth_method == 'pat':
            headers = JIRA.DEFAULT_OPTIONS["headers"].copy()
            headers["Authorization"] = f"Bearer {self._config['token']}"
            self._jira_client = JIRA(server=self._jira_url, options={"headers": headers})

        elif auth_method == 'cookie':
            basic_creds = (self._config['username'], self._config['password'])
            self._jira_client = JIRA(server=self._jira_url, auth=basic_creds)

        elif auth_method == 'api_token':
            headers = JIRA.DEFAULT_OPTIONS["headers"].copy()
            b64_header = base64.b64encode(f"{self._config['username']}:{self._config['token']}"
                                          .encode())
            headers["Authorization"] = f"Basic {b64_header.decode()}"
            self._jira_client = JIRA(server=self._jira_url, options={"headers": headers})

        else:
            msg = ('You must set auth_method to either "oauth", ',
                   '"basic", "pat", "api_token", or "cookie" in your Jira pack config file.')
            raise Exception(msg)

        if self._projects_available is None:
            self._projects_available = set()
            for proj in self._jira_client.projects():
                self._projects_available.add(proj.key)
        self._project = self._config.get('project', None)
        if not self._project or self._project not in self._projects_available:
            raise Exception('Invalid project (%s) to track.' % self._project)

        self._jql_query = 'project={} ORDER BY id DESC'.format(self._project)
        latest_issue = self._jira_client.search_issues(self._jql_query, maxResults=1)
        if latest_issue:
            self._latest_id = int(latest_issue[0].id)
        self._update_jql(self._latest_id)

    def poll(self):
        self._detect_new_issues()

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _update_jql(self, latest_id=None):
        jql = 'project={}'.format(self._project)
        if latest_id:
            jql = '{} AND id > {}'.format(jql, latest_id)
        self._jql_query = '{} ORDER BY id ASC'.format(jql)

    def _detect_new_issues(self):
        new_issues = self._jira_client.search_issues(self._jql_query, maxResults=50, startAt=0)
        for issue in new_issues:
            self._latest_id = int(issue.id)
            self._dispatch_issues_trigger(issue)
        self._update_jql(self._latest_id)

    def _dispatch_issues_trigger(self, issue):
        trigger = self._trigger_ref
        payload = {}
        payload['project'] = self._project
        payload['id'] = issue.id
        payload['expand'] = issue.raw.get('expand', '')
        payload['issue_key'] = issue.key
        payload['issue_url'] = issue.self
        payload['issue_browse_url'] = self._jira_url + '/browse/' + issue.key
        payload['fields'] = issue.raw.get('fields', {})
        self._sensor_service.dispatch(trigger, payload)
