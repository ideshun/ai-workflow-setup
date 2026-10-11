# Trae 适配

仅用于本次目标为 Trae。基线：2026-09-24；IDE/SOLO 差异依当前端确认，不因共用文档推断所有模式完全一致。

## 默认路径

- 新初始化的原生项目规则放 `.trae/rules/<name>.md`（不通用内容），通过当前 Rules UI 或已核实的 frontmatter 配置。
- Skills 共享层默认 `.agents/skills/<name>/SKILL.md`，依赖 `Enable .agents Skills Directory` 开关：开关状态未确认时在交付总结列明并给出开启步骤；用户不愿启用或确认无效时再经确认改用 `.trae/skills/`（同名时原生优先，说明遮蔽影响）。使用 `name`、`description` 等已核实字段。
- 手册、知识和模板共享层默认 `.agents/AI-CODING.md`、`.agents/knowledge/`、`.agents/templates/`。它们是普通内容，入口或规则需明确要求读取。
- 已有根 `AGENTS.md` 可以继续用，但需用户确认对应导入开关；不要同时创建重复的常驻规则覆盖它。

新项目若需要文件型共同入口，优先当前 Trae 原生项目规则。只有入口读取方式与开关已明确时才依赖 AGENTS.md；不把未启用的入口当已加载。

## 触发与导入

原生规则支持始终、指定文件、智能、手动四种触发。文档描述 `alwaysApply`、`globs`、`description` 等元数据，但执行时必须按目标版本的实际格式生成；额外场景字段、嵌套层数与模式限制不猜测、不从其他产品复制。

需要创建原生规则而 schema 不确定时，先用当前 UI 生成或用户提供的合法样例核对；不能将一个无元数据的 Markdown 文件报告为“已配置指定文件触发”。若转换需要等价触发，在完成核对前不改源。

两项独立导入设置：

- Settings → Rules → Import Settings：`Include AGENTS.md in the context`。
- Settings → Skills & Commands → Import Settings：`Enable .agents Skills Directory`。

本参考不确认开关默认值；不自动修改设置。项目已有 `.agents/skills/` 且开关确认有效时保留原布局；同名 `.trae/skills/` 优先，新增同名副本可能遮蔽公共版本，必须在预览中说明。

## 更新和生成说明

先检查规则实际作用域、现有用户级约束和导入来源，不读私人历史或更改用户规则。公共手册不绑定 Trae；两个导入开关仅在相应资产存在时写入 `.trae/` 下获准的适配说明或交付总结，本次状态只写总结。

没有经过核实的自定义 Agent 注册模板时，不创建 `.trae/agents/` 或 `.agents/agents/` 冒充原生角色。可以在有真实支持的独立任务能力下使用流程文档，不能用同会话自检假称独立审查。

## 来源

- [Rules](https://docs.trae.ai/ide/rules)
- [Skills](https://docs.trae.ai/ide/skills)
