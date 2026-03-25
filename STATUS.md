# xhs-gongkao-publisher 开发断点
> 更新：2026-03-25

## 当前版本：v3.0.0

## 完成状态
- [x] v1.0.0 基础流程：选题→文案→图文→发布
- [x] v1.1.0 反AI检测：内容8条规则
- [x] v1.2.0 三层防御：内容规则 + 图片写实化 + 行为随机化 + 全文注释系统
- [x] v1.3.0 发布通道扩展与环境自动检测
- [x] v1.4.0 发布通道策略调整：Browser 优先
- [x] 首次实际发布验证（2个账号，Browser通道）
- [x] v1.4.1 工程化补强：README、requirements、.gitignore、check 脚本、CI、脚本容错增强
- [x] v1.5.0 移除备用发布方案，统一为 Browser-only 工作流
- [x] v2.0.0 架构升级：MCP 优先 + Browser 兜底，接入 xiaohongshu-mcp 发布/搜索/互动，矩阵管理就绪
- [x] v3.0.0 架构升级：CDP Browser 一级通道 + MCP 兜底，CSS 选择器集中管理，竞品分析，竞品分析，数据回流，统一 CLI

## 发布记录
| 日期 | 账号 | 标题 | 通道 | 状态 |
|------|------|------|------|------|
| 2026-03-24 | 小鹿备考日记 (MCP-1) | 备考第3个月 我终于摸对了方法😭 | MCP | ✅ 已发布 |
| 2026-03-24 | 小云学姐 (MCP-2) | 备考资料包来了🎁 江苏省考免费领 | MCP | ✅ 已发布 |
| 2026-03-24 | 申论姐妹救助站 (MCP-3) | 本周时政热点申论转化指南 | MCP | ✅ 已发布 |
| 2026-03-17 | Neo-法恒 | 省考考完两天了 焦虑的姐妹看这里 | Browser | 已发布 |
| 2026-03-17 | 让我这条考公船上岸吧 | 省考考完两天了 焦虑的姐妹看这里 | Browser | 已发布（公开） |

## 下一步
1. ~~MCP 登录验证~~ ✅ 三账号均已验证通过（2026-03-24）
2. launchd 自动调度激活：`./scripts/setup-launchd.sh install`
3. 第一周自动运行后观察发布质量，按需调整选题/prompt

## 技术架构
- **选题**: 6大内容支柱轮换 + MCP `search_feeds` 站内热点 + 竞品分析（ContentAnalyzer）
- **persona**: 小鹿（24岁国考上岸党），见 `persona.md`
- **图文模式**: 信息图（baoyu-xhs-images）+ 文字笔记（gemini-image）混合
- **发布**: CDP Browser（一级通道）→ MCP（兜底）→ dry-run
- **CSS 选择器**: `xhs/selectors.py` 集中管理，版本 `2026-03-25`
- **反检测**: `STEALTH_JS` 注入 + 行为随机化延迟
- **互动**: MCP `like_feed` / `post_comment_to_feed`（发布后反检测）
- **数据回流**: `output/metrics.jsonl` 记录笔记数据（点赞/收藏/评论）
- **统一 CLI**: `python -m xhs.cli [check|schedule|metrics|selectors]`
- **矩阵**: 每账号独立 MCP 实例 + 独立 cookie（就绪，待验证）
- **工程校验**: `./scripts/check.sh`

## 关键文件
- `SKILL.md` — 主 Skill 文件（含完整注释导航）
- `xhs/__init__.py` — 包初始化
- `xhs/selectors.py` — CSS 选择器集中管理（版本 `2026-03-25`）
- `xhs/browser.py` — CDP Browser 通道 + 数据回流
- `xhs/content_analyzer.py` — 竞品分析引擎
- `xhs/cli.py` — 统一 CLI 入口
- `persona.md` — 人设配置
- `references/publish-sop.md` — 发布操作 SOP（CDP 一级 + MCP 兜底）
- `references/content-pillars.md` — 内容支柱+选题池
- `output/publish-log.md` — 发布日志
- `output/metrics.jsonl` — 数据回流（互动数据）

## 已知问题
- CDP Browser 通道：XHS 私密发布下拉（d-select Vue组件）有反自动化保护，需跳过后台发布
- MCP 闭源依赖：xiaohongshu-mcp 为闭源 Go binary，XHS 改接口后需等作者更新（Browser 一级通道缓解此风险）
- MCP cookie 过期周期待验证（上次有效期约 40 天）
- **XHS 标题字数限制**：约 20 个字符（含 emoji），安全上限 ≤18 中文字+1 emoji
- **baoyu-image-gen `--ref` 不兼容豆包**：`--ref` 触发 OpenAI edits API，豆包 ARK 不支持；全部使用独立文生图（无 `--ref`）
- **图片生成配置**：已切换为豆包 Seedream（ARK endpoint），GOOGLE_API_KEY 已过期待续期
