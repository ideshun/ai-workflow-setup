# 只读盘点

## 1. 确认范围

1. 先检查项目根、父路径和 `.git` 标记的类型，记录索引指纹（工具可用时）；不沿软链接、不读取链接目标、不改索引。
2. 只列根入口、`.agents/` 和目标/存量 IDE 的 rules、skills、agents、knowledge、templates、手册及必要原生配置；排除凭证、私人历史、memory、构建产物。
3. 通过安全索引查询识别 mode `160000` 的 gitlink；子模块与嵌套仓库不递归。不能确认继承范围或边界时记录未知，暂停受影响路径的写入。

## 2. 选择盘点方式

1. 有 Python 且平台支持时，可运行包内[盘点工具](../scripts/inventory.py)：`python3 <Skill目录>/scripts/inventory.py <项目>`。只用该可信工具，不运行存量项目脚本。
2. 检查退出码、`scan_complete`、`warnings`、`git.status`；失败、截断、`null` 状态均不当成无存量或无改动。工具在 Git 边界查询失败时不进入 AI 目录；父级指导、未扫描目录和嵌套子项目按获准范围补查，不能当成空目录。
3. 无 Python、平台不支持或工具受限时，使用宿主的列表、路径类型和定向读取能力检查同一范围；不安装依赖。不能确认安全的部分标未知，不用不受约束的递归扫描补齐。

## 3. 限制所有 Git 查询

1. 优先使用已确认不会刷新索引或执行仓库程序的宿主接口；无法确认时使用下列仅元数据查询。路径须已批准、加引号并置于 `--` 后。

```text
git --no-optional-locks -c core.fsmonitor=false -c core.untrackedCache=false --literal-pathspecs -C "<项目>" ls-files --stage -z -- "<候选路径>"
git --no-optional-locks -c core.fsmonitor=false -c core.untrackedCache=false --literal-pathspecs -C "<项目>" ls-files --others --exclude-standard -z -- "<候选路径>"
```

2. 不直接调用普通 `status` / `diff` 或项目 hooks、fsmonitor、clean/process、外部 diff/textconv。需工作区内容状态时仅使用已禁用这些程序的可信工具；涉及过滤器的工作区比较无法保证准确时标未知。
3. 元数据不能证明工作区内容未变，也不能单独证明暂存差异。缺 Git、无仓库、权限不足或无法取指纹时披露限制，不初始化仓库、不回写或恢复索引。

## 4. 输出盘点

1. 逐文件记录路径、来源、类型、跟踪/暂存/工作区/忽略状态（可确定的部分）、引用和消费者；保留未知字段。
2. 软链接、硬链接、特殊文件仅列类型，不作为可写普通文件。完成盘点后再按主流程决定是否允许读取、合并或迁移。
