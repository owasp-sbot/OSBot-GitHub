from dotenv                                                     import load_dotenv
from osbot_github.api.GitHub__API                               import GitHub__API
from osbot_utils.helpers.sqlite.domains.Sqlite__Cache__Requests import Sqlite__Cache__Requests

SQLITE_DB_NAME__GIT_HUB_API_CACHE = 'github_api_cache.sqlite'
SQLITE_TABLE__BEDROCK_REQUESTS    = 'github_api_requests'

class GitHub__API__Cache(Sqlite__Cache__Requests, GitHub__API):
    db_name         : str   = SQLITE_DB_NAME__GIT_HUB_API_CACHE
    table_name      : str   = SQLITE_TABLE__BEDROCK_REQUESTS
    pickle_response : bool  = True

    def __init__(self, db_path=None):
        load_dotenv()
        super().__init__(db_path=db_path, db_name=self.db_name, table_name=self.table_name)
        GitHub__API.__init__(self)

    def file_download(self, **kwargs):
        return self.invoke(super().file_download, kwargs)

    def user(self, **kwargs):
        return self.invoke(super().user, kwargs)

    def organization(self, **kwargs):
        return self.invoke(super().organization, kwargs)

    def repo(self, **kwargs):
        return self.invoke(super().repo, kwargs)

    def repos_from_user(self, **kwargs):
        def target(**target_kwargs):
            user      = self.user(**target_kwargs)
            all_repos = list(user.get_repos())
            return all_repos

        request_data = dict(target='repos_from_user', kwargs=kwargs)

        return self.invoke_with_cache(target, kwargs, request_data)

    def repos_from_organization(self, **kwargs):
        def target(**target_kwargs):
            organization = self.organization(**target_kwargs)
            all_repos    = list(organization.get_repos())
            return all_repos

        request_data = dict(target='repos_from_organization', kwargs=kwargs)
        return self.invoke_with_cache(target, kwargs, request_data)