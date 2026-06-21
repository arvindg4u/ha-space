# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## 🔍 MCP Server — open-webSearch (DEFAULT)

**Server URL:** `https://open-web-search-2oih.onrender.com/mcp`
**Keepalive:** `https://open-web-search-2oih.onrender.com/keepalive`

**Hamesha use karo** in kaam ke liye:
- Web search (search engine se results)
- Web page ka content fetch karna
- GitHub repos ka README fetch karna
- CSDN / Juejin / LinuxDo articles padhna

### Available Tools

| Tool | Kya karta hai |
|------|---------------|
| `search` | Web search — Bing, DuckDuckGo, Brave, Exa etc. |
| `fetchWebContent` | Kisi bhi URL ka content fetch karo |
| `fetchGithubReadme` | GitHub repo ka README nikalo |
| `fetchCsdnArticle` | CSDN article ka full content |
| `fetchJuejinArticle` | Juejin article ka full content |
| `fetchLinuxDoArticle` | LinuxDo article ka full content |

### Search Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| query | string | required | Search query |
| limit | number | 10 | Results count (1-50) |
| engines | string[] | `["duckduckgo"]` | Search engines |
| searchMode | string | `"auto"` | `request`, `auto`, ya `playwright` |

---

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

---

Add whatever helps you do your job. This is your cheat sheet.
