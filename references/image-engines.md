# 图片引擎说明

## v2.x 引擎 — AI图片生成（Doubao Seedream）

**触发方式**：`--engine ai`（当前默认）
**特点**：
- 使用豆包 Seedream-3.0 文生图
- ARK endpoint: `https://ark.cn-beijing.volces.com/api/v3`
- model: `doubao-seedream-3-0-t2i-250415`
- **会触发小红书 AI 内容标识**（平台合规标注，无法规避）
- 适合：场景配图、人物插画、氛围图

**环境变量**：
```bash
export OPENAI_API_KEY="$ARK_API_KEY"
export OPENAI_BASE_URL="https://ark.cn-beijing.volces.com/api/v3"
export IMAGE_MODEL="doubao-seedream-3-0-t2i-250415"
```

**调用方式（Step 4 中）**：
```
使用 baoyu-image-gen，model=$IMAGE_MODEL，生成8张卡片配图
```

---

## v3.0 引擎 — HTML卡片渲染（截图，无AI标识）

**触发方式**：`--engine html`
**特点**：
- 用 Python + Playwright 将内容渲染为 HTML 卡片后截图
- 无任何 AI 元数据，不触发小红书 AI 标识
- 渲染脚本：`scripts/render-html-cards.py`
- 三个账号各有独立视觉风格（见下方）
- 图片清晰度高，文字可读性强
- **推荐用于干货/攻略类内容**（文字卡片效果更佳）

**三账号视觉风格**：
| 账号 | 风格 | 主色 | 特点 |
|------|------|------|------|
| 账号1 小鹿备考日记 | 暖米色手账风 | #E8956D | 手写感、暖色调 |
| 账号2 小云学姐 | 清爽青绿江南感 | #4CAF87 | 清新、简洁 |
| 账号3 申论姐妹救助站 | 知性蓝绿专业感 | #3B7DD8 | 专业、条理 |

**调用流程（Step 4 中）**：
```bash
# 1. 将卡片内容写入 cards.json
# 2. 调用渲染器
python ~/.claude/skills/xhs-gongkao-publisher/scripts/render-html-cards.py \
  --input /tmp/xhs-cards.json \
  --output ~/xhs-images/$(date +%Y%m%d)-[选题]/ \
  --account [1|2|3]

# 3. 读取 manifest.json 获取图片路径列表
# 4. 传入 MCP publish_content
```

**cards.json 格式**：
```json
[
  {
    "index": 1,
    "title": "封面标题（15字以内）",
    "body": "正文内容\n• 列表项1\n• 列表项2\n→ 总结句",
    "tags": ["可选标签"]
  },
  {
    "index": 2,
    "title": "第2张标题",
    "body": "..."
  }
]
```

---

## 引擎选择建议

| 内容类型 | 推荐引擎 | 原因 |
|---------|---------|------|
| 干货攻略（学习方法/题型拆解/资料分享）| **v3.0 HTML** | 文字清晰，无AI标 |
| 备考日记/心态/打卡 | **v3.0 HTML** | 手账感更真实 |
| 场景配图/封面氛围图 | v2.x AI | AI图更有视觉冲击 |
| 混合（正文卡片+封面配图）| v3.0 HTML + v2.x AI 封面 | 最佳效果 |

**当前默认**：v3.0 HTML（2026-03-24 起，避免 AI 标识）
