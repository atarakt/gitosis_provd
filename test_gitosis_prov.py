import unittest
import os
from gitosis_prov import GenerateGitosisConfigFile

class TestGenerateGitosisConfigFile(unittest.TestCase):
    def setUp(self):
        config = GenerateGitosisConfigFile()
        self.config = GenerateGitosisConfigFile()

    def test_parse_extra(self):
        expected = {'official/xivo-skaro': 'extra_dev1'}
        self.assertEqual(self.config._get_extra_options(), expected)

    def test_repositories_names(self):
        expected = {}
        expected['official/xivo-skaro']     = 'XiVO Skaro'
        expected['official/xivo-gallifrey'] = 'XiVO Gallifrey'
        expected['private/hard-img']        = 'Hardware img'
        expected['private/hard-code']       = 'Hardware code'
        result = self.config._get_repositories_names()
        self.assertEqual(result, expected)

    def test_create_skel(self):
        expected = '[gitosis]\n'
        self.assertEqual(self.config._create_skel(), expected)

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

    def test_create_group_for_repository(self):
        title    = '[group official/xivo-skaro]\n'
        writable = 'writable = official/xivo-skaro\n'
        members  = 'members = @xivo-core-team extra_dev1\n' 
        expected = title + writable + members + '\n'
        result   = self.config._create_group('official/xivo-skaro')
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

    def test_write_config_file(self):
        os.remove('gitosis.conf')
        self.config._create_config_file()
        self.assertTrue(os.path.isfile('gitosis.conf'))

if __name__ == '__main__':
    unittest.main()
