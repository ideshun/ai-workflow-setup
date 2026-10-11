# Qoder 适配

仅用于本次目标为 Qoder 的执行。资料基线：2026-09-24；IDE 与 CLI 分别判断，未注明的发现顺序/版本细节不是保证。

## 路径选择

| 资产 | 新初始化默认 | 存量处理 |
| --- | --- | --- |
| 项目入口 | 根 `AGENTS.md` | 合并已有入口，保留有效指令及层级边界。 |
| Skills | 共享层 `.agents/skills/<name>/SKILL.md`（IDE 0.4.2 起读取，CLI 1.1.11 起默认开启；当前设置仍需核对） | 复用共享来源；原生目录中的共用 Skill 按转换协议列迁移方案，未获准前保留，检查同名来源。 |
| 原生规则 | `.qoder/rules/`（仅在确需原生触发时） | 保存正文不证明触发方式已配置；保留已有元数据及 UI 设置，不猜 schema。 |
| 原生 Agent | `.qoder/agents/<name>.md` | 只在实际需要并获准时创建；公共流程另行引用。 |
| 项目说明/知识/模板 | 共享层 `.agents/AI-CODING.md`、`.agents/knowledge/`、`.agents/templates/` | 由入口显式路由；旧原生目录中的共用内容迁移须获准、合并并更新引用，清理另行确认。 |
| 原生 Wiki | `.qoder/repowiki/wiki_plan.yaml` | 仅在当前版本有效 schema 已核实、用户确有需要时配置，不能当普通文档替代物。 |

这些默认路径只用于没有有效存量的新初始化，不是迁移命令。不要自动创建 `.qoderignore`；如用户确需调整索引范围，展示具体排除内容和影响后另行确认。

## 已知原生行为与限制

- 官方支持根 `AGENTS.md`；Rules 与入口冲突时 Rules 优先。新增入口不自动覆盖用户规则。
- Skills 以 `name`、`description` 基础字段定义；原生目录中的包须包含 `SKILL.md`。
- IDE 0.4.2 发布说明读取 `.agents/skills/`；CLI 1.1.7 加入兼容开关，1.1.11 起默认开启。当前设置可能不同，不将发布记录当本机生效证明。
- Rules 有 Always Apply、Specific Files、Model Decision、Apply Manually。官方说明通过 UI 配置；本参考不提供猜测的 `alwaysApply/globs/ruleType` 文件 schema。
- Rules 文档说明不支持链接。不能把一行 Markdown 链接当作原生导入；根入口明确要求实际读取文档是另一种流程，不等价于按文件自动注入。
- CLI 文档的 `/skills`、`/skills reload` 或 `/settings` 仅用于支持这些命令的端，不假定 IDE 命令相同。

## 安全的最小生成

没有特定文件自动触发要求时，可在根入口放短要求，按需创建自然语言规则正文，并明确写出读取条件。若生成原生规则正文，在交付总结说明 Rules UI 需确认的触发类型；未确认的触发不得标为已经配置。

仅在需要独立静态审查时，可采用已核实的薄 Agent 形式，工具范围须与批准任务一致：

```yaml
---
name: project-reviewer
description: 在明确范围内独立只读审查，流程由项目审查 Skill 定义，不修改或运行项目。
tools: Read, Grep, Glob
---
```

正文只包括主会话提供输入、实际读取入口和审查 Skill、缺 Diff 时的限制、只读护栏。不要重复输出字段或将该工具列表写成其他产品的通用权限配置。

Wiki 的 version 1 schema 曾由 knowledge-plan 能力说明：`repowiki.notes/documents/template` 与 `knowledgecard.notes`；当时不支持有效 `scope` 过滤。执行时先读取当前已安装指引或官方规范；没有可核实版本就保留既有配置并列待确认，不凭此摘要编造文件。

## 公共内容与专属说明

公共手册按通用骨架写项目导航与流程，不绑定 Qoder。发现/刷新、Rules UI、Agent/Wiki 用法仅写 `.qoder/` 下获准的适配说明或交付总结；本次版本与核验状态只写总结。知识显式读取，Wiki 文件存在不表示已构建。

## 来源

- [Rules / AGENTS.md](https://docs.qoder.com/user-guide/rules)
- [Skills](https://docs.qoder.com/cli/Skills)
- [IDE Skills](https://docs.qoder.com/extensions/skills)
- [IDE Release Notes](https://docs.qoder.com/release-notes/desktop)
- [CLI Release Notes](https://docs.qoder.com/release-notes/qoder-cli)
- [Custom Agent](https://docs.qoder.com/extensions/subagent)
- [Indexing](https://docs.qoder.com/user-guide/indexing)
