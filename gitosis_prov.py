from configobj import ConfigObj

class GenerateGitosisConfigFile:
    def __init__(self):
        config_file = 'repositories.conf'
        self.config = ConfigObj(config_file)

    def _get_officials_repo(self):
        return self.config['repositories']['officials']

    def _get_privates_repo(self):
        return self.config['repositories']['privates']

    def _get_team(self):
        return self.config['xivo_team']['xivo']

    def _get_extra_data(self):
        return self.config['extra_data']
