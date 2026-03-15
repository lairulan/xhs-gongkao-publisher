# xhs-gongkao-publisher 开发断点
> 更新：2026-03-12

## 当前版本：v1.2.0

## 完成状态
- [x] v1.0.0 基础流程：选题→文案→图文→发布
- [x] v1.1.0 反AI检测：内容8条规则
- [x] v1.2.0 三层防御：内容规则 + 图片写实化 + 行为随机化 + 全文注释系统

## 下一步：Phase 2 首次运营验证
1. 启动 xiaohongshu-mcp：`cd ~/xiaohongshu-mcp && npm start`
2. 确认小红书账号已登录
3. 运行 Skill：`/xhs-gongkao-publisher`
4. 验证发布成功，检查反AI检测效果

## 技术架构
- **选题**: 6大内容支柱轮换（备考技巧/政策解读/上岸经验/时间管理/心态调整/职位分析）
- **persona**: 小鹿（24岁国考上岸党），见 `persona.md`
- **图文模式**: 信息图（baoyu-xhs-images）+ 文字笔记（gemini-image）混合
- **发布**: xiaohongshu-mcp

## 关键文件
- `SKILL.md` — 主 Skill 文件（含完整注释导航）
- `persona.md` — 人设配置
- `references/` — 爆款笔记参考库
- `output/` — 历史输出

## 已知问题
- 暂无，待首次运营发现问题后更新
