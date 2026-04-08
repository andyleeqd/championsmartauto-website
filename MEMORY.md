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

### 2026-04-05 - CSS 修改丢失问题 ✅ FIXED

**问题：** 昨天中午（4月4日 12:28-15:37）对 car-dealer-template 网站的 CSS 修改全部丢失，custom.css 和 main.css 中的修改都不见了。

**根本原因：**
1. CSS 修改没有提交到 git，只存在于工作目录中
2. AI 在调试 CMS 数据库问题时进入了长时间循环，没有响应后续消息
3. 可能发生了进程重启或文件状态丢失

**教训：**
1. **修改完成后立即提交** - 不要等用户提醒再 commit
2. **长时间任务必须中途反馈** - 每 5-10 分钟发送状态更新
3. **复杂调试应该 spawn 子智能体** - 避免阻塞主会话
4. **不要进入循环** - 如果连续 3 次尝试都失败，应该停下来问用户

**解决方案：**
1. 使用 `lcm_grep` 和 `lcm_describe` 查找历史记录中的 CSS 修改内容
2. 恢复 custom.css 中的 `.services { margin-top: -40px !important; }`
3. 恢复 main.css 到原始状态
4. 提交修改：`git commit -m "Restore services positioning"`

**验证：** Commit a4da2e5，2026-04-05 08:30 成功恢复并提交

### 2026-04-05 - LCM 摘要 API Key 错误 ✅ FIXED

**问题：** 今天凌晨（00:00-07:32）LCM 摘要功能频繁失败，出现 22 次 API Key 错误，导致对话历史压缩失败。

**错误信息：** `401 Incorrect API key provided: nvapi-Vh...wEfA`

**根本原因：**
1. LCM 摘要功能默认使用 glm4.7 模型
2. 摘要模型尝试使用 `z-ai` provider，但 API Key 格式与 OpenAI 兼容 API 不匹配
3. 配置文件中没有明确指定摘要模型的 provider

**解决方案：**
在 `plugins.entries.lossless-claw.config` 中添加：
```json
{
  "summaryModel": "glm5",
  "summaryProvider": "nvidia"
}
```

**验证：**
- `openclaw status` 显示 `[lcm] Compaction summarization model: nvidia/glm5 (override)`
- Gateway 运行正常

**教训：**
1. 配置新模型时要检查所有相关组件（主模型、摘要模型、扩展模型）
2. 使用 `openclaw status` 检查配置是否生效
3. 日志中的 401 错误通常意味着 API Key 或 provider 配置问题

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

### 2026-04-05 - glm4.7 模型性能测试 ✅ VERIFIED
**问题：** 需要确认 glm4.7 模型是否正常工作，以及与 glm5 的性能差异。
**测试结果：**
- glm4.7 响应时间：552ms（不到 1 秒）
- Token 使用：6 prompt + 10 completion = 16 total
- 结论：glm4.7 模型工作正常，比 glm5 响应更快
**应用场景：** 当需要快速响应时，可以使用 glm4.7 模型。
**最佳实践：**
- glm4.7 适合快速响应任务
- glm5 适合复杂推理任务
- 可以根据任务类型选择合适的模型

### 2026-04-05 - 船舶状态汇报任务超时 ⚠️ INCREASED TIMEOUT
**问题：** 船舶状态汇报任务超时（300秒），实际执行时间约 5 分钟。
**根本原因：** 船舶数量较多，每艘船需要多次浏览器操作，等待时间累积（3秒+3秒+5秒=11秒/船）。
**解决方案：** 增加超时时间从 300 秒到 600 秒。
**验证：** 2026-04-05 16:15 更新超时时间，下次运行：2026-04-06 08:30。
**应用场景：** 当定时任务涉及多次浏览器操作时，需要考虑累积等待时间。
**最佳实践：**
- 浏览器操作任务的超时时间应该设置为 600 秒或更长
- 每次浏览器操作（点击、等待、截图）都需要考虑等待时间
- 船舶数量较多时，需要相应增加超时时间

