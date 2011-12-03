import unittest
from gitosis_prov import GenerateGitosisConfigFile

class TestGenerateGitosisConfigFile(unittest.TestCase):
    def setUp(self):
        config = GenerateGitosisConfigFile()
        self.result = config._get_data()

    def test_parse_officials_repo(self):
        expected = ['xivo-skaro', 'xivo-gallifrey']
        self.assertEqual(self.result['repositories']['officials'], expected)

    def test_parse_privates_repo(self):
        expected = ['hard-img', 'hard-code']
        self.assertEqual(self.result['repositories']['privates'], expected)

    def test_parse_dev(self):
        expected = ['dev1', 'dev2']
        self.assertEqual(self.result['xivo_team']['xivo'], expected)

    def test_parse_extra(self):
        expected = {'hard-img': 'extra_dev1', 'xivo-skaro': 'extra_dev2'}
        self.assertEqual(self.result['extra'], expected)



if __name__ == '__main__':
    unittest.main()

