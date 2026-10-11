# CodeBuddy 适配

目标为 CodeBuddy 时读取。基线：2026-09-24；IDE 与 CodeBuddy Code CLI 分开处理，不能用 IDE 发布记录填补 CLI 未知项。

WorkBuddy 按自定义目标处理，不套用本页。[WorkBuddy 官方指南](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Product-Guide)确认 Skills 能力，但未明确本页的项目入口、目录和触发格式；先核实目标端规范，缺失时暂停原生配置生成。

## 默认资产路径

- 新初始化入口优先根 `CODEBUDDY.md`，按当前端规范使用。
- 如果已有根 `AGENTS.md` 并依靠“无 CODEBUDDY.md 时回退”工作，保持该有效入口；新增 CODEBUDDY.md 可能遮蔽它，必须先确认完整承接原指令及用户选择，不能空壳抢占。
- Skills 共享层默认 `.agents/skills/<name>/SKILL.md`：IDE 4.6.2 有 `.agents` 兼容修复记录，但层级、作用域与 CLI 发现未完整核实，生成后核对目标端实际发现，结果及待确认项写交付总结；确认不可用且用户同意时才退回 `.codebuddy/skills/`，不预先双放同名副本。基础字段 `name`、`description`，资源随包保存。
- IDE Rules：`.codebuddy/rules/<name>/RULE.mdc`（不通用内容，仅确需原生触发时）。不要把它机械写成另一产品的平铺规则目录。
- 手册、知识和模板共享层默认 `.agents/AI-CODING.md`、`.agents/knowledge/`、`.agents/templates/`；这些是组织约定，由入口显式路由，不是自动上下文。
- 原生 Agent/其他配置只有当前端规范已核实且任务需要才创建；不照搬别家工具名或权限字段。

## 已核实边界

IDE Rules 文档描述每个规则目录包含 RULE.mdc，支持三种：总是应用、Agent 根据描述判断、手动 @ 引用；创建或修改后需新建会话生效。当前参考没有保证能跨版本复用的完整元数据模板。

遇到需要触发等价的转换，核对当前版本导出的合法格式或官方示例；不能猜写字段，也不能把仅正文复制标作原生注册成功。只做初始文档型配置时，可在已支持的根入口使用短正文与明确阅读路由，说明它与原生触发不同。

IDE 4.6.2 发布记录修复 `.agents` 等目录中的 Skills 查询/调用，但未完整说明层级、作用域与优先级。已有共享 Skills 在实际目标端确认有效时可保持；新初始化按共享层策略默认 `.agents/skills/`，发现核对结果写交付总结。

CLI 文档列出 `.codebuddy/skills/` 与用户级目录，本参考未确认 `.agents/skills/` 的 CLI 发现。CLI 与 IDE 的入口/规则格式和扩展字段若有差异，分别核实。

## 扩展与更新

存量 Skill 可能包含工具权限、context、hooks、变量或执行片段。读取它们用于判断语义，不执行、不删未知字段，也不因为基础标准只需要两字段就将其余字段抹掉。无法解释或目标不支持时暂停转换。

旧原生目录中的共用内容按[转换协议](conversion.md)列 `.agents/` 迁移方案；获准后合并目标、重算链接并更新引用方。验证后仅将无消费者的源文件列入清理询问；未获准或未验证时保留。

私人 `.codebuddy/memory/`、历史会话和日志不是待共享资产，任何流程都不读取、不迁移、不清理。不要从目录存在就宣布项目有有效工程配置，不复制历史到新手册。

公共手册只写项目导航与通用流程，不绑定 CodeBuddy。必要刷新/新会话与调用条件写 `.codebuddy/` 下获准的适配说明或交付总结；本次宿主、版本、实际来源及验证状态只写总结，不写入公共正文。

## 来源

- [IDE Rules](https://www.codebuddy.ai/docs/zh/ide/User-guide/Rules)
- [IDE Skills](https://www.codebuddy.ai/docs/ide/Features/Skills)
- [CLI Skills](https://www.codebuddy.ai/docs/zh/cli/skills)
- [IDE Release Notes](https://www.codebuddy.ai/docs/ide/release-notes/release-notes)
- [CLI 目录结构](https://www.codebuddy.ai/docs/zh/cli/codebuddy-dir)