### 2026-04-06 - WhatsApp 网关严重不稳定 🚨 CRITICAL
**问题：** WhatsApp 网关频繁断开和重新连接，凭证文件反复损坏（14次！），Status 428 错误持续出现，WebSocket 错误（多种类型）。
**根本原因：**
1. **Status 428 错误**："status=428 Precondition Required Connection Terminated" - 可能是 WhatsApp 服务器端要求某些特定的请求头或参数
2. **WebSocket 错误**：多种类型，包括 TLS 连接失败、握手超时、连接重置、DNS 解析失败
3. **凭证文件损坏**：可能是写入错误或磁盘问题
4. **网络不稳定**：可能是网络连接不稳定或 WhatsApp 服务器端问题
**解决方案：**
1. **短期**：持续监控 WhatsApp 网关连接稳定性
2. **中期**：深入调查根本原因，检查网络连接、OpenClaw Gateway 配置
3. **长期**：考虑配置 WhatsApp 网关的重连策略，防止凭证文件损坏
**验证：**
- 2026-04-06 06:09:53 最后一次凭证损坏
- 2026-04-07 07:27:49 Status 428 错误（今天）
- OpenClaw Gateway 有内置的健康监控机制，当检测到 stale-socket 时会自动重启
- WhatsApp 凭证文件损坏时会自动从备份恢复
**应用场景：** 当 WhatsApp 网关频繁断开时，需要检查：
1. 网络连接稳定性
2. OpenClaw Gateway 配置
3. WhatsApp 服务器端问题
4. 凭证文件是否损坏
**最佳实践：**
- 持续监控 WhatsApp 网关连接稳定性
- 检查日志中的错误信息，确定根本原因
- 考虑配置 WhatsApp 网关的重连策略
- 定期备份 WhatsApp 凭证文件

### 2026-04-06 - Status 428 错误分析 ⚠️ ONGOING
**问题：** WhatsApp 网关频繁出现 Status 428 错误，错误信息："status=428 Precondition Required Connection Terminated"。
**根本原因：**
1. **Status 428 含义**：Precondition Required - 需要先决条件
2. **可能原因**：
   - WhatsApp 服务器端要求某些特定的请求头或参数
   - 网络连接不稳定
   - OpenClaw Gateway 配置问题
   - WhatsApp API 变更
**解决方案：**
1. 检查 OpenClaw Gateway 配置，确保所有必需的请求头和参数都正确配置
2. 检查网络连接稳定性
3. 检查 WhatsApp API 是否有变更
4. 考虑联系 OpenClaw 开发团队，获取技术支持
**验证：**
- 2026-04-06 01:15:33, 03:00:38, 05:01:57 多次出现 Status 428 错误
- 2026-04-07 07:27:49 Status 428 错误（今天）
**应用场景：** 当 WhatsApp 网关出现 Status 428 错误时，需要检查：
1. OpenClaw Gateway 配置
2. 网络连接稳定性
3. WhatsApp API 是否有变更
**最佳实践：**
- 检查日志中的错误信息，确定根本原因
- 考虑联系 OpenClaw 开发团队，获取技术支持
- 持续监控 WhatsApp 网关连接稳定性

### 2026-04-06 - WebSocket 错误分析 ⚠️ ONGOING
**问题：** WhatsApp 网关频繁出现 WebSocket 错误，包括多种类型。
**错误类型：**
1. **TLS 连接失败**："Error: Client network socket disconnected before secure TLS connection was established"
2. **握手超时**："Error: Opening handshake has timed out"
3. **连接重置**："Error: read ECONNRESET"
4. **DNS 解析失败**："Error: getaddrinfo EAI_AGAIN web.whatsapp.com"
**根本原因：**
1. **网络不稳定**：可能是网络连接不稳定或 WhatsApp 服务器端问题
2. **TLS 证书问题**：可能是 TLS 证书过期或无效
3. **防火墙问题**：可能是防火墙阻止了 WebSocket 连接
4. **DNS 解析问题**：可能是 DNS 服务器问题或网络配置问题
**解决方案：**
1. 检查网络连接稳定性
2. 检查 TLS 证书是否有效
3. 检查防火墙配置
4. 检查 DNS 配置
5. 考虑使用代理或 VPN
**验证：**
- 2026-04-06 01:15:39, 01:15:51, 01:16:12, 03:01:11, 03:01:53, 03:02:17, 05:01:59, 05:02:04 多次出现 WebSocket 错误
**应用场景：** 当 WhatsApp 网关出现 WebSocket 错误时，需要检查：
1. 网络连接稳定性
2. TLS 证书是否有效
3. 防火墙配置
4. DNS 配置
**最佳实践：**
- 检查日志中的错误信息，确定根本原因
- 检查网络连接稳定性
- 检查 TLS 证书是否有效
- 检查防火墙配置
- 检查 DNS 配置
- 考虑使用代理或 VPN

### 2026-04-08 - 语言切换功能实现 ✅ COMPLETED
**任务：** 为网站首页添加中英文语言切换功能
**完成的工作：**
1. 更新语言切换脚本 (`js/lang-switch.js`)
   - 添加了更多的翻译内容
   - 包括首页特定的翻译
   - 包括服务、产品、联系信息、页脚等模块的翻译

