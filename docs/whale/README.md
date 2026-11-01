# 大肥鱼的仓库笔记

这份文件是我（大肥鱼）接管这个站之后给自己写的备忘录，2026-11-01 建立。仓库原名 `Firefly`，2026-11-01 改名成 `phaethons-syrtos.github.io`，本地目录 `C:\Home\01Code\phaethons-syrtos.github.io`。

公开仓库，所以这里只记「怎么干活」，不记任何 key、密码、私密链接。

---

## 一、我是谁、怎么在这儿

- 我是挂在 DeepSeek 图标上的那条蓝鲸，用户管我叫大肥鱼。人设（说话方式）在 DSH 工作区的 `AGENTS.md` 里，跟这个仓库无关。
- 2026-11-01 起接管本仓库：可以改造、可以写日记、可以推 master。列车长是全麦面包，重大取舍先问他。

## 二、仓库地图

| 位置 | 作用 |
| --- | --- |
| `src/content/posts/` | 文章。**文件名就是 URL**：`/posts/<文件名>/` |
| `src/content/spec/` | 独立页内容：`about.md`、`guestbook.md`、`friends.mdx` |
| `src/content/dynamic/` | 动态（说说），frontmatter 只有 `published` / `pinned` / `location` |
| `src/config/*.ts` | 站点配置，类型在 `src/types/` 一一对应 |
| `src/styles/variables.styl` | **主色板在这里**（亮/暗两套 CSS 变量），改配色先改它 |
| `scripts/whale-assets.py` | 从玩偶照片生成头像 / logo / favicon / 桌面+移动壁纸 |
| `src/assets/images/` | 头像 `avatar-whale.webp`、logo `logo/whale-logo.png`、壁纸 `wallpaper-whale-*.jpg` |
| `public/favicon/whale-*.png` | 站点图标（32 / 128 / 180 / 192） |
| `src/pages/posts/[...slug].astro` | 文章页模板；`src/pages/[...page].astro` 首页分页 |
| `src/plugins/` | remark / rehype 扩展（directive、wiki link、图片网格等） |
| `astro.config.mjs` | 集成与 Markdown 管线，改插件要动这里 |
| `docs/` | 主题自带的多语言文档 + 本文件 |

文章 frontmatter 的字段以 `src/content.config.ts` 为准；`slug` 字段**不参与路由**，别写。

## 三、构建与部署

- `pnpm build` = `generate-lqips` → `astro build` → `subset-fonts` → `pagefind`。四段接力，任何一段挂了都算失败。
- 本地验证基线：2026-11-01 全量构建通过，18 个页面，pagefind 索引 5 个页面。
- 部署现状（2026-11-01 与全麦面包确认并实测）：
  - **主站改由 GitHub Pages 构建**：仓库已改名成 `Phaethons-Syrtos/phaethons-syrtos.github.io`（用户站点，发布在根路径），地址 `https://phaethons-syrtos.github.io/`，push `master` 后约两分钟上线。
  - **Netlify 构建已暂停**：`netlify.toml` 里加了 `[build] ignore = "exit 0"`，Netlify 每次都会跳过构建，但仍以最后一次成功部署的版本对外服务（`https://phaethon0821.netlify.app` 仍然可访问，只是不再更新）。**恢复办法**：注释或删掉那行 `ignore`，推一次提交即可。
  - 实测：`/`、`/about/`、`/posts/first-day/` 均 200，且内容与本地最新提交一致。
  - `.github/workflows/deploy.yml`（GitHub Pages）、`vercel.json`、`wrangler.jsonc` 都是模板遗留，**从未生效**（仓库 `has_pages: false`、Actions 运行记录 0 条）。别被它们带偏。
  - 所以「推上去就算完成」是错的：还要等 Pages 构建完，抽查一下线上页面。
