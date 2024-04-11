import pytest
from unittest                           import TestCase

from dotenv import load_dotenv
from github import Github
from github.PaginatedList import PaginatedList
from github.Repository import Repository

from osbot_github.api.GitHub__API       import GitHub__API
from osbot_github.dbs.Table__GitHub__Repos import REPO__OSBOT_GIT_HUB
from osbot_github.utils.Version         import Version
from osbot_utils.utils.Misc             import list_set

class test_GitHub_API(TestCase):
    github_api      : GitHub__API
    test_file_path  : str

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.github_api = GitHub__API()
        cls.test_file_path = 'docs/test_files/an_markdown_file.md'

    # def test__init__(self):
    #     assert self.github_api.target_repo == 'owasp-sbot/OSBot-GitHub'
    #     assert self.github_api.target_branch == 'dev'

    def test_access_token(self):
        assert self.github_api.access_token() is not None
        assert len(self.github_api.access_token()) > 10



    def test_file_download(self):
        repo_full_name = REPO__OSBOT_GIT_HUB
        branch         = 'dev'
        assert '# An Markdown file' in self.github_api.file_download(repo_full_name,branch, self.test_file_path)












    def test_repos_from_user(self):
        user_name = 'DinisCruz'
        repos = self.github_api.repos_from_user(user_name)
        repo  = next(iter(repos), None)
        assert type(repos) is PaginatedList
        assert type(repo ) is Repository
        assert repo.owner.login == user_name

    def test_repos_from_organisation(self):
        org_name = 'owasp-sbot'
        repos = self.github_api.repos_from_organisation(org_name)
        repo  = next(iter(repos), None)
        assert type(repos) is PaginatedList
        assert type(repo ) is Repository
        assert repo.organization.login == org_name



