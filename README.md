# ai-workflow-setup

一个用于**初始化、更新或迁移项目 AI 工作流与配置**的 Agent Skill（AI 工程化资产）。

核心分工：共用内容（手册、知识、规则、Skills、模板）统一放 `.agents/`，只写项目事实、工作方法和阅读路由；IDE 专属的入口、原生规则、Agent/Wiki 注册放目标 IDE 的原生路径。一次只处理一个目标 IDE，公共内容不绑定任何宿主。

## 适用场景

- 为当前项目初始化 AI 工程化资产（入口、手册、知识、规则、Skills、模板）
- 按当前代码更新已有资产，保留手工内容，移出客户端操作说明与临时核验信息
- 重新整理已有资产：先展示变更方案，不直接覆盖或删除
- 新增其他 IDE 兼容配置，复用 `.agents/` 公共内容
- 只读盘点项目里已有的 AI 配置与缺项

## 不适用场景

- 业务功能开发、普通代码审查
- 插件安装、权限设置、发布工具
- 只读盘点、只计划之外的写入（盘点/计划/审查请求到此为止，零写入）

## 目录结构

```text
ai-workflow-setup/
├── SKILL.md                      主流程：盘点 → 方案 → 写入/合并 → 验证交付
├── references/
│   ├── inventory.md              只读盘点的范围、方式与 Git 查询限制
│   ├── asset-templates.md        内容骨架：入口/手册/知识/规则/Skills/模板
│   ├── conversion.md             跨 IDE 合并与转换协议、等价判定、清理条件
│   ├── ide-qoder.md              Qoder 适配
│   ├── ide-codex.md              Codex 适配
│   ├── ide-cursor.md             Cursor 适配
│   ├── ide-codebuddy.md          CodeBuddy 适配
│   └── ide-trae.md               Trae 适配
└── scripts/
    └── inventory.py              只读盘点工具（Python 3.9+，输出 JSON）
```

## 安装

把整个目录放到宿主能发现的 Skills 位置即可，目录名保持 `ai-workflow-setup`。共享层推荐项目级 `.agents/skills/`；各产品的常见位置如下，实际发现以当前版本为准。

| 目标 | 共享 Skills 位置 | 备注 |
| --- | --- | --- |
| CodeBuddy | `.agents/skills/<name>/SKILL.md` | 生成后核对目标端实际发现；确认不可用且用户同意时才退回 `.codebuddy/skills/` |
| Cursor | `.agents/skills/<name>/SKILL.md` | 官方同时列出项目/用户级 `.cursor/skills/`，注意同名遮蔽 |
| Codex | `.agents/skills/<name>/SKILL.md` | 官方扫描项目根到工作目录之间各级目录，另含用户级 `~/.agents/skills/` |
| Qoder | `.agents/skills/<name>/SKILL.md` | IDE 0.4.2 起读取，CLI 1.1.11 起默认开启，当前设置仍需核对 |
| Trae | `.agents/skills/<name>/SKILL.md` | 依赖 `Enable .agents Skills Directory` 开关；未启用时经确认改用 `.trae/skills/` |

WorkBuddy 按自定义目标处理，不套用 CodeBuddy 适配页。

## 使用

以斜杠命令或自然语言触发均可：

```text
/ai-workflow-setup 为当前项目初始化 AI 工程化资产。
/ai-workflow-setup 根据当前代码更新已有 AI 工程化资产，保留手工内容。
/ai-workflow-setup 重新整理已有 AI 工程化资产，先展示变更方案，不直接覆盖或删除。
/ai-workflow-setup 为当前项目新增 Cursor 原生适配，复用 .agents 公共内容。
```

## 工作方式

1. **确认目标并只读盘点**：记录项目根、操作类型、目标产品/端型/版本；读取对应 IDE 适配；盘点 Git 根、继承入口、获准子项目和路径类型，再读候选配置与最小项目事实。
2. **列方案并取得确认**：列出入口、手册、知识、规则、Skills、模板清单；检出异 IDE 配置时提示并请用户选新增兼容/转换/保留（未回答或选保留则零写入）；按转换协议列源→目标、动作、引用方、消费者与差异，未确认的差异一律暂停。
3. **写入或合并**：复核路径类型、父目录与并发变化；目标已存在则逐段合并而非覆盖；重算相对引用并更新批准范围内的引用方；先写依赖后写入口，无实质变化不写。
4. **验证、清理与交付**：核对批准清单、格式与引用闭包、手工内容保留；分别记录正文保留、触发/作用域等价、静态检查与客户端证据（未访问客户端则写未验证）；清理仅列已验证且无消费者的源文件，展示清单后一次性询问，收到明确确认才删除。

