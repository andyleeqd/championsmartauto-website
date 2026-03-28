# MEMORY.md - Long-Term Memory
> Your curated memories. Distill from daily notes. Remove when outdated.

---

## About Paul

### Key Context
- 常用WhatsApp沟通
- 关注船舶跟踪、汇率、小家电OEM采购
- 工作时间：Asia/Shanghai时区

### Preferences Learned
- 定时任务列表格式：不用表格和多余符号，用简洁的列表形式
- 报告格式：简洁清晰，信息密度高
- 需要中途反馈：长时间任务不能静默执行，要定期更新进度

### Important Dates
[Birthdays, anniversaries, deadlines they care about]

---

## Lessons Learned

### 2026-03-18 - Ollama Keepalive Notifications ✅ FIXED
**Problem:** Ollama keepalive script notifications every 10 minutes were too frequent and disruptive.
**Status:** Successfully disabled notifications by setting delivery mode to "none".
**Action:** Updated cron job 57e11985-0764-45b6-8d6d-6717c009b1e0 with delivery: {"mode": "none"}.
**Result:** Script continues to run every 10 minutes in background to keep model hot, but no longer sends WhatsApp notifications.

### 2026-03-19 - 长时间任务必须中途反馈
**问题：** 搜索小家电OEM厂家时，进行了约10次搜索耗时30分钟，期间没有任何状态更新，用户不知道是否在正常工作。
**教训：** 复杂多步骤任务必须中途汇报进度，不能等全部完成再反馈。
**改进：**
1. 长时间任务中途发送状态更新，如"已搜索到X家，继续搜索中..."
2. 告知预计步骤数量
3. 分批发送结果，而不是等全部完成

### 2026-03-19 - 任务完成立即汇报，不等人问
**问题：** Ollama启动任务，21:18就完成启动，但等到21:59用户问"怎么样？"才回复，耗时58分钟。
**教训：** 任务完成后必须立即主动汇报结果，不能等人来问。
**改进：**
1. 任务完成第一时间推送结果，不等人问
2. 断线重连后，主动检查是否有未完成的任务并汇报
3. 执行Windows程序时，优先检查常见路径：
   - /mnt/c/Users/Administrator/AppData/Local/Programs/
   - /mnt/c/Program Files/
   - /mnt/c/Users/{用户名}/AppData/Local/
4. WSL环境下找Windows程序，先用 find 或 ls 遍历 /mnt/c/Users/ 找实际用户目录

### 2026-03-20 - 遇到问题要精确归因，不能简单说"工具不好用"
**问题：**
1. agent-browser 访问船讯网失败，直接说"不好用"，实际是目标网站有反爬机制
2. xreach 未配置认证，却说"工具不好用"，实际是配置缺失
**教训：** 遇到工具失败时，必须先分析根本原因：
1. 是工具本身的问题，还是配置问题？
2. 是目标网站的问题（反爬、JS兼容），还是工具问题？
3. 有没有替代方案可以尝试？
**改进：**
1. 不泛泛地说"不好用"，要说明具体失败原因
2. 工具失败时，主动检查配置是否完整
3. 先尝试替代方案，再下结论
4. 记录具体问题，而不是一棍子打死整个工具

### 2026-03-20 - 复盘后必须有行动
**问题：** 讨论了 agent-reach 和 agent-browser 的问题，但没有立即跟进配置或测试。
**教训：** 复盘不只是记录，必须有具体行动：
1. 记录教训到 MEMORY.md
2. 立即修复可修复的问题（如配置认证）
3. 测试验证改进是否有效
4. 不要"说完了就完了"，要有 follow-through
**改进：**
1. 复盘时明确下一步行动
2. 能立即做的立即执行
3. 需要用户配合的（如提供认证信息）要主动请求

### 2026-03-26 - delivery-mirror 回显循环问题 ✅ IDENTIFIED & WORKAROUND
**问题：** OpenClaw 使用 delivery-mirror 模型在消息发送后自动回显到 session 历史，WhatsApp 网关将这些回显当作用户消息发送，AI 误以为是用户确认而再次回复，形成循环。
**根本原因：**
1. 回显消息的 model 字段为 "delivery-mirror"
2. 回显消息带有完整 metadata 和 idempotencyKey
3. 回显消息的 sender_id 为用户自己的号码
**解决方案：**
- **短期：** AI 识别此模式，忽略 sender 为用户自己号码且 content 与 AI 刚发送内容相同的消息，用 NO_REPLY 处理
- **长期：** 需要联系 OpenClaw 开发团队，在 WhatsApp 网关中过滤 delivery-mirror 模型的回显消息，或调整回显机制让回显不被当作用户消息处理
**验证：** 2026-03-26 09:13 成功识别并忽略多个回显消息，无循环发生

