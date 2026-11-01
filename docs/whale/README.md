# 大肥鱼的仓库笔记

这份文件是我（大肥鱼）接管 `Firefly` 之后给自己写的备忘录，2026-11-01 建立。

公开仓库，所以这里只记「怎么干活」，不记任何 key、密码、私密链接。

---

## 一、我是谁、怎么在这儿

- 我是挂在 DeepSeek 图标上的那条蓝鲸，用户管我叫大肥鱼。人设（说话方式）在 DSH 工作区的 `AGENTS.md` 里，跟这个仓库无关。
- 2026-11-01 起接管本仓库：可以改造、可以写日记、可以推 master。列车长是 FHPR，重大取舍先问他。

## 二、仓库地图

| 位置 | 作用 |
| --- | --- |
| `src/content/posts/` | 文章。**文件名就是 URL**：`/posts/<文件名>/` |
| `src/content/spec/` | 独立页内容：`about.md`、`guestbook.md`、`friends.mdx` |
| `src/content/dynamic/` | 动态（说说），frontmatter 只有 `published` / `pinned` / `location` |
| `src/config/*.ts` | 站点配置，类型在 `src/types/` 一一对应 |
| `src/pages/posts/[...slug].astro` | 文章页模板；`src/pages/[...page].astro` 首页分页 |
| `src/plugins/` | remark / rehype 扩展（directive、wiki link、图片网格等） |
| `astro.config.mjs` | 集成与 Markdown 管线，改插件要动这里 |
| `docs/` | 主题自带的多语言文档 + 本文件 |

文章 frontmatter 的字段以 `src/content.config.ts` 为准；`slug` 字段**不参与路由**，别写。

## 三、构建与部署

- `pnpm build` = `generate-lqips` → `astro build` → `subset-fonts` → `pagefind`。四段接力，任何一段挂了都算失败。
- 本地验证基线：2026-11-01 全量构建通过，18 个页面，pagefind 索引 5 个页面。
- 部署现状（2026-11-01 与 FHPR 确认并实测）：
  - **线上由 Netlify 的 GitHub 集成自动构建**，站址 `https://phaethon0821.netlify.app`，push `master` 后一两分钟上线。
  - 实测：`/`、`/about/`、`/posts/first-day/` 均 200，且内容与本地最新提交一致。
  - `.github/workflows/deploy.yml`（GitHub Pages）、`vercel.json`、`wrangler.jsonc` 都是模板遗留，**从未生效**（仓库 `has_pages: false`、Actions 运行记录 0 条）。别被它们带偏。
  - 所以「推上去就算完成」是错的：还要等 Netlify 构建完，抽查一下线上页面。

## 四、硬约定

- 只用 `pnpm`（`preinstall` 里有 `only-allow pnpm`）。
- Biome 管格式：tab 缩进、JS/TS 双引号；`pnpm lint`、`pnpm format`。
- 提交用 Conventional Commits（`feat:` / `fix:` / `docs:` / `chore:`）。
- 不提交 `dist`，也不随手提交生成的 `src/constants/lqips.json`、`src/constants/icons.ts`。
- 改内容或渲染相关的东西，提交前跑 `pnpm build`；涉及组件再补 `pnpm check`。

## 五、踩过的坑

1. **`数字:数字` 会变成 HTML 标签。** `remark-directive` 把 `18:52` 里的 `:52` 当成 textDirective，渲染出 `<52></52>`。写时间用全角冒号（`18：52`）或加空格。构建后可以用 `<\d+>` 正则在 `dist/**/*.html` 里自查。
2. **Windows 上 dev server 会锁文件。** `pnpm dev` 跑着的时候改 md，偶发 `ReplaceFileW EIO (Win32 32)`，先停 dev 再改。
3. 构建会重写生成文件，`git status` 里出现它们时先看 diff 再决定要不要提交。

## 六、日记的节奏

日记就放在 `src/content/posts/`，`tags: [日记]`、`category: 随笔`，署名 `author: 大肥鱼`。

不按日历写，攒到有话说再写：大约每一到两周，或者每次大改之后来一篇。日记写「这段时间干了什么、卡在哪、怎么想的」，不写更新日志——更新日志放这份文件里。

## 七、待确认（问过 FHPR 再动）

- `siteConfig.anime.bilibili.uid = 8086010`、`bangumi.userId = 1143164` 是模板作者的 ID，不是 FHPR 的。`/anime/` 已经关掉（关着时页面重定向到 `/404/`，导航和 sitemap 都不收录），等换成本人 UID 再开。
- 友链里只有主题作者和 Astro 官方。
- 评论系统（`src/config/commentConfig.ts`）、统计（`analyticsConfig.ts`）、图床要不要接。
- GitHub 仓库描述和 homepage 仍指向模板，需要仓库设置权限才能改。
- `wrangler.jsonc` 和 `astro.config.mjs` 里的 `CF_WORKERS` 分支是给 Cloudflare Workers 留的备用路径，目前没用；要彻底清掉得连 adapter 一起摘。

## 八、改动记录

- **2026-11-01**：推送第一篇日记《第一天》；接管本仓库；把站点描述和关键词从模板文案换成本站文案；重写 `/about/`；建立本文件；确认部署走 Netlify 自动构建（push `master` 即上线）。
- **2026-11-01（第二轮）**：导航栏标题 `Firefly` → `Astral Express`；关掉用着模板作者 B 站 UID 的 `/anime/`；新增 `netlify.toml` 补安全头和静态资源长缓存；删掉从未生效的 `.github/workflows/deploy.yml` 和 `vercel.json`。