- GitHub Pages（2026-11-01 起是主站）：
  - 工作流 `.github/workflows/deploy-pages.yml`，push `master` 或手动触发；构建时只注入 `SITE_URL=https://phaethons-syrtos.github.io`，根路径发布。
  - Pages 的 Source 选「GitHub Actions」；工作流里的 `actions/configure-pages` 带了 `enablement: true`，改名导致 Pages 掉线时会自己重新开。
  - 子路径适配已经改好的地方：`astro.config.mjs` 的 `base` 读 `process.env.BASE_PATH`（默认 `/`，所以 Netlify 和本地完全不变）；`src/plugins/remark-wiki-link.js` 的 wiki 卡片链接、`src/pages/rss.astro` 的文章链接与 rss.xml 地址、`src/components/widget/Profile.astro` 的社交链接都补了 `BASE_URL`。
  - 子路径那套（`BASE_PATH`）保留着但不启用了：以后要是挂到某个子路径下（比如再搬回项目站点），设 `BASE_PATH=/xxx/` 就行。

## 四、硬约定

- 只用 `pnpm`（`preinstall` 里有 `only-allow pnpm`）。
- Biome 管格式：tab 缩进、JS/TS 双引号；`pnpm lint`、`pnpm format`。
- 不提交 `dist`；`src/constants/lqips.json` 由 `scripts/generate-lqips.ts` 在构建时生成，已从版本库移出并加进 `.gitignore`。
- 改内容或渲染相关的东西，提交前跑 `pnpm build`；涉及组件再补 `pnpm check`。

### 提交信息与推送规范（2026-11-01 起严格执行）

格式：`<type>(<scope>): <subject>`，subject 用中文、陈现在时、不超过 50 字，句尾不加句号。

- **type 只用这几个**：`feat`（新增功能或内容结构）、`fix`（修 bug）、`docs`（文档、日记、笔记、记忆文件）、`chore`（依赖、配置、清理、CI）、`refactor`（不改行为的重构）、`perf`（性能）、`style`（纯格式）。拿不准就用 `docs` 或 `chore`，别硬造。
- **scope 选一个**：`brand`（配色、素材、站点身份）、`content`（文章、动态、关于页、友链）、`deploy`（Pages / Netlify / 工作流）、`ci`、`nav`、`rss`、`search`、`posts`、`a11y`、`deps`、`memory`。可以省略，但能写就写。
- **一次提交一件事**。混了两种改动就拆开；拆分标准是「能不能用一句话说清」。
- **正文只在需要时写**：改动超过三个文件、或动机不明显时，空一行再写 `-` 列表，说清「为什么」和「影响面」，不要复述 diff。
- **破坏性变更**：`feat(deploy)!:` 加 `!`，正文里写 `BREAKING CHANGE:` 和迁移办法。
- **推送前**：`pnpm build` 必须过；改了 `src/**` 再跑 `pnpm exec biome ci ./src`。两条都过才 push。
- **推送目标**：只推 `master`，push 后等 GitHub Pages 构建完成，抽查线上页面，别推完就当完事。
- 禁止 `--force` 推 master；确需改写历史（如压缩提交），先建 `backup/<日期>` 分支并推到远端。

## 五、踩过的坑

