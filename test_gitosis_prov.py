import unittest
import os
from gitosis_prov import GenerateGitosisConfigFile

class TestGenerateGitosisConfigFile(unittest.TestCase):
    def setUp(self):
        config = GenerateGitosisConfigFile()
        self.config = GenerateGitosisConfigFile()

    def test_parse_officials_repo(self):
        expected = {'xivo-skaro': 'XiVO Skaro', 'xivo-gallifrey': 'XiVO Gallifrey'}
        self.assertEqual(self.config._get_officials_repo(), expected)

    def test_parse_privates_repo(self):
        expected = {'hard-img': 'Hardware img', 'hard-code': 'Hardware code'}
        self.assertEqual(self.config._get_privates_repo(), expected)

    def test_get_group(self):
        expected = ['gitosis-admin', ['admin1', 'admin2']]
        self.assertEqual(self.config._get_group('gitosis-admin'), expected)

    def test_parse_extra(self):
        expected = {'hard-img': 'extra_dev1', 'xivo-skaro': 'extra_dev2'}
        self.assertEqual(self.config._get_extra_data(), expected)

    def test_create_skel(self):
        expected = '[gitosis]\n'
        self.assertEqual(self.config._create_skel(), expected)

    def test_create_admin_group(self):
        expected = '[group gitosis-admin]\nwritable = gitosis-admin\nmembers = admin1, admin2\n\n'
        self.assertEqual(self.config._create_group('gitosis-admin'), expected)

    def test_create_official_repository(self):
        expected = '[repo official/xivo-skaro]\nowner = XiVO Dev Team\ndescription = XiVO Skaro\ngitweb = yes\ndaemon = yes\n'
        self.assertEqual(self.config._create_repository('official/xivo-skaro'), expected)

    def test_create_private_repository(self):
        expected = '[repo private/hard-img]\nowner = XiVO Dev Team\ndescription = Hardware img\n'
        self.assertEqual(self.config._create_repository('private/hard-img'), expected)

    def test_write_config_file(self):
        os.remove('gitosis.conf')
        self.config._create_config_file()
        self.assertTrue(os.path.isfile('gitosis.conf'))

if __name__ == '__main__':
    unittest.main()

