from dotenv                                         import load_dotenv
from github.NamedUser                               import NamedUser
from github.Organization                            import Organization
from github.PaginatedList                           import PaginatedList
from github.Repository                              import Repository
from osbot_github.api.GitHub__API                   import GitHub__API
from osbot_github.api.cache.TestCase__GitHub__API   import TestCase__GitHub__API
from osbot_utils.utils.Misc                         import list_set
from osbot_utils.utils.Objects                      import pickle_save_to_bytes, pickle_load_from_bytes, obj_data
from tests.api.cache.test_GitHub__API__Cache        import GIT_HUB__USER_NAME, GIT_HUB__ORG_NAME__OWASP_SBOT, GIT_HUB__REPO__OSBOT_GITHUB


class test_GitHub_API(TestCase__GitHub__API):
    github_api       : GitHub__API
    test_file_path   : str

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_dotenv()
        cls.github_api = GitHub__API()
        #cls.github_api.disable()
        #cls.github_api.update()
        cls.test_file_path = 'docs/test_files/an_markdown_file.md'

    # def setUp(self):
    #     self.github_api_cache.print_requests = True

    def test__init__(self):
        assert list_set(self.github_api.__dict__) == ['log_info', 'session']

    def test_access_token(self):
        assert self.github_api.access_token() is not None
        assert len(self.github_api.access_token()) > 10

    # def test_file_download(self):
    #     repo_full_name = REPO__OSBOT_GIT_HUB
    #     branch         = 'dev'
    #     kwargs         = dict(repo=repo_full_name,branch=branch, file_path=self.test_file_path)
    #     assert '# An Markdown file' in self.github_api.file_download(**kwargs)

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
        assert type(repos)      is PaginatedList
        assert type(repo )      is Repository
        assert repo.owner.login == user_name
        assert len(list(repos))       > 40
        #pprint(f'there are {len(repos)} repos in user {user_name}')

    def test_repos_from_organization(self):
        org_name = GIT_HUB__ORG_NAME__OWASP_SBOT
        repos    = self.github_api.repos_from_organization(org_name=org_name)
        repo     = next(iter(repos), None)
        assert type(repos     ) is PaginatedList
        assert type(repo      ) is Repository
        assert len (list(repos)) > 20
        #pprint(f'there are {len(repos)} repos in organization {org_name}')


    def test__pickle_roundtrip(self):
        def check_pickle_roundtrip(target, expected_type):
            pickled_data   = pickle_save_to_bytes(target)
            target_pickled = pickle_load_from_bytes(pickled_data)

            assert type(pickled_data)       is bytes
            assert  target                  == target_pickled
            assert obj_data(target_pickled) == obj_data(target_pickled)
            assert type(target)             is expected_type

        org_name       = GIT_HUB__ORG_NAME__OWASP_SBOT
        user_name      = GIT_HUB__USER_NAME
        repo_full_name = GIT_HUB__REPO__OSBOT_GITHUB

        #check_pickle_roundtrip(self.github_api_cache.github().get_organization(org_name ), Organization)
        #check_pickle_roundtrip(self.github_api_cache.github().get_user        (user_name), NamedUser   )
        #check_pickle_roundtrip(self.github_api_cache.github().get_repo        (repo     ), Repository  )

        check_pickle_roundtrip(self.github_api.organization(org_name       = org_name       ), Organization)
        check_pickle_roundtrip(self.github_api.user        (user_name      = user_name      ), NamedUser   )
        check_pickle_roundtrip(self.github_api.repo        (repo_full_name = repo_full_name ), Repository  )

