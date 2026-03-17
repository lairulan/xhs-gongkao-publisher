# xhs-gongkao-publisher 开发断点
> 更新：2026-03-17

## 当前版本：v1.3.0

## 完成状态
- [x] v1.0.0 基础流程：选题→文案→图文→发布
- [x] v1.1.0 反AI检测：内容8条规则
- [x] v1.2.0 三层防御：内容规则 + 图片写实化 + 行为随机化 + 全文注释系统
- [x] v1.3.0 双通道发布：MCP（本地推荐）+ Browser（沙箱备用），环境自动检测
- [x] 首次实际发布验证（2个账号，Browser通道）

## 发布记录
| 日期 | 账号 | 标题 | 状态 |
|------|------|------|------|
| 2026-03-17 | Neo-法恒 | 省考考完两天了 焦虑的姐妹看这里 | 已发布 |
| 2026-03-17 | 让我这条考公船上岸吧 | 省考考完两天了 焦虑的姐妹看这里 | 已发布（公开） |

## 下一步
1. 本地运行 MCP 通道验证（Cookie 持久化 + publish_image）
2. 生成新选题内容（避免重复 3/17 已发内容）
3. 测试信息图模式（baoyu-xhs-images 集成）

## 技术架构
- **选题**: 6大内容支柱轮换
- **persona**: 小鹿（24岁国考上岸党），见 `persona.md`
- **图文模式**: 信息图（baoyu-xhs-images）+ 文字笔记（gemini-image）混合
- **发布**: MCP（本地，推荐）/ Browser+CDP（沙箱，备用）

## 关键文件
- `SKILL.md` — 主 Skill 文件（含完整注释导航）
- `persona.md` — 人设配置
- `references/publish-sop.md` — 发布操作 SOP（MCP优先+Browser备用）
- `references/content-pillars.md` — 内容支柱+选题池
- `output/publish-log.md` — 发布日志

## 已知问题
- Browser 通道：XHS 私密发布下拉（d-select Vue组件）有反自动化保护，无法通过合成事件触发
- 沙箱环境每次新会话需重新扫码登录（Cookie 不持久化）
