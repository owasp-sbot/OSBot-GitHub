import pytest
from unittest                           import TestCase

from dotenv import load_dotenv
from github import Github
from github.NamedUser import NamedUser
from github.Organization import Organization
from github.PaginatedList import PaginatedList
from github.Repository import Repository

from osbot_github.api.GitHub__API               import GitHub__API
from osbot_github.api.cache.GitHub__API__Cache  import GitHub__API__Cache
from osbot_github.dbs.Table__GitHub__Repos      import REPO__OSBOT_GIT_HUB
from osbot_github.utils.Version         import Version
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc             import list_set
from osbot_utils.utils.Objects import pickle_save_to_bytes, pickle_load_from_bytes
from tests.api.cache.test_GitHub__API__Cache import GIT_HUB__USER_NAME, GIT_HUB__ORG_NAME__OWASP_SBOT


class test_GitHub_API(TestCase):
    github_api      : GitHub__API
    test_file_path  : str

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.github_api = GitHub__API__Cache()
        #cls.github_api.disable()
        #cls.github_api.update()
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
        kwargs         = dict(repo=repo_full_name,branch=branch, file_path=self.test_file_path)
        assert '# An Markdown file' in self.github_api.file_download(**kwargs)

    def test_user(self):
        user_name   = GIT_HUB__USER_NAME
        user_1      = self.github_api.user(user_name=user_name)
        user_2      = self.github_api.user(user_name=user_name)
        user_3      = self.github_api.user(user_name=user_name)
        assert type(user_1) is NamedUser
        assert type(user_2) is NamedUser
        assert type(user_3) is NamedUser

    def test_organization(self):
        organization_name   = GIT_HUB__ORG_NAME__OWASP_SBOT
        organization_1      = self.github_api.organization(org_name=organization_name)
        organization_2      = self.github_api.organization(org_name=organization_name)
        organization_3      = self.github_api.organization(org_name=organization_name)
        assert type(organization_1) is Organization
        assert type(organization_2) is Organization
        assert type(organization_3) is Organization

    def test_repos_from_user(self):
        user_name  = GIT_HUB__USER_NAME
        repos      = self.github_api.repos_from_user(user_name=user_name)
        repo       = next(iter(repos), None)
        assert type(repos)      is list             #   PaginatedList
        assert type(repo )      is Repository
        assert repo.owner.login == user_name
        assert len(repos)       > 40

        pprint(f'there are {len(repos)} repos in user {user_name}')

    def test_repos_from_organization(self):
        org_name = GIT_HUB__ORG_NAME__OWASP_SBOT
        repos    = self.github_api.repos_from_organization(org_name=org_name)
        repo     = next(iter(repos), None)
        assert type(repos) is list               # PaginatedList
        assert type(repo ) is Repository
        assert len (repos) > 20
        pprint(f'there are {len(repos)} repos in organization {org_name}')



