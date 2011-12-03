import unittest
from gitosis_prov import GenerateGitosisConfigFile

class TestGenerateGitosisConfigFile(unittest.TestCase):
    def setUp(self):
        config = GenerateGitosisConfigFile()
        self.config = GenerateGitosisConfigFile()

    def test_parse_officials_repo(self):
        expected = ['xivo-skaro', 'xivo-gallifrey']
        self.assertEqual(self.config._get_officials_repo(), expected)

    def test_parse_privates_repo(self):
        expected = ['hard-img', 'hard-code']
        self.assertEqual(self.config._get_privates_repo(), expected)

    def test_parse_dev(self):
        expected = ['dev1', 'dev2']
        self.assertEqual(self.config._get_team(), expected)

    def test_parse_extra(self):
        expected = {'hard-img': 'extra_dev1', 'xivo-skaro': 'extra_dev2'}
        self.assertEqual(self.config._get_extra_data(), expected)

    def test_create_skel(self):
        expected = "[gitosis]\ngitweb = no\ndaemon = no\n"
        self.assertEqual(self.config._create_skel(), expected)

if __name__ == '__main__':
    unittest.main()

