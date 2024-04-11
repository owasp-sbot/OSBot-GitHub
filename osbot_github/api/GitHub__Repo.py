from osbot_github.api.GitHub__API                   import GitHub__API
from osbot_github.schemas.Schema__Repo import Schema__Repo
from osbot_utils.base_classes.Kwargs_To_Self        import Kwargs_To_Self
from osbot_utils.decorators.lists.group_by          import group_by
from osbot_utils.decorators.lists.index_by          import index_by
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import datetime_to_str, timestamp_to_str


class GitHub__Repo(Kwargs_To_Self):
    github_api : GitHub__API
    repo_name  : str

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

    def file_content(self, path=""):
        parsed_content = self.file_parsed_content(path=path)
        return parsed_content.get('content')

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


    def raw_contents(self, path=""):
        return self.repo().get_contents(path)

    @cache_on_self
    def repo(self):
        return self.github_api.github().get_repo(self.repo_name)

    def repo_data(self):
        repo = self.repo()
        repo_data = {
            "name"         : repo.name,
            "owner"        : repo.owner.login,
            "full_name"    : repo.full_name,
            "description"  : repo.description,
            "url"          : repo.url,
            "pushed_date"  : int(repo.pushed_at.timestamp () * 1000),
            "created_date" : int(repo.created_at.timestamp() * 1000),
            "updated_date" : int(repo.updated_at.timestamp() * 1000),
            "size"         : repo.size,
            "stars"        : repo.stargazers_count,
            "forks"        : repo.forks_count,
            "watchers"     : repo.watchers_count,
            "language"     : repo.language,
            "topics"       : ",".join(repo.get_topics()),
        }
        return repo_data

    def repo_obj(self):
        repo_data = self.repo_data()
        return Schema__Repo().update_from_kwargs(**repo_data)
