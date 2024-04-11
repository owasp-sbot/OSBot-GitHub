import pytest
from unittest                           import TestCase
from osbot_github.api.GitHub_Rest_API   import GitHub_Rest_API
from osbot_github.utils.Version         import Version
from osbot_utils.utils.Misc             import list_set

class test_GitHub_Rest_API(TestCase):
    github_rest_api : GitHub_Rest_API
    test_file_path  : str
    @classmethod
    def setUpClass(cls):
        cls.github_rest_api = GitHub_Rest_API(target_branch='dev')
        cls.test_file_path = 'docs/test_files/an_markdown_file.md'

    def test__init__(self):
        assert self.github_rest_api.target_repo   == 'owasp-sbot/OSBot-GitHub'
        assert self.github_rest_api.target_branch == 'dev'

    def test_access_token(self):
        assert self.github_rest_api.access_token() is not None
        assert len(self.github_rest_api.access_token()) > 10

    def test_commits(self):
        commits = self.github_rest_api.commits()
        for commit in commits:
            assert list_set(commit) == ['author','date', 'message', 'sha']

    def test_file_content(self):
        file_path = 'osbot_github/version'
        assert self.github_rest_api.file_content(file_path).strip() == Version().value()

    def test_file_parsed_content(self):
        result    = self.github_rest_api.file_parsed_content(self.test_file_path)
        assert '# An Markdown file' in result.get('content')

    def test_file_download(self):
        assert '1# An Markdown file' in self.github_rest_api.file_download(self.test_file_path)

    @pytest.mark.skip("to be refactored into s3")
    def test_folder_contents(self):
        result = self.github_rest_api.folder_contents('docs')
        assert len(result) == 3

    @pytest.mark.skip("to be refactored into s3")
    def test_folder_files(self):
        result = self.github_rest_api.folder_files("docs")
        assert len(result) == 1
        assert result[0].get('path') == 'docs/homepage.md'

    @pytest.mark.skip("to be refactored into s3")
    def test_folder_folders(self):
        result = self.github_rest_api.folder_folders("docs")
        assert len(result) > 1

    @pytest.mark.skip("to be refactored into s3")
    def test_folders_and_files(self):
        result = self.github_rest_api.folders_and_files("docs", index_by='path')
        assert self.test_file_path in  result
        assert len(result) > 3

    def test_parse_raw_content(self):
        result = self.github_rest_api.parse_raw_content([])
        assert result == {}

    def test_repo(self):
        repo = self.github_rest_api.repo()
        assert repo.default_branch == 'dev'
        assert repo.id             ==  784967553
        assert repo.full_name      == "owasp-sbot/OSBot-GitHub"
        assert repo.name           == 'OSBot-GitHub'
        assert repo.git_url        == 'git://github.com/owasp-sbot/OSBot-GitHub.git'

    @pytest.mark.skip("to be refactored into s3")
    def test___get_last_action_details(self):
        print()
        repo = self.github_rest_api.repo()
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


        #pprint(workflow_runs_list)
        #workflow_runs_list = [run for run in workflow_runs]

        #print(len(workflow_runs_list))
        return
        # for workfow_run in repo.get_workflow_runs():
        #     pprint(workfow_run)
        #     break
        # return
        # last_workflow_run = repo.get_workflow_runs().get_page(0)[0]  # Assuming the latest run is what you want
        # #obj_info(last_workflow_run)
        # for job in last_workflow_run.get_jobs():
        #     pprint(job)
        #job_id = last_workflow_run.get_jobs().get_page(0)[0].id