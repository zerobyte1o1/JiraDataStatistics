import os

import yaml


class Env:
    rootPath = os.path.dirname(os.path.abspath(__file__))
    configPath = os.path.join(rootPath, "env.yaml")
    env = yaml.safe_load(open(configPath))

    @classmethod
    def get_jira_url(cls):
        return cls.env["jira"]["url"]

    @classmethod
    def get_jira_url_browse(cls):
        return cls.env["jira"]["url_browse"]

    @classmethod
    def get_username(cls):
        return cls.env["jira"]["username"]

    @classmethod
    def get_password(cls):
        return cls.env["jira"]["password"]

    @classmethod
    def get_projects(cls):
        return cls.env["jira_default_data"]["projects"]


if __name__ == '__main__':
    res = Env.get_password()
    print(res)
