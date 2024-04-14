from osbot_github.api.GitHub__API import GitHub__API


class Sqlite__GitHub__Load_Data:

    def __init__(self):
        self.github_api = GitHub__API()

    #def create_database_for_user(self):
    def load_repos_for_user(self, sqlite_db, table_name, user_name):
        user_repos = self.github_api.repos_from_user(user_name)
        return len(user_repos)