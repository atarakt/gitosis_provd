from configobj import ConfigObj

class GenerateGitosisConfigFile:
    def _get_data(self):
        config_file = 'repositories.conf'
        config = ConfigObj(config_file)
        return config


