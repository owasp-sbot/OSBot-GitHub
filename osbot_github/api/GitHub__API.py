from os import getenv

import requests
from github import Github

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc                       import datetime_to_str
from osbot_utils.utils.Python_Logger              import logger_info
from osbot_utils.decorators.lists.group_by        import group_by
from osbot_utils.decorators.lists.index_by        import index_by
from osbot_utils.decorators.methods.cache_on_self import cache_on_self

GIT_HUB__ACCESS_TOKEN   = "GIT_HUB__ACCESS_TOKEN"
GIT_HUB__REPO_PATH      = 'https://raw.githubusercontent.com/'
GIT_HUB__DEFAULT_BRANCH = 'main'
GIT_HUB__DEFAULT_REPO   = 'owasp-sbot/OSBot-GitHub'


class GitHub__API:

    def __init__(self):     #, target_repo=None, target_branch=None):
        #self.target_repo    = target_repo   or GIT_HUB__DEFAULT_REPO
        #self.target_branch  = target_branch or GIT_HUB__DEFAULT_BRANCH
        self.log_info       = logger_info()
        self.session        = requests.Session()

    def access_token(self):
        return getenv(GIT_HUB__ACCESS_TOKEN)

    def file_download(self, repo, branch, file_path):
        download_url = f'{GIT_HUB__REPO_PATH}/{repo}/{branch}/{file_path}'
        pprint(download_url)
        headers  = {'Authorization'  : f'token {self.access_token()}',
                    'Accept-Encoding': 'gzip'}
        response = self.session.get(download_url, headers=headers)
        return response.text

    def github(self):
        return Github(self.access_token())

    @cache_on_self
    def organisation(self, user_name):
        return self.github().get_user(user_name)

    @cache_on_self
    def user(self, user_name):
        return self.github().get_user(user_name)

    def repos_from_user(self, user_name):
        return self.user(user_name).get_repos()

    def repos_from_organisation(self, org_name):
        return self.organisation(org_name).get_repos()
