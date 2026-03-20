# xhs-gongkao-publisher 开发断点
> 更新：2026-03-20

## 当前版本：v1.4.0

## 完成状态
- [x] v1.0.0 基础流程：选题→文案→图文→发布
- [x] v1.1.0 反AI检测：内容8条规则
- [x] v1.2.0 三层防御：内容规则 + 图片写实化 + 行为随机化 + 全文注释系统
- [x] v1.3.0 双通道发布：MCP + Browser，环境自动检测
- [x] v1.4.0 通道优先级翻转：Browser 优先（本地零配置）→ MCP 备用
- [x] 首次实际发布验证（2个账号，Browser通道）

## 发布记录
| 日期 | 账号 | 标题 | 状态 |
|------|------|------|------|
| 2026-03-17 | Neo-法恒 | 省考考完两天了 焦虑的姐妹看这里 | 已发布 |
| 2026-03-17 | 让我这条考公船上岸吧 | 省考考完两天了 焦虑的姐妹看这里 | 已发布（公开） |

## 下一步
1. 生成新选题内容（避免重复 3/17 已发内容）
2. 测试 `/setup-browser-cookies` 导入真实浏览器 Cookie 免扫码
3. 测试信息图模式（baoyu-xhs-images 集成）

## 技术架构
- **选题**: 6大内容支柱轮换
- **persona**: 小鹿（24岁国考上岸党），见 `persona.md`
- **图文模式**: 信息图（baoyu-xhs-images）+ 文字笔记（gemini-image）混合
- **发布**: Browser（本地，推荐，零配置）/ MCP（备用，需预启动服务）

## 关键文件
- `SKILL.md` — 主 Skill 文件（含完整注释导航）
- `persona.md` — 人设配置
- `references/publish-sop.md` — 发布操作 SOP（Browser优先+MCP备用）
- `references/content-pillars.md` — 内容支柱+选题池
- `output/publish-log.md` — 发布日志

## 已知问题
- Browser 通道：XHS 私密发布下拉（d-select Vue组件）有反自动化保护，无法通过合成事件触发（公开发布后手动切换即可）
- 可通过 `/setup-browser-cookies` 导入本机浏览器 Cookie 减少扫码登录
