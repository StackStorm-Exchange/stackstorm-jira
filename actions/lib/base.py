from patched_search import JIRA
import base64

#  from st2common.runners.base_action import Action
__all__ = [
    'BaseJiraAction'
]


class Action(object):
    def __init__(self, config):
        self.config = config


class BaseJiraAction(Action):
    def __init__(self, config):
        super(BaseJiraAction, self).__init__(config=config)
        self._client = self._get_client()

    def _get_client(self):
        config = self.config

        options = {'server': config['url'], 'verify': config['verify']}

        auth_method = config['auth_method']

        if auth_method == 'oauth':
            rsa_cert_file = config['rsa_cert_file']
            rsa_key_content = self._get_file_content(file_path=rsa_cert_file)

            oauth_creds = {
                'access_token': config['oauth_token'],
                'access_token_secret': config['oauth_secret'],
                'consumer_key': config['consumer_key'],
                'key_cert': rsa_key_content
            }

            client = JIRA(options=options, oauth=oauth_creds)

        elif auth_method == 'basic':
            basic_creds = (config['username'], config['password'])
            client = JIRA(options=options, basic_auth=basic_creds,
                          validate=config.get('validate', False))

        elif auth_method == 'pat':
            headers = JIRA.DEFAULT_OPTIONS["headers"].copy()
            headers["Authorization"] = f"Bearer {config['token']}"
            client = JIRA(server=config['url'], options={"headers": headers})

        elif auth_method == 'cookie':
            basic_creds = (config['username'], config['password'])
            client = JIRA(options=options, auth=basic_creds)

        elif auth_method == 'api_token':
            headers = JIRA.DEFAULT_OPTIONS["headers"].copy()
            b64_header = base64.b64encode(f"{config['username']}:{config['token']}".encode())
            headers["Authorization"] = f"Basic {b64_header.decode()}"
            client = JIRA(server=config['url'], options={"headers": headers})

        else:
            msg = ('You must set auth_method to either "oauth", ',
                   '"basic", "pat", "api_token", or "cookie" in your Jira pack config file.')
            raise Exception(msg)

        return client

    def _get_file_content(self, file_path):
        with open(file_path, 'r') as fp:
            content = fp.read()

        return content