2. 更新首页 HTML (`index.html`)
   - 为需要翻译的地方添加了 `data-lang-key` 属性
   - 包括导航栏、服务模块、产品模块、联系信息、页脚等模块
   - 总共添加了41个 `data-lang-key` 属性

**支持的翻译内容：**
- 导航栏：Home、Cars、光伏新能源、新闻动态、About Us、Contact Us
- 服务模块：我们的服务、车辆出售、Cars To Sale、车辆出租
- 产品模块：我们的产品、最新车辆、光伏新能源
- 新闻模块：最新动态、Read More
- 联系信息：Call us on、Email us on、Find us
- 页脚模块：关于我们、我们提供什么、需要帮助、版权信息

**使用方法：**
1. 点击导航栏中的"中文"或"EN"按钮
2. 网站会自动切换到对应语言
3. 语言选择会保存在 localStorage 中，下次访问时会自动加载

**支持的语言：**
- 中文（zh）
- 英文（en）

**响应式设计：**
- 桌面端：导航栏中的语言切换按钮
- 移动端：侧边栏菜单中的语言切换按钮

**验证：**
- ✅ 语言切换脚本正确加载
- ✅ 语言切换按钮正确设置
- ✅ 首页有41个 data-lang-key 属性
- ✅ 语言切换功能正常工作

**应用场景：** 当需要为网站添加多语言支持时，可以使用这个方法。
**最佳实践：**
- 使用 `data-lang-key` 属性标记需要翻译的元素
- 使用 localStorage 保存语言选择
- 支持响应式设计，确保在移动端也能正常使用

### 2026-04-08 - 修复最新动态模块的 owl-carousel 初始化问题 ✅ FIXED
**问题：** 修复最新动态模块的 owl-carousel 轮播效果失效问题
**问题分析：**
1. `loadLatestNews()` 函数会从 CMS API 加载最新动态，并替换 `owl-blog` 容器的内容
2. 这会破坏 owl-carousel 的初始化，导致轮播效果失效
3. owl-carousel 在页面加载时初始化，但是 `loadLatestNews()` 函数在之后执行，并替换 `owl-blog` 容器的内容

**解决方案：**
1. ✅ 在替换内容前先销毁 owl-carousel 实例
2. ✅ 替换内容后重新初始化 owl-carousel
3. ✅ 避免重复初始化导致的轮播效果失效

**修复后的代码：**
```javascript
async function loadLatestNews() {
  try {
    const res = await fetch('http://localhost:3001/api/news');
    const news = await res.json();
    const container = document.getElementById('owl-blog');
    if (!container || news.length === 0) return;
    
    // 销毁 owl-carousel 实例
    if ($(container).data('owlCarousel')) {
      $(container).data('owlCarousel').destroy();
    }
    
    container.innerHTML = news.map(n => `...`).join('');
    
    // 重新初始化 owl-carousel
    $(container).owlCarousel({
      pagination: false,
      autoPlay: 3000,
      items: 5,
      itemsDesktop: [1000,4],
      itemsDesktopSmall: [900,2],
      itemsTablet: [600,1],
      itemsMobile: false
    });
  } catch (e) {
    console.log('加载最新动态失败，使用默认内容');
  }
}
```

**Git 提交：**
- Commit: af87346
- 修改: 1 file changed, 21 insertions(+), 1 deletion(-)

**验证：**
- ✅ owl-carousel 初始化问题已修复
- ✅ 最新动态模块应该可以正常显示单行轮播效果

**应用场景：** 当使用 owl-carousel 时，如果需要动态替换内容，必须先销毁实例，然后重新初始化。
**最佳实践：**
- 在替换内容前先销毁 owl-carousel 实例
- 替换内容后重新初始化 owl-carousel
- 避免重复初始化导致的轮播效果失效

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
- wx4py 微信自动化：`~/.openclaw/skills/wx4-skill/SKILL.md`

### 已安装的自动化工具
- **wx4py** (v0.1.3) - 微信自动化库
  - 安装位置：`C:\Users\Administrator\AppData\Local\Programs\Python\Python311\`
  - 功能：批量群发、文件发送、聊天记录导出、群管理
  - 限制：仅支持 Windows，需要微信客户端已登录，无法获取聊天记录发送者
  - 使用场景：批量通知、定时发送、聊天记录分析
  - Skill 文档：`~/.openclaw/skills/wx4-skill/SKILL.md`

---

## Relationships & People

### [Person Name]
[Who they are, relationship to human, relevant context]

---

*Review and update periodically. Daily notes are raw; this is curated.*