## 产出布局

| # | 配置项 | 默认路径 |
| --- | --- | --- |
| 1 | 根入口 | adapter 规定（如 `CODEBUDDY.md` / `AGENTS.md`） |
| 2 | 手册 | `.agents/AI-CODING.md` |
| 3 | 知识（≥1） | `.agents/knowledge/*.md` |
| 4 | 规则（≥1） | `.agents/rules/*.md` |
| 5 | Skills | `.agents/skills/<name>/SKILL.md` |
| 6 | 模板 | `.agents/templates/*.md`（有 Skill 时） |
| 7 | 原生 Agent | adapter 路径（目标支持、有审查流程且用户需要时） |

内容以项目证据为准，不写空占位；不适用或无依据的项注明原因。

## 各 IDE 适配要点

| 目标 | 根入口 | 原生规则 | 资料基线 |
| --- | --- | --- | --- |
| CodeBuddy | `CODEBUDDY.md`（已有 `AGENTS.md` 回退时须先确认遮蔽影响） | `.codebuddy/rules/<name>/RULE.mdc` | 2026-09-24 |
| Cursor | `AGENTS.md`（支持嵌套） | `.cursor/rules/<name>.mdc`（`alwaysApply`/`globs`/`description`） | 2026-09-24 |
| Codex | `AGENTS.md`（含 `AGENTS.override.md` 覆盖） | 不生成 `config.toml`/执行策略；`.rules` 是命令执行策略，非编码规范 | 2026-09-24 |
| Qoder | `AGENTS.md`（Rules 优先于入口） | `.qoder/rules/`（触发类型由 UI 配置，不猜 schema） | 2026-09-24 |
| Trae | 原生项目规则优先；`AGENTS.md` 需确认导入开关 | `.trae/rules/<name>.md` | 2026-09-24 |

自定义产品须先取得当前端官方规范或有效配置样例；没有依据则只交付盘点与缺项，不生成原生配置。

## 只读盘点工具

```bash
python3 scripts/inventory.py <项目路径> [--max-depth 8] [--max-files 2000]
```

输出 JSON：`project_path`、`git`（可用/根/状态/标记类型）、`assets[]`（路径、来源、类型、`file_type`、`staged`/`worktree`/`tracked`/`ignored`）、`warnings`、`scan_complete`。

退出码：`0` 完整；`1` 受限或拒绝（`scan_complete=false`，字段可能为 `null`）；`2` 参数无效。

工具约束：只列项目根白名单内的候选，不跟随软链接、不进入 gitlink/嵌套仓库；排除凭证、`.env*`、`.npmrc`、私人历史、`memory/` 等敏感名称；Git 仅做元数据查询并禁用 fsmonitor、hooks、外部 diff、clean/process 过滤器；不读文件内容、不回写索引。没有 Python、平台不支持或工具受限时，改用宿主的列表与定向读取能力，不安装依赖。

## 安全边界

- 盘点、计划、审查类请求零写入；目标/文件清单和差异未获准不写入
- 不改业务代码、全局配置、CI、钩子、MCP、权限或索引政策；不安装依赖、不暂存、不提交、不发布
- 未验证的迁移不声明等价；显式读取文件不等于原生发现或自动触发
- 公共正文不写客户端身份、操作教程或本次核验快照，这类信息只写交付总结或目标 IDE 下获准的适配说明
- 私人目录（`memory/`、历史会话、日志）不读取、不迁移、不清理

## 兼容性

- 必需：宿主的文件读取、编辑与路径类型检查能力
- 可选：Git（缺 Git 时披露盘点限制）、Python 3.9+（缺 Python 时用宿主能力替代）
- 不安装任何依赖

## 适配资料时效

各 IDE 适配页的抓取基线均为 2026-09-24。IDE 与 CLI 分开判断，不能用一端的发布记录填补另一端未知项；执行前按当前安装版本核对路径、触发 schema 与开关状态。
