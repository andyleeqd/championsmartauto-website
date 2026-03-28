# Agent 技能使用指南

## agent-reach 使用方法

agent-reach 是多平台搜索工具，支持微信公众号、Twitter、B站、小红书、抖音等。

### 微信公众号搜索

```bash
cd ~/.agent-reach && python3 -c "
import asyncio
from miku_ai import get_wexin_article

async def search():
    articles = await get_wexin_article('关键词', 10)
    for a in articles:
        print(f\"标题: {a['title']}\")
        print(f\"链接: {a['url']}\")
        print('---')

asyncio.run(search())
"
```

### Twitter/X 搜索

```bash
xreach search "关键词" -n 10 --json
xreach tweet URL_OR_ID --json  # 读取单条推文
xreach tweets @username -n 20 --json  # 用户时间线
```

### B站视频

```bash
yt-dlp --dump-json "https://www.bilibili.com/video/BVxxx"
yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh,en" --convert-subs vtt --skip-download -o "/tmp/%(id)s" "URL"
```

### 小红书

```bash
mcporter call 'xiaohongshu.search_feeds(keyword: "关键词")'
mcporter call 'xiaohongshu.get_feed_detail(feed_id: "xxx", xsec_token: "yyy")'
```

### 抖音

```bash
mcporter call 'douyin.parse_douyin_video_info(share_link: "https://v.douyin.com/xxx/")'
```

### 网页提取

```bash
curl -s "https://r.jina.ai/URL"  # 任意网页转markdown
```

### Web 搜索 (Exa)

```bash
mcporter call 'exa.web_search_exa(query: "关键词", numResults: 5)'
```

### GitHub

```bash
gh search repos "关键词" --sort stars --limit 10
gh issue list -R owner/repo --state open
```

## 注意事项

- xreach 需要 Twitter 登录认证
- 小红书需要 Cookie 登录
- 抖音无需登录
- 微信文章用 miku_ai 搜索，用 Camoufox 读取详情
