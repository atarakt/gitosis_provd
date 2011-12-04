from configobj import ConfigObj

class GenerateGitosisConfigFile:
    def __init__(self):
        config_file          = 'repositories.conf'
        self.config          = ConfigObj(config_file)

    def _get_users(self, group):
        path = group.split('/')[0]
        if path == 'official' or path == 'private':
            users = ['@xivo-core-team']
            if self._get_extra_options().has_key(group):
                users.append(self._get_extra_options().get(group))
        else:
            users = self.config['groups'][group]
        return ' '.join(users)

    def _get_extra_options(self):
        return self.config['extra_options']
    
    def _get_repositories_names(self):
        result = {}
        for item in self.config['repositories'].iteritems():
            branch, repositories = item
            for data in repositories.iteritems():
                name, desc = data
                name = "%s/%s" % (branch, name)
                result[name] = desc
        return result

    def _create_skel(self):
        return ('[gitosis]\n')

    def _get_repositories(self, group_name):
        repositories = None if group_name == 'xivo-core-team' else group_name
        return repositories

    def _create_group(self, group):
        users = self._get_users(group)
        title    = '[group %s]\n' % group
        data     = self._get_repositories(group)
        writable = 'writable = %s\n' % data if data is not None else ''
        members  = 'members = %s\n'  % self._get_users(group)
        return title + writable + members + '\n'

    def _create_repository(self, repository):
        branch, repo = repository.split('/')
        title  = '[repo %s]\n' % repository
        owner  = 'owner = XiVO Dev Team\n'
        desc   = 'description = %s\n' % self.config['repositories'][branch][repo]
        gitweb = 'gitweb = yes\n' if branch == 'official' else ''
        daemon = 'daemon = yes\n' if branch == 'official' else ''
        return title + owner + desc + gitweb + daemon + '\n'

    def _create_config_file(self):
        config_file = open('gitosis.conf', 'w')
        config_file.write(self._create_skel())
        config_file.write(self._create_group('gitosis-admin'))
        config_file.write(self._create_group('xivo-core-team'))
        repositories = sorted(self._get_repositories_names().keys())
        for repository in repositories:
            config_file.write(self._create_group(repository))
            config_file.write(self._create_repository(repository))
        config_file.close()
