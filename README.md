# 针对jira数据分析脚本
## bug_reason
- 不规范缺陷原因issue提取脚本,可根据项目和时间区间整理不合格的issue，只针对bug类型。
- 使用方法：BugReason().__run__(project="clover,sanity",data="2023-02-15~2023-02-18")
- 产出文件：在results/bug_reason下
