# Codex 适配

仅用于目标为 OpenAI Codex 的执行。基线：2026-09-24；CLI、IDE 扩展、应用及云端能力不能仅凭一个版本相互推导。无可靠版本时只生成已核实的最小形式。

## 路径选择

- 根 `AGENTS.md` 保存项目指导。先检查既有 `AGENTS.md`、`AGENTS.override.md` 和继承配置；具体发现/覆盖行为未核实时不删除或合并这些入口，也不绕过有效覆盖文件。
- Skills 默认 `.agents/skills/<name>/SKILL.md`。官方当前源码扫描项目根到工作目录之间各级目录，并包含用户级 `~/.agents/skills/`；这是源码依据，不保证所有旧版都相同。
- 现有 `.codex/skills/` 等来源是否有效取决于当前实现/配置；保留候选，不擅自清理。不为支持新目录重写全局配置。
- 项目使用手册共享层默认 `.agents/AI-CODING.md`，知识/模板/自然语言规则按需放 `.agents/knowledge/`、`.agents/templates/`、`.agents/rules/`；这些是内容组织方式，需入口或 Skill 明确阅读，不是原生执行策略。

## 规则的关键区别

Codex 的 `.rules` / `prefix_rule` 是命令执行策略，决策包括 `allow`、`prompt`、`forbidden`，不是 Markdown 编码规范。不要执行这些文件，也不要把自然语言“禁止提交”转换成放宽执行权限的配置。

不因初始化 AI 资产创建 `config.toml`、sandbox/approval 配置、执行策略或 MCP 设置。遇到这类存量只在获准时读必要部分，保留未知字段与权限边界；敏感值不复制到说明或迁移预览。

`AGENTS.md` 的详细层级/覆盖规范在先前抓取中未完整取得，官方文档入口可能有访问限制。不能把抓取失败当成产品不支持，也不能把 Skills 扫描逻辑当作入口扫描逻辑。简单根入口以官方约定使用；涉及覆盖和迁移时定向核实目标版本。

## 生成与更新

Skills 首先采用 `name`、`description` 和 Markdown 正文。不生成 `agents/openai.yaml` 或其他专有 UI 字段来凑完整；确需时先查当前规范。

本参考没有可安全通用化的原生自定义 Agent 注册模板。需要独立审查时，先核实当前端提供的 subagent 能力及格式；无依据则保留流程文档和手动交接，不创建伪 `.agents/agents` 配置，也不声称同会话自检是独立审查。

公共手册只写项目导航与通用流程，不绑定 Codex。工作目录对发现范围的影响和专属调用方式写 `.codex/` 下获准的适配说明或交付总结；本次版本、实际来源与待验收项只写总结。用户级技能不改动，不复制其他产品命令。

## 来源

- [官方 Skills 根目录实现](https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/host_roots.rs)
- [官方执行策略说明](https://github.com/openai/codex/blob/main/codex-rs/execpolicy/README.md)
- [AGENTS.md 官方参考入口](https://developers.openai.com/codex/agent-configuration/agents-md)
- [AGENTS.md 开放约定](https://agents.md/)
- [Skills 官方参考入口](https://developers.openai.com/codex/skills)

后两类官方产品页面的详细机制若不可访问，明确取证边界，不能据参考链接本身宣布完整验证。
