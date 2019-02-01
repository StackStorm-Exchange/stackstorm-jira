import yaml

from st2tests.base import BaseActionTestCase

__all__ = [
    'JIRABaseActionTestCase',
]


class JIRABaseActionTestCase(BaseActionTestCase):
    __test__ = False

    def setUp(self):
        super(JIRABaseActionTestCase, self).setUp()

        self.full_auth_passwd_config = self.load_yaml('full_auth_passwd.yaml')
        self.blank_config = self.load_yaml('blank.yaml')

    def load_yaml(self, filename):
        return yaml.safe_load(self.get_fixture_content(filename))