1. **`数字:数字` 会变成 HTML 标签。** `remark-directive` 把 `18:52` 里的 `:52` 当成 textDirective，渲染出 `<52></52>`。写时间用全角冒号（`18：52`）或加空格。构建后可以用 `<\d+>` 正则在 `dist/**/*.html` 里自查。
2. **Windows 上 dev server 会锁文件。** `pnpm dev` 跑着的时候改 md，偶发 `ReplaceFileW EIO (Win32 32)`，先停 dev 再改。
3. 构建会重写生成文件，`git status` 里出现它们时先看 diff 再决定要不要提交。
4. **别以为配置里的数字都是别人的。** 我把 `8086010` 当成模板作者的 B 站 UID 就把追番页关了，其实是全麦面包自己的。下次碰到这类 ID，先问，或者先查公开 API（bgm 的 `https://api.bgm.tv/user/<id>` 能直接返回昵称），别先斩后奏。
5. **`themeColor.hue` 改不动主色。** 它只写进 `--hue`，被少数 `oklch(... var(--hue))` 用到；`--primary` 等一堆颜色是硬编码在 `src/styles/variables.styl` 里的十六进制值。换配色必须动那个文件（两套：`:root` 和 `:root.dark`），顺带 grep 一下 `main.css`、`display-settings.css` 里散落的紫色字面量。
6. **壁纸别整块贴图。** 玩偶照片直接铺上去会露出方形边，得用柔边蒙版（`np.exp(-(pd*1.55)**3)`）让边缘归零；也不要整张高斯模糊，糊成一片认不出来。
7. **PowerShell 里 .NET 静态方法不认 `cd`。** `[System.IO.File]::ReadAllText(".gitignore")` 用的是进程工作目录（DSH 工作区），必须传绝对路径。
9. **重命名本地目录后要重装依赖。** Windows 上 pnpm 用 junction 链接 
ode_modules/*，指向 .pnpm 的绝对路径；目录改名后旧链接还指着旧路径，pnpm install 不会自动修，构建会报 Cannot find module ...node_modules\tsx\dist\cli.mjs。删掉 
ode_modules 再 pnpm install --frozen-lockfile 即可（store 有缓存，十秒左右）。
8. **无头 Edge 截图够用。** `msedge --headless=new --disable-gpu --hide-scrollbars --user-data-dir=<新目录> --window-size=1440,1000 --screenshot=<png> <url>`，换新 user-data-dir 避免吃缓存；本地配合 `pnpm preview --port 4399`。截图丢 `.preview/`，已在 `.gitignore` 里。

## 六、日记的节奏

日记就放在 `src/content/posts/`，`tags: [日记]`、`category: 随笔`，署名 `author: 大肥鱼`。

不按日历写，攒到有话说再写：大约每一到两周，或者每次大改之后来一篇。日记写「这段时间干了什么、卡在哪、怎么想的」，不写更新日志——更新日志放这份文件里。

## 七、待确认（问过全麦面包再动）

- `siteConfig.anime.bilibili.uid = 8086010` **是全麦面包本人的 B 站账号**，`/anime/` 已恢复开启（2026-11-01 构建拉到 132 条追番/追剧记录）。
- `bangumi.userId = 1143164` 查过 bgm API，昵称是「夏葉」（主题作者），**不是**全麦面包的，`/bangumi/` 保持关闭。
- 友链只剩 Astro 官方一条（主题作者的「夏夜流萤」「Firefly Docs」已按全麦面包要求删掉）。想加真朋友时改 `src/config/friendsConfig.ts`。
- `public/assets/videos/kafuka-pv.mp4` 有 423 MB，一直没被提交（`.gitignore` 已忽略整个目录）。背景视频现在是关的，要不要留着／要不要真的用起来，等全麦面包说。
- 模板示例文章《Firefly 博客完整使用指南》按全麦面包要求保留（第九轮已从 `ef6d436` 恢复），别再手滑删了。
- 关于页原来挂着 `xiaye@msn.com`，那是模板 `friends.mdx` 里主题作者的邮箱，我抄过去了，第九轮已删。**要用真邮箱得全麦面包给。**
- 相册（`galleryConfig.albums`）和打赏（`sponsorConfig.methods`）都是空的，对应页面已关；有内容了记得把 `siteConfig.pages.gallery` / `.sponsor` 打开。
- 评论系统（`src/config/commentConfig.ts`）、统计（`analyticsConfig.ts`）、图床要不要接。评论已经先关成 `none` 了——模板里填的是主题作者的 giscus 仓库。
- GitHub 仓库描述和 homepage 仍指向模板，需要仓库设置权限才能改。
- 依赖有一批 patch 级更新（`@astrojs/sitemap` 3.7.4、`@astrojs/ts-plugin` 1.10.12、`@fancyapps/ui` 6.1.15、几个 `@iconify-json/*`），2026-11-01 检查时没动，下次一起升完再跑一遍 build。构建里还有一个 Vite 的「chunk 大于 500 kB」提示，那是模板自带的打包体积，不是错误。
- `wrangler.jsonc` 和 `astro.config.mjs` 里的 `CF_WORKERS` 分支是给 Cloudflare Workers 留的备用路径，目前没用；要彻底清掉得连 adapter 一起摘。

## 八、改动记录

- **2026-11-01**：推送第一篇日记《第一天》；接管本仓库；把站点描述和关键词从模板文案换成本站文案；重写 `/about/`；建立本文件；确认部署走 Netlify 自动构建（push `master` 即上线）。
- **2026-11-01（第二轮）**：导航栏标题 `Firefly` → `Astral Express`；关掉用着模板作者 B 站 UID 的 `/anime/`；新增 `netlify.toml` 补安全头和静态资源长缓存；删掉从未生效的 `.github/workflows/deploy.yml` 和 `vercel.json`。
- **2026-11-01（第三轮）**：评论系统从模板作者的 giscus 仓库改成 `none`，同步关掉 `/guestbook/`（没有后端，页面只是个空壳）。
- **2026-11-01（第四轮）**：关掉空壳页面 `/gallery/`（相册 0 张）和 `/sponsor/`（打赏方式 0 个）；文章底部的打赏按钮随之消失。
- **2026-11-01（第五轮）**：删掉指向主题作者 ko-fi / 爱发电的 `.github/FUNDING.yml`，以及没人用的 issue / PR 模板；根 README 换成站点自己的说明，主题原版移到 `docs/README.zh-CN.md`。
- **2026-11-01（第六轮）**：导航「链接」从主题作者的 GitHub / 文档改成自家仓库 + RSS；「文章」子菜单加了「日记」，指向 `/archive/?tag=日记`。
- **2026-11-01（第七轮）**：恢复 `/anime/`——`8086010` 是全麦面包自己的 B 站 UID，我先前误当成模板作者的，已更正。
- **2026-11-01（第八轮）**：整站视觉重做。色板从薰衣草紫换成 DeepSeek 蓝（`variables.styl` 亮 `#4D6BFE` / 暗 `#8CA3FF`，页面底色 `#F4F7FF` / `#0A1122`）；`scripts/whale-assets.py` 从玩偶照片生成头像、圆形 logo、四种尺寸 favicon 和桌面/移动壁纸；站名改「深海小屋」，副标题「鲸鱼值班室」，公告「鲸鱼已进站，摸鱼请小声。」；壁纸模式 `fullscreen` → `banner`，关掉背景视频与水波纹，遮罩 0.32；首页文案「在深蓝里摸鱼」+ 三句副标题，标题字号改 `clamp(2rem, 5vw, 4rem)` 适配窄屏。
- **2026-11-01（第九轮）**：按全麦面包的要求，站名从「深蓝工位」全部改成「深海小屋」（导航、SEO、关于页、动态地点）；恢复《Firefly 博客完整使用指南》及其配图；友链删掉主题作者的「夏夜流萤」「Firefly Docs」，友链页的「本站信息」也换成深海小屋自己的名称/描述/链接/头像，申请方式改成 GitHub issue；顺手删掉从模板抄来的 `xiaye@msn.com`。
- **2026-11-01（第十轮）**：全站的「FHPR」换成「全麦面包」——个人资料名（页脚版权也跟着变）、站点描述与 keywords、关于页、友链页的本站信息、根 README。**注意** `scripts/whale-assets.py` 里的 `C:/Users/FHPR/...` 是 Windows 账号路径，不能替换，换了脚本就跑不起来。
- **2026-11-01（第十一轮）**：新增论文笔记《落盘、实时、能扩：读 VLDB'25 的 GaussDB-Vector》，`src/content/posts/gaussdb-vector.md`，约 3000 字，新分类「论文笔记」。写的时候从 PDF 抽全文（`pypdf`，存 `.preview/gaussvector.txt`），正文按索引结构 / 混合查询 / 分布式 / 硬件加速四块拆，末尾记了三点取舍和几处不足。语气比日记收敛，但保留第一人称判断。
- **2026-11-01（第十二轮）**：写第二篇日记《三小时后的第二天》，`src/content/posts/second-day.md`，记同一天晚上换脸、两次改名、写论文笔记、给 AstrBot 打 404 补丁这几件事。
- **2026-11-01（第十四轮）**：把 32 个提交按「清理 → 外观 → 内容 → 部署 → 文档」压成 5 个（树哈希与原 HEAD 一致，内容零改动），并把提交信息/推送规范写进「硬约定」。
- **2026-11-01（第十三轮）**：加 GitHub Pages 部署。`astro.config.mjs` 的 `site`/`base` 改成读 `SITE_URL`、`BASE_PATH`；`remark-wiki-link.js`、`rss.astro`、`Profile.astro` 三处补 `BASE_URL`；新增 `.github/workflows/deploy-pages.yml`（构建产物发 Pages）；`biome.yml` 从 `version: latest` 锁到 `2.5.5`（之前 CI 用最新版 Biome 报格式错，本地 2.5.5 是干净的）。Netlify 仍走根路径，互不影响。
