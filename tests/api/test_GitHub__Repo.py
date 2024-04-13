from unittest                               import TestCase
from dotenv                                 import load_dotenv
from osbot_github.api.GitHub__API           import GitHub__API
from osbot_github.api.GitHub__Repo          import GitHub__Repo
from osbot_github.api.cache.GitHub__API__Cache import GitHub__API__Cache
from osbot_github.dbs.Table__GitHub__Repos  import REPO__OSBOT_GIT_HUB
from osbot_github.utils.Version             import Version
#from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files                import parent_folder, file_name
from osbot_utils.utils.Misc                 import list_set


class test_GitHub__Repo(TestCase):
    github_repo    : GitHub__Repo
    repo_full_name : str
    test_file_path : str

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.repo_full_name         = REPO__OSBOT_GIT_HUB
        cls.github_repo            = GitHub__Repo(repo_name=cls.repo_full_name)
        cls.test_file_path         = 'docs/test_files/an_markdown_file.md'
        cls.github_repo.github_api = GitHub__API__Cache()

    def test__init__(self):
        assert self.github_repo.repo_name              == self.repo_full_name
        assert type(self.github_repo.github_api)       is GitHub__API__Cache
        assert list_set(self.github_repo.__locals__()) == ['github_api', 'repo_name']

    def test_commits(self):
        commits = self.github_repo.commits()
        assert type(commits) is list
        for index,commit in enumerate(commits):
            assert type(commit) is dict
            assert list_set(commit) == ['author','date', 'message', 'sha']
            break

    def test_file_content(self):
        file_path = 'osbot_github/version'
        assert self.github_repo.file_content(file_path).strip() == Version().value()

    def test_file_parsed_content(self):
        result    = self.github_repo.file_parsed_content(self.test_file_path)
        assert '# An Markdown file' in result.get('content')

    def test_folder_contents(self):
        results = self.github_repo.folder_contents('docs')
        for result in results:
            assert list_set(result) == ['download_url', 'last_modified', 'name', 'path', 'sha', 'size', 'type']

    def test_folder_files(self):
        file_path     = self.test_file_path
        target_folder = parent_folder(file_path)
        result = self.github_repo.folder_files(target_folder)
        assert len(result)           == 1
        assert list_set(result[0])   == ['content', 'download_url', 'last_modified', 'name', 'path', 'sha', 'size', 'type']
        assert result[0].get('path') == file_path

    def test_folder_folders(self):
        result = self.github_repo.folder_folders("docs")
        assert len(result) == 1
        assert list_set(result[0]) == ['download_url', 'last_modified', 'name', 'path', 'sha', 'size', 'type']

    def test_folders_and_files(self):
        result = self.github_repo.folders_and_files("docs", index_by='path')
        assert self.test_file_path in result
        assert len(result) > 1

    def test_parse_raw_content(self):
        result = self.github_repo.parse_raw_content([])
        assert result == {}

    def test_repo(self):
        repo           = self.github_repo.repo()
        repo_full_name = REPO__OSBOT_GIT_HUB
        repo_name     = file_name(repo_full_name, check_if_exists=False)
        assert repo.default_branch == 'dev'
        assert repo.id             ==  784967553
        assert repo.full_name      == repo_full_name
        assert repo.name           == repo_name
        assert repo.git_url        == f'git://github.com/{REPO__OSBOT_GIT_HUB}.git'

    def test_repo_data(self):
        repo_data = self.github_repo.repo_data()
        assert repo_data.get('full_name') == self.repo_full_name
        assert list_set(repo_data) == ['archived', 'created_at', 'default_branch', 'description',
                                       'forks', 'full_name', 'language', 'name', 'organisation',
                                       'owner', 'private', 'pushed_at', 'repo_id', 'size', 'stars',
                                       'topics', 'updated_at', 'url', 'visibility', 'watchers']

    def test_repo_obj(self):
        repo_data = self.github_repo.repo_data()
        repo_obj  = self.github_repo.repo_obj()
        assert repo_obj.__attr_names__() == list_set(repo_data)
        assert repo_obj.__locals__    () == repo_data

    # todo: refactor the getting of the job details into github_repo codebase
    def test_get_workflow_runs(self):
        print()
        repo = self.github_repo.repo()
        workflow_runs_list = []
        n = 2
        kwargs = {'branch': 'dev'}
        for i, workflow_run in enumerate(repo.get_workflow_runs(**kwargs)):
            if i >= n:
                break
            workflow_runs_list.append(workflow_run)
            assert len(list(workflow_run.jobs())) == 1


            # for job in workflow_run.jobs():
            #     print(job.url)
            #     logs_url = job.url + '/logs'
            #     data = requests.get(job.url, headers=headers)
            #     pprint(data.json())
            #     data = requests.get(logs_url, headers=headers)
            #     print(data.text)

        # pprint(workflow_runs_list)
        # workflow_runs_list = [run for run in workflow_runs]

        # print(len(workflow_runs_list))

        # for workfow_run in repo.get_workflow_runs():
        #     pprint(workfow_run)
        #     break
        # return
        # last_workflow_run = repo.get_workflow_runs().get_page(0)[0]  # Assuming the latest run is what you want
        # #obj_info(last_workflow_run)
        # for job in last_workflow_run.get_jobs():
        #     pprint(job)
        # job_id = last_workflow_run.get_jobs().get_page(0)[0].id