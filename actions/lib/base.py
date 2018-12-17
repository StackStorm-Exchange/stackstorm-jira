from jira import JIRA

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
        self.project = ""

    def _run(self, profile=None):
        if profile:
            self._client = self._get_client(profile)

    def _get_client(self, profile=None):

        profile = self._build_profile(profile)

        options = {'server': profile['url'], 'verify': profile['verify']}

        auth_method = profile['auth_method']

        if auth_method == 'oauth':
            rsa_cert_file = profile['rsa_cert_file']
            rsa_key_content = self._get_file_content(file_path=rsa_cert_file)

            oauth_creds = {
                'access_token': profile['oauth_token'],
                'access_token_secret': profile['oauth_secret'],
                'consumer_key': profile['consumer_key'],
                'key_cert': rsa_key_content
            }

            client = JIRA(options=options, oauth=oauth_creds)

        elif auth_method == 'basic':
            basic_creds = (profile['username'], profile['password'])
            client = JIRA(options=options, basic_auth=basic_creds)

        else:
            msg = ('You must set auth_method to either "oauth"',
                   'or "basic" your jira.yaml config file.')
            raise Exception(msg)

        return client

    def _build_profile(self, profile_name):
        config = self.config
        profile = {}

        profiles = config.pop('profiles',{})
        override_profile = profiles.get(profile_name,{})
        config.update(override_profile)

        return profile

    def _get_file_content(self, file_path):
        with open(file_path, 'r') as fp:
            content = fp.read()

        return content
