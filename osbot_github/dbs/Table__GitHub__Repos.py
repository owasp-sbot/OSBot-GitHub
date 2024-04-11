from osbot_github.api.GitHub__API import GitHub__API
from osbot_github.dbs.Sqlite__GitHub import Sqlite__GitHub, SQLITE_TABLE__REPOS
from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self

REPO__OSBOT_GIT_HUB   = 'owasp-sbot/OSBot-GitHub'

class Table__GitHub__Repos(Kwargs_To_Self):
    sqlite__github  : Sqlite__GitHub
    github_api      : GitHub__API

    def __init__(self):
        super().__init__()
        self.github_api.target_repo = REPO__OSBOT_GIT_HUB

    def table(self):
        return self.sqlite__github.table(SQLITE_TABLE__REPOS)

    # def raw_github_repos(self):
    #     return self.github_api.repo()