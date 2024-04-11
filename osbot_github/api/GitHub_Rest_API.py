from os import getenv

import requests
from dotenv import load_dotenv
from github import Github

from osbot_utils.utils.Misc                       import datetime_to_str
from osbot_utils.utils.Python_Logger              import logger_info
from osbot_utils.decorators.lists.group_by        import group_by
from osbot_utils.decorators.lists.index_by        import index_by
from osbot_utils.decorators.methods.cache_on_self import cache_on_self

GIT_HUB__ACCESS_TOKEN   = "GIT_HUB__ACCESS_TOKEN"
GIT_HUB__REPO_PATH      = 'https://raw.githubusercontent.com/'
GIT_HUB__DEFAULT_BRANCH = 'main'
GIT_HUB__DEFAULT_REPO   = 'owasp-sbot/OSBot-GitHub'

# todo refactor this to one of the OSBot repos
class GitHub_Rest_API:

    def __init__(self, target_repo=None, target_branch=None):
        self.target_repo    = target_repo   or GIT_HUB__DEFAULT_REPO
        self.target_branch  = target_branch or GIT_HUB__DEFAULT_BRANCH
        self.log_info       = logger_info()
        self.session        = requests.Session()

    def access_token(self):
        load_dotenv()
        return getenv(GIT_HUB__ACCESS_TOKEN)

    def commits(self, count=5):
        raw_commits = self.repo().get_commits().get_page(0)
        commits = []
        for raw_commit in raw_commits[:count]:
            # files = []
            # for file in raw_commit.files:
            #     files.append(file.filename)
            commit = dict(  author  = raw_commit.author.login if raw_commit.author else 'Unknown',
                            date    = datetime_to_str(raw_commit.commit.author.date)    ,
                            #files   = files                                             ,
                            message = raw_commit.commit.message                         ,
                            sha     = raw_commit.sha                                    ,
                            #url     = raw_commit.url                                   # this can be calculated from the repo path and the sha
                            )

            commits.append(commit)
        return commits

    def raw_contents(self, path=""):
        return self.repo().get_contents(path)

    def file_content(self, path=""):
        parsed_content = self.file_parsed_content(path=path)
        return parsed_content.get('content')

    def file_download(self, file_path):
        download_url = f'{GIT_HUB__REPO_PATH}/{self.target_repo}/{GIT_HUB__DEFAULT_BRANCH}/{file_path}'
        headers      = {'Authorization': f'token {self.access_token()}',
                        'Accept-Encoding': 'gzip'}
        response     = self.session.get(download_url, headers=headers)
        return response.text

    def file_parsed_content(self, path=""):
        raw_contents = self.raw_contents(path)
        #pprint(obj_info(raw_contents))
        return self.parse_raw_content(raw_contents)

    @index_by
    @group_by
    def folder_contents(self, path=""):
        folder_contents = []
        raw_contents = self.raw_contents(path)
        if type(raw_contents) is list:
            for raw_content in raw_contents:
                content = self.parse_raw_content(raw_content)
                folder_contents.append(content)

        return folder_contents

    @index_by
    @group_by
    def folder_files(self, path=""):
        return self.folder_contents(path, group_by='type').get('file', [])

    @index_by
    @group_by
    def folder_folders(self, path=""):
        return self.folder_contents(path, group_by='type').get('dir', [])

    # this is VERY slow (when running on root)
    @index_by
    @group_by
    def folders_and_files(self, path=""):
        all_contents = []
        current_folder_contents = self.folder_contents(path)

        for item in current_folder_contents:
            all_contents.append(item)
            if item['type'] == 'dir':
                all_contents.extend(self.folders_and_files(item['path']))
        return all_contents

    def github(self):
        return Github(self.access_token())

    def parse_raw_content(self, raw_content):
        if type(raw_content) is not list:
            item_content = {'name': raw_content.name,
                            'path': raw_content.path,
                            'sha': raw_content.sha,
                            'size': raw_content.size,
                            'type': raw_content.type,
                            'last_modified': raw_content.last_modified,
                            'download_url': raw_content.download_url}

            if raw_content.type == 'file':
                item_content['content'] = raw_content.decoded_content.decode()
                #pprint(obj_info(raw_content))
            return item_content
        return {}

    @cache_on_self
    def repo(self):
        return self.github().get_repo(self.target_repo)