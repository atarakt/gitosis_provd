from configobj import ConfigObj

class GenerateGitosisConfigFile:
    def __init__(self):
        config_file = 'repositories.conf'
        self.config = ConfigObj(config_file)

    def _get_users(self, group):
        path = group.split('/')[0]
        if path == 'people':
            users = group.split('/')[1]
            return users
        if path == 'official' or path == 'private':
            users = ['@xivo-core-team']
            if self._get_extra_options().has_key(group):
                extra_users = self._get_extra_options().get(group)
                users.append(extra_users)
            users = ' '.join(users)
        else:
            users = self.config['groups'][group]
            if isinstance(users, dict):
                users = ' '.join(users.keys())
        return users

    def _get_core_team_users(self):
        users = self._get_users('xivo-core-team').split(' ')
        return users

    def _get_user_extra_data(self, user):
        users = self.config['groups']['xivo-core-team']
        return users.get(user)

    def _get_extra_options(self):
        return self.config['extra_options']
    
    def _get_core_team_user_repositories(self, user):
        data = self._get_user_extra_data(user).get('extra_repo')
        return data.split(' ')

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
        branch, repo = repository.split('/', 1)
        title  = '[repo %s]\n' % repository
        if branch == 'people':
            owner, desc = self._get_people_data(repo)
        else:
            owner, desc = self._get_team_data(branch, repo)
        gitweb = 'gitweb = yes\n' if branch == 'official' else ''
        daemon = 'daemon = yes\n' if branch == 'official' else ''
        return title + owner + desc + gitweb + daemon + '\n'

    def _get_team_data(self, branch, repo):
        owner  = 'owner = XiVO Dev Team\n'
        desc   = 'description = %s\n' % self.config['repositories'][branch][repo]
        return owner, desc

    def _get_people_data(self, repo):
        user, extra = repo.split('/')
        data   = self._get_user_extra_data(user).get('real_name')
        owner  = 'owner = ' + data + '\n'
        desc   = ''
        return owner, desc

    def _create_config_file(self):
        config_file = open('gitosis.conf', 'w')
        config_file.write(self._create_skel())
        config_file.write(self._create_group('gitosis-admin'))
        config_file.write(self._create_group('xivo-core-team'))
        repositories = sorted(self._get_repositories_names().keys())
        for repository in repositories:
            self.create_global_repository(config_file, repository)
        for user in self._get_core_team_users():
            for repository in self._get_core_team_user_repositories(user):
                self.create_people_repository(user, repository, config_file)
        config_file.close()

    def create_global_repository(self, config_file, repository):
        config_file.write(self._create_group(repository))
        config_file.write(self._create_repository(repository))

    def create_people_repository(self, user, repository, config_file):
        data = 'people/%s/%s' % (user, repository)
        config_file.write(self._create_group(data))
        config_file.write(self._create_repository(data))
