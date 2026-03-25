# 矩阵账号总配置表

## 账号-MCP-Persona 映射

| 账号 | IP 名称 | MCP 工具前缀 | 端口 | Persona 文件 | 内容方向 |
|------|---------|------------|------|------------|---------|
| 账号1 | 小鹿备考日记 | `mcp__xiaohongshu-mcp__` | 18060 | `personas/account-1-student.md` | 备考过程记录/学习方法 |
| 账号2 | 小云学姐 | `mcp__xiaohongshu-mcp-2__` | 18061 | `personas/account-2-xuejie.md` | 江苏省考/事业编指导/资料分享 |
| 账号3 | 申论姐妹救助站 | `mcp__xiaohongshu-mcp-3__` | 18062 | `personas/account-3-shenlun.md` | 申论专项干货 |

## cookies 路径

```
账号1: ~/xiaohongshu-mcp/cookies.json
账号2: ~/xiaohongshu-mcp/account-2/cookies.json
账号3: ~/xiaohongshu-mcp/account-3/cookies.json
```

## MCP 进程启动命令

```bash
# 账号1（主账号，已在运行）
cd ~/xiaohongshu-mcp && nohup ./xiaohongshu-mcp-darwin-arm64 -port :18060 -headless=true > /tmp/xhs-mcp-1.log 2>&1 &

# 账号2
cd ~/xiaohongshu-mcp/account-2 && nohup ../xiaohongshu-mcp-darwin-arm64 -port :18061 -headless=true > /tmp/xhs-mcp-2.log 2>&1 &

# 账号3
cd ~/xiaohongshu-mcp/account-3 && nohup ../xiaohongshu-mcp-darwin-arm64 -port :18062 -headless=true > /tmp/xhs-mcp-3.log 2>&1 &
```

## 内容发布策略（三号协同）

### 每日节奏
| 时段 | 账号 | 内容类型 |
|------|------|---------|
| 07:00-08:00 | 账号1 | 早打卡/今日计划（高互动时段） |
| 12:00-13:00 | 账号3 | 申论干货（午休刷手机高峰） |
| 20:00-21:00 | 账号2 | 经验分享/攻略（晚间学习时段） |

### 内容互补规则
- **不互动**：三个账号互不关注、互不评论（避免矩阵被识别）
- **话题差异化**：同一热点三个账号角度不同（学生视角/学姐视角/专业视角）
- **发布间隔**：同一话题三账号发布间隔 ≥ 2 天

## 检查登录状态

发布前必须确认目标账号已登录：

```
账号1: mcp__xiaohongshu-mcp__check_login_status
账号2: mcp__xiaohongshu-mcp-2__check_login_status
账号3: mcp__xiaohongshu-mcp-3__check_login_status
```

## 重新登录（cookies 过期时）

```bash
# 账号1
cd ~/xiaohongshu-mcp && ./xiaohongshu-login-darwin-arm64

# 账号2
cd ~/xiaohongshu-mcp/account-2 && ../xiaohongshu-login-darwin-arm64

# 账号3
cd ~/xiaohongshu-mcp/account-3 && ../xiaohongshu-login-darwin-arm64
```
