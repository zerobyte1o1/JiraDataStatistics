import sys

from jira import JIRA
from config.env import Env
from util.simple_tools import SimpleTools
from util.handle_file import Handlefile


class JiraBase():
    def __init__(self):
        # jira初始化
        try:
            self.jira = JIRA(server=Env.get_jira_url(), basic_auth=(Env.get_username(), Env.get_password()))
            if not self.jira.projects():
                print("jira API令牌已更换，请联系管理员获取令牌")
                sys.exit()
        except:
            print("jira API令牌有误，请联系管理员")
            sys.exit()
        self.st = SimpleTools()
        self.hf = Handlefile()


if __name__ == '__main__':
    res = JiraBase().jira.projects()
    print(res)
