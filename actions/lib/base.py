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

    def _get_client(self, profile=None):
        config = self.config
        profile_name = profile

        default_profile = config.get('default_profile', None)

        if profile_name is None and default_profile is None:
            profile_name = "inline"
        elif profile_name is None and len(default_profile) > 0:
            profile_name = default_profile
        else:
            profile_name = profile

        profile = self._build_profile(profile_name)

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

        if profile_name == "inline".lower():
                profile['url'] = config.get('url')
                profile['verify'] = config.get('verify')
                profile['auth_method'] = config.get('auth_method')
                profile['rsa_cert_file'] = config.get('rsa_cert_file')
                profile['oauth_token'] = config.get('oauth_token')
                profile['oauth_secret'] = config.get('oauth_secret')
                profile['consumer_key'] = config.get('consumer_key')
                profile['username'] = config.get('username')
                profile['password'] = config.get('password')
                self.project = config.get("project")
        else:
            if 'profiles' in config and len(config['profiles']) > 0:
                for profile_cfg in config['profiles']:
                    if profile_cfg['name'].lower() == profile_name.lower():
                        profile['url'] = profile_cfg.get('url')
                        profile['verify'] = profile_cfg.get('verify')
                        profile['auth_method'] = profile_cfg.get('auth_method')
                        profile['rsa_cert_file'] = profile_cfg.get('rsa_cert_file')
                        profile['oauth_token'] = profile_cfg.get('oauth_token')
                        profile['oauth_secret'] = profile_cfg.get('oauth_secret')
                        profile['consumer_key'] = profile_cfg.get('consumer_key')
                        profile['username'] = profile_cfg.get('username')
                        profile['password'] = profile_cfg.get('password')
                        self.project = config.get("project")
                        break
            else:
                msg = ('No configuration file called: %s found. Please check',
                       'your config file' % profile)

        if len(profile.items()) == 0:
            msg = ('No configuration profile found. Please check your config',
                   'file for the profile you have specified.')
            raise Exception(msg)

        return profile

    def _get_file_content(self, file_path):
        with open(file_path, 'r') as fp:
            content = fp.read()

        return content
