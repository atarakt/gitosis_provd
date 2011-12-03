from configobj import ConfigObj

class GenerateGitosisConfigFile:
    def __init__(self):
        config_file          = 'repositories.conf'
        self.config          = ConfigObj(config_file)

    def _get_officials_repo(self):
        return self.config['repositories']['official']

    def _get_privates_repo(self):
        return self.config['repositories']['private']

    def _get_group(self, group):
        return [group, self.config['groups'][group]]

    def _get_extra_data(self):
        return self.config['extra_data']
    
    def _create_skel(self):
        return ('[gitosis]\n')

    def _create_group(self, group):
        group_name, users = self._get_group(group)
        description = '[group %s]\n' % group_name
        writable = 'writable = %s\n' % group_name
        members = 'members = %s\n'  % ', '.join(users)
        return ('%s%s%s\n' % (description, writable, members))

    def _create_repository(self, repository):
        '''If repository is official, it will be browsable by anyone'''
        branch, repo = repository.split('/')
        title = '[repo %s]\n' % repository
        owner = 'owner = XiVO Dev Team\n'
        desc = 'description = %s\n' % self.config['repositories'][branch][repo]
        gitweb = 'gitweb = yes\n' if branch == 'official' else ''
        daemon = 'daemon = yes\n' if branch == 'official' else ''
        return title + owner + desc + gitweb + daemon

    def _create_config_file(self):
        config_file = open('gitosis.conf', 'w')
        config_file.write(self._create_skel())
        config_file.write(self._create_group('gitosis-admin'))
        config_file.close()
