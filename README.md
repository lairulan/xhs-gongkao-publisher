# xhs-gongkao-publisher

小红书公考种草内容自动生成与发布仓库。这个仓库以 `Skill + SOP + 辅助脚本` 为主，不是一个独立 Web 应用。

## 当前约定

- MCP（xiaohongshu-mcp）是默认主发布通道，Browser 为兜底
- `output/` 只保存本地运行产物，不纳入 Git 跟踪

## 目录说明

- `SKILL.md`: 主工作流和执行规则
- `STATUS.md`: 当前版本、发布验证和下一步
- `persona.md`: 人设和语气约束
- `references/`: 选题、文案、发布 SOP
- `scripts/batch-screenshot.py`: 信息图 HTML 批量截图
- `scripts/check.sh`: 本仓库最小化校验入口

## 环境准备

1. 安装 Python 依赖

```bash
python3 -m pip install -r requirements.txt
```

2. 安装 Playwright Chromium

```bash
python3 -m playwright install chromium
```

3. 确保运行环境可使用 Browser 工具，并提前准备浏览器登录态

建议通过 `/setup-browser-cookies` 导入本机浏览器 Cookie，减少扫码登录。

## 本地校验

运行基础校验：

```bash
./scripts/check.sh
```

## 维护说明

- `output/` 下的日志、内容存档和图片属于运行产物，应保留在本地，不进入版本库
- `__pycache__/`、`.pyc`、`.venv/` 等缓存和环境目录已忽略
- 如调整发布优先级或操作流程，优先同步 `SKILL.md`、`STATUS.md`、`references/publish-sop.md`
