import unittest
import os
from gitosis_prov import GenerateGitosisConfigFile

class TestGenerateGitosisConfigFile(unittest.TestCase):
    def setUp(self):
        config = GenerateGitosisConfigFile()
        self.config = GenerateGitosisConfigFile()

    def test_parse_extra(self):
        expected = {'official/xivo-skaro': 'extra_dev1 extra_dev2', 'private/hard-img': 'extra_dev1'}
        self.assertEqual(self.config._get_extra_options(), expected)

    def test_get_repositories_names(self):
        expected = {}
        expected['official/xivo-skaro']     = 'XiVO Skaro'
        expected['official/xivo-gallifrey'] = 'XiVO Gallifrey'
        expected['private/hard-img']        = 'Hardware img'
        expected['private/hard-code']       = 'Hardware code'
        result = self.config._get_repositories_names()
        self.assertEqual(result, expected)

    def test_get_core_team_users(self):
        expected = ['dev1', 'dev2']
        result   = self.config._get_core_team_users()
        self.assertEqual(result, expected)

    def test_get_core_team_user_repositories(self):
        expected = ['misc', 'extra']
        result   = self.config._get_core_team_user_repositories('dev1')
        self.assertEqual(result, expected)

    def test_get_people_repository(self):
        expected = 'people/dev1/misc'
        result = self.config._get_repositories('people/dev1/misc')
        self.assertEqual(result, expected)

    def test_create_skel(self):
        expected = '[gitosis]\n'
        self.assertEqual(self.config._create_skel(), expected)

    def test_get_admin_users(self):
        expected = 'admin1 admin2'
        result = self.config._get_users('gitosis-admin')
        self.assertEqual(result, expected)

    def test_get_core_team_user(self):
        expected = 'dev1 dev2'
        result = self.config._get_users('xivo-core-team')
        self.assertEqual(result, expected)

    def test_get_core_team_extra_data(self):
        expected = {'real_name': 'first dev', 'extra_repo': 'misc extra'}
        result = self.config._get_user_extra_data('dev1')
        self.assertEqual(result, expected)

    def test_create_admin_group(self):
        title    = '[group gitosis-admin]\n'
        writable = 'writable = gitosis-admin\n'
        members  = 'members = admin1 admin2\n'
        expected = title + writable + members + '\n'
        result   = self.config._create_group('gitosis-admin')
        self.assertEqual(result, expected)

    def test_create_core_team_group(self):
        title    = '[group xivo-core-team]\n'
        members  = 'members = dev1 dev2\n' 
        expected = title + members + '\n'
        result   = self.config._create_group('xivo-core-team')
        self.assertEqual(result, expected)

    def test_create_group_for_repository_with_two_extra_users(self):
        title    = '[group official/xivo-skaro]\n'
        writable = 'writable = official/xivo-skaro\n'
        members  = 'members = @xivo-core-team extra_dev1 extra_dev2\n' 
        expected = title + writable + members + '\n'
        result   = self.config._create_group('official/xivo-skaro')
        self.assertEqual(result, expected)

    def test_create_group_for_repository_with_one_extra_user(self):
        title    = '[group private/hard-img]\n'
        writable = 'writable = private/hard-img\n'
        members  = 'members = @xivo-core-team extra_dev1\n' 
        expected = title + writable + members + '\n'
        result   = self.config._create_group('private/hard-img')
        self.assertEqual(result, expected)

    def test_create_group_people(self):
        title    = '[group people/dev1/misc]\n'
        writable = 'writable = people/dev1/misc\n'
        members  = 'members = dev1\n' 
        expected = title + writable + members + '\n'
        result   = self.config._create_group('people/dev1/misc')
        self.assertEqual(result, expected)

    def test_create_official_repository(self):
        title    = '[repo official/xivo-skaro]\n'
        owner    = 'owner = XiVO Dev Team\n'
        desc     = 'description = XiVO Skaro\n'
        gitweb   = 'gitweb = yes\n'
        daemon   = 'daemon = yes\n'
        expected = title + owner + desc + gitweb + daemon + '\n'
        result   = self.config._create_repository('official/xivo-skaro')
        self.assertEqual(result, expected)

    def test_create_private_repository(self):
        title    = '[repo private/hard-img]\n'
        owner    = 'owner = XiVO Dev Team\n'
        desc     = 'description = Hardware img\n'
        expected = title + owner + desc + '\n'
        result   = self.config._create_repository('private/hard-img')
        self.assertEqual(result, expected)

    def test_create_people_repo(self):
        title = '[repo people/dev1/misc]\n'
        owner = 'owner = first dev\n'
        expected = title + owner + '\n'
        result   = self.config._create_repository('people/dev1/misc')
        self.assertEqual(result, expected)

    def test_write_config_file(self):
        if os.path.isfile('gitosis.conf'):
            os.remove('gitosis.conf')
        self.config._create_config_file()
        self.assertTrue(os.path.isfile('gitosis.conf'))

if __name__ == '__main__':
    unittest.main()
