# Cursor 适配

仅用于当前目标为 Cursor。基线：2026-09-24；当前安装版本、CLI/IDE/Cloud 环境和组织设置须另核对。

## 路径与最小格式

- 根 `AGENTS.md`：简单项目指导，无规则触发元数据；官方也支持嵌套入口。避免和已有常驻规则复制同一套正文。
- `.agents/skills/<name>/SKILL.md`：共享层默认，官方已列出该项目级目录；不另建同名副本。已有 `.cursor/skills/` 中的共用流程按转换协议列迁移方案，未获准前保留。
- `.cursor/rules/<name>.mdc`：原生项目规则（不通用内容）。普通 `.md` 不能当成已注册的原生规则。
- 共享层 `.agents/AI-CODING.md`、`.agents/knowledge/`、`.agents/templates/`：按需组织普通文档，明确路由后读取，不自动成为原生能力。
- `.cursor/agents/`：只有独立角色确实需要且当前 schema 已核实时创建；不从其他产品照抄 frontmatter。

已确认的规则元数据含 `alwaysApply`、`globs`、`description`。常驻规则的最小形式：

```text
---
description: 当前项目稳定的共同约束
alwaysApply: true
---
这里是已核实、未与根入口重复的规则正文。
```

需要按文件范围触发时，先确认用户需要的作用域再使用当前版本支持的 `globs` 格式。例如单一匹配模式可写：

```text
---
description: Vue 文件的开发约束
globs: "src/**/*.vue"
alwaysApply: false
---
这里是已核实的 Vue 修改边界。
```

这个语法示例仅适用于确有该路径且需要此作用域的项目；生成时根据实际文件与批准范围填写模式，并核对当前 Cursor 版本支持。不要将示例的框架或范围当作项目事实。

`alwaysApply: true` 表示始终加载；匹配文件可自动附加规则；描述可用于 Agent 相关性判断；手动引用是不同触发方式。空值和组合行为以当前文档为准，不把一个模式转换成另一个而不说明。

## Skills 与兼容来源

官方列出项目和用户级 `.cursor/skills/`、`.agents/skills/`，另兼容部分其他产品技能目录。检查实际发现来源与同名遮蔽，不依靠文件顺序猜优先级，也不要因兼容而添加其他产品目录。

公共基础字段 `name`、`description` 足以描述大多数流程。`paths`、`disable-model-invocation`、界面样式等增强是当前产品扩展；仅在具体需要、语义已核实时使用。更新/转换存量不能删除不认识的字段。

## 原生角色与云端边界

官方自定义 Agent 目录不包含通用 `.agents/agents/` 保证。原生 Agent 注册按当前版本字段保留，不以改扩展名实现等价转换。

本机用户级 Skills 不当然同步到 Cloud Agents、远程机器或自托管环境，不启用同步、不上传项目。公共手册不绑定 Cursor；必要客户端条件写 `.cursor/` 下获准的适配说明或交付总结，本次环境与检查状态只写总结。

## 来源

- [Rules](https://cursor.com/docs/rules)
- [Agent Skills](https://cursor.com/docs/skills)
- [Subagents](https://cursor.com/docs/subagents)
