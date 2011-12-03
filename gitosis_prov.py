from configobj import ConfigObj

class GenerateGitosisConfigFile:
    def __init__(self):
        self.repo            = 'gitosis'
        self.web_default     = 'no'
        self.daemon_default  = 'no'
        config_file          = 'repositories.conf'
        self.config          = ConfigObj(config_file)

    def _get_officials_repo(self):
        return self.config['repositories']['officials']

    def _get_privates_repo(self):
        return self.config['repositories']['privates']

    def _get_team(self):
        return self.config['xivo_team']['xivo']

    def _get_extra_data(self):
        return self.config['extra_data']
    
    def _create_skel(self):
        repo   = "[%s]" % self.repo
        web    = "gitweb = %s"    % self.web_default
        daemon = "daemon = %s" % self.daemon_default
        return ("%s\n%s\n%s\n" % (repo, web, daemon))