### 2026-03-26 - Netlify Identity 密码重置链接错误 ✅ FIXED
**问题：** 用户无法登录 CMS 后台，密码重置邮件的链接指向错误的站点。
**原因：** 网站未配置 Netlify Identity Widget，导致密码重置 token 无法被处理。
**解决方案：** 在 Hugo 页面模板的 `</head>` 前添加 Netlify Identity Widget 脚本和样式：
```html
<link rel="stylesheet" href="https://identity.netlify.com/v1/netlify-identity-widget.css" />
<script src="https://identity.netlify.com/v1/netlify-identity-widget.js"></script>
<script>
  if (window.netlifyIdentity) {
    window.netlifyIdentity.on("init", user => {
      if (!user) {
        window.netlifyIdentity.on("login", () => {
          document.location.href = "/admin/";
        });
      }
    });
  }
</script>
```
**应用场景：** 所有通过 Netlify Identity 认证的静站点，当用户需要从邮件恢复密码或完成登录流程时，必须在所有页面中包含此 Widget。
**验证：** Commit db15da2，2026-03-26 09:32 成功部署到 `https://championsmartauto.netlify.app/`

### 2026-03-26 - Git index.lock 锁文件问题 ⚠️ RECURRING
**问题：** Git 操作时出现 "Unable to create '.git/index.lock': File exists" 错误。
**原因：** 之前的 Git 进程异常退出，锁文件残留。
**解决方案：** 删除锁文件后重试：
```bash
rm -f .git/index.lock
git commit -m "message"
```
**或者一次性命令：** `git commit ... 2>&1 || (rm -f .git/index.lock && git commit ...)`
**最佳实践：** 定期清理，或者在脚本中添加自动删除锁文件的处理

### 2026-03-26 - 定时任务超时问题 ✅ FIXED
**问题：** 所有定时任务（Gateway 自动重启、船舶状态汇报、汇率通知）都超时失败，连续错误次数：4次、3次、2次。
**根本原因：**
1. 超时配置太短：`timeoutSeconds: 300`（5分钟），任务执行时间超过 300 秒
2. API Key 配置问题：
   - LCM 插件无法找到 z-ai provider 的 API key
   - Tavily API key 未配置到插件配置中
3. 队列等待时间过长：`lane wait exceeded: lane=session:agent:main:main waitedMs=275455 queueAhead=2`
**解决方案：**
1. 增加超时时间：将 `timeoutSeconds` 从 300 增加到 600 秒
   - 文件：`/home/lijia/.openclaw/openclaw.json`
   - 位置：`agents.defaults.timeoutSeconds`
2. 配置 Tavily API Key：添加到 `plugins.entries.openclaw-tavily.config.apiKey`
   - 文件：`/home/lijia/.openclaw/openclaw.json`
   - API Key: `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`
3. 配置 LCM API Key：添加到 `agents/main/agent/auth-profiles.json`
   - Provider: `nvidia`
   - API Key: `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`
**验证：**
- 2026-03-26 16:44 Gateway 重启完成
- 2026-03-26 17:14 Tavily 插件成功初始化：`tavily: initialized (depth=advanced, maxResults=5, answer=true, rawContent=false, timeout=30s, cacheTtl=15min)`
- 2026-03-26 17:14 LCM 插件无错误日志
**应用场景：** 当定时任务超时失败时，需要检查：
1. 超时时间是否足够
2. API Key 是否正确配置
3. 队列等待时间是否过长
**最佳实践：**
- 定时任务超时时间建议设置为 600 秒或更长
- API Key 需要同时配置到 `openclaw.json` 和 `auth-profiles.json`
- 修复配置后需要重启 Gateway 让配置生效

---

## Ongoing Context

### Active Projects
- 子智能体技能配置与测试

### Key Decisions Made
- 所有协作 Agent 都配置了 AGENTS.md，包含搜索工具速查
- 技能文档统一放在 `memory/agent-skills.md`

### Things to Remember
- 微信搜索任务需要更长 timeout（180-300秒）
- GitHub 搜索用 gh CLI 很快，适合短时间任务

### 技能文档位置
- 主文档：`memory/agent-skills.md`
- 各 Agent：`~/.openclaw/agents/{agent}/agent/AGENTS.md`

---

## Relationships & People

### [Person Name]
[Who they are, relationship to human, relevant context]

---

*Review and update periodically. Daily notes are raw; this is curated.*
