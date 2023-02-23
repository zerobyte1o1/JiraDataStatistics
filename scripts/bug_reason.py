import os
import time
from src.api.jira_base import JiraBase
from config.env import Env


class BugReason(JiraBase):
    def get_issues(self, **kwargs):
        """
        获取jira数据
        :param kwargs: 支持输入项目 project="clover,sanity" 和日期 date="2023-02-15~2023-02-18"
        :return:
        """
        if "project" in kwargs:
            project = f"project in ({kwargs['project']})"
        else:
            project = f"project in {Env.get_projects()}"
        if "date" in kwargs:
            list_date = kwargs["date"].split("~")
            date = f" AND created >= {list_date[0]} AND created <= {list_date[1]}"
        else:
            date = ""
        jql = f"{project} {date} AND issuetype = Bug ORDER BY created DESC"
        issues = self.jira.search_issues(jql,maxResults=False)
        print(len(issues))
        list_issues = list()
        for issue in issues:
            list_issue = list()
            # name =lambda x:x.name if x is not None else None
            # print(f"编号\t{issue.key}")
            # print(f"类型\t{issue.fields.issuetype}")
            # print(f"摘要\t{issue.fields.summary}")
            # print(f"描述\t{issue.fields.description}")
            # print(f"bug原因\t{issue.fields.customfield_10220}")
            # print(f"创建时间\t{self.st.dete_format(issue.fields.created)}")
            # print(f"Original coder\t{[f'{issue.fields.customfield_10109}']}")
            # print(f"经办人\t{issue.fields.assignee}")
            # print(f"报告人\t{issue.fields.reporter}\n\n")
            list_issue.append(f"{issue.fields.project}")
            if issue.raw['fields']['customfield_10021'] is None:
                list_issue.append('None')
            else:
                list_issue.append(f"{issue.raw['fields']['customfield_10021'][0]['name']}")
            list_issue.append(f"{issue.key}")
            list_issue.append(f"{issue.fields.issuetype}")
            list_issue.append(f"{issue.fields.summary}")
            list_issue.append(f"{issue.fields.description}")
            list_issue.append(f"{issue.fields.customfield_10220}")
            list_issue.append(f"{self.st.dete_format(issue.fields.created)}")
            list_issue.append(f"{issue.fields.customfield_10109}")
            list_issue.append(f"{issue.fields.assignee}")
            list_issue.append(f"{issue.fields.reporter}")
            list_issues.append(list_issue)
        return list_issues

    def check_bug_reason(self, list_issues: list):
        list_results = list()
        for i in range(len(list_issues)):
            if list_issues[i][6] == 'None' or len(list_issues[i][6]) < 5:
                list_results.append(list_issues[i])
        return list_results

    def create_unqualified_reason_excel(self, list_issues: list):
        header = ["项目", "冲刺", "编号", "类型", "摘要", "描述", "bug原因", "创建时间", "Original coder", "经办人", "报告人"]
        wb, sheet = self.hf.write_excel(header, list_issues)
        sheet.column_dimensions["A"].width = 15
        sheet.column_dimensions["B"].width = 15
        sheet.column_dimensions["C"].width = 15
        sheet.column_dimensions["E"].width = 40
        sheet.column_dimensions["F"].width = 50
        sheet.column_dimensions["G"].width = 15
        sheet.column_dimensions["H"].width = 20
        sheet.column_dimensions["I"].width = 20
        sheet.column_dimensions["J"].width = 15
        sheet.column_dimensions["K"].width = 15
        if 'results' in os.listdir(os.getcwd()):
            results_url = os.path.abspath("results/bug_reason/")
        else:
            results_url = os.path.abspath("../results/bug_reason/")
        result_abs = os.path.join(results_url, '缺陷原因不规范issue_' + str(int(time.time())) + '.xlsx')
        wb.save(result_abs)
        wb.close()

    def run(self, **kwargs):
        """

        :param kwargs: 支持输入项目 project="clover,sanity" 和日期 date="2023-02-15~2023-02-18"
        :return:
        """
        raw = self.get_issues(**kwargs)
        checked_data = self.check_bug_reason(raw)
        self.create_unqualified_reason_excel(checked_data)
        print("缺陷原因不规范issue整理成功！已存放至results/bug_reason文件下")


if __name__ == '__main__':
    BugReason().run(project='clover,sanity', date='2021-02-15~2023-02-18')
