from os import environ

from osbot_github.api.GitHub__API import GitHub__API
from osbot_github.schemas.Schema__Repo import Schema__Repo
from osbot_github.schemas.Schema__Repos import Schema__Repos
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.helpers.sqlite.Sqlite__Database    import Sqlite__Database
from osbot_utils.utils.Files                        import current_temp_folder, path_combine, folder_create

DB_NAME__GIT_HUB          = 'github.sqlite'
ENV_NAME_PATH_LOCAL_DBS   = 'PATH_LOCAL_DBS'
FOLDER_NAME__GIT_HUB_DBS  = 'github_dbs'
SQLITE_TABLE__REPOS       = 'repos'


class Sqlite__GitHub(Sqlite__Database):

    github_api : GitHub__API

    def __init__(self):
        super().__init__(db_path=self.path_sqlite_github())
        self.setup()

    def path_db_folder(self):
        return environ.get(ENV_NAME_PATH_LOCAL_DBS) or current_temp_folder()

    def path_github_dbs(self):
        return path_combine(self.path_db_folder(), FOLDER_NAME__GIT_HUB_DBS)

    def path_sqlite_github(self):
        return path_combine(self.path_github_dbs(), DB_NAME__GIT_HUB)

    def setup(self):
        folder_create(self.path_db_folder())
        folder_create(self.path_github_dbs())
        self.table_repos__create()
        return self

    @cache_on_self
    def table_repos(self):
        return self.table(SQLITE_TABLE__REPOS)

    def table_repos__create(self):
        with self.table_repos() as _:
            _.row_schema = Schema__Repo                        # set the table row's schema
            if _.exists() is False:
                _.create()                                          # create if it doesn't exist
                return True
        return False


