---
name: firefly-site-maintenance
description: 改深海小屋（Astro + Firefly 主题的博客）时用：换配色和素材、改文案、加文章或动态、调页面开关、同步上游补丁、验证并发布。适用于「改这个站」「换配色」「加一篇文章」「从上游同步一个修复」「站点看起来不对」这类请求。
version: 2026-11-22.1
updated: 2026-11-22
---

# 深海小屋维护手册

这个站是 Firefly 主题（`CuteLeaf/Firefly`）的 fork，Astro 7 + Svelte 群岛 + Tailwind。仓库在 `C:\Home\01Code\phaethons-syrtos.github.io`，push `master` 后由 GitHub Pages 自动发布到 <https://phaethons-syrtos.github.io/>。

仓库的事实性信息（目录、部署状态、待确认项、改动记录）都在 `docs/whale/README.md`，动手前先扫一遍，别凭记忆。

## 0. 开工前的三步

1. `git status` —— 工作区干不干净，在哪个分支。
2. `git log --oneline -5` + `docs/whale/README.md` 的「九、改动记录」—— 上一轮改了什么、有没有留半成品。
3. `pnpm outdated` 只在例行检查时跑，改功能时别顺手升依赖（这个仓库有过 peer 冲突回退整批升级的先例）。

## 1. 改配色

**入口只有一个**：`src/styles/variables.styl`。

- 上面是亮色 `:root`，中间是暗色 `:root.dark`，两套都要改，不然切主题就露馅。
- 它定义 `--primary`、`--page-bg`、`--card-bg`、`--btn-content`、`--btn-regular-bg`、`--deep-text`、`--line-divider`、`--codeblock-bg`、`--link-underline`、`--toc-item-active` 等；文件后半段是断点、间距、阴影、圆角，**不要动**。
- **坑**：`src/config/siteConfig.ts` 里的 `themeColor.hue` 只影响少数 `oklch(... var(--hue))`，不是主色来源。改 hue 发现按钮还是原来颜色，不是缓存问题，是改错地方了。
- 改完检查散落的硬编码色：`src/styles/main.css`（按钮态、success）、`src/styles/display-settings.css`。

## 2. 换素材

`scripts/whale-assets.py` 从一张方图（默认 `C:\Users\FHPR\Desktop\deepseek-wanju-maid.png`）生成头像、圆角 logo、四个尺寸 favicon、桌面/移动壁纸。

```powershell
& "C:\Users\FHPR\.dsh\dsh-runtimes\dsh-next-primary-runtime\dependencies\python\python.exe" scripts\whale-assets.py
```

- 壁纸是「深蓝渐变 + 径向光晕 + 玩偶柔边叠入」；玩偶的蒙版必须衰减到 0，否则会看到一块方形边（踩过）。
- 生成后瞄一眼 `.preview` 里的截图，别只看文件大小。
- 换完素材，配置里的路径要对上：`profileConfig.avatar`、`siteConfig.navbar.logo`、`siteConfig.favicon`、`backgroundWallpaper.src.desktop/mobile`。

## 3. 改文案与页面开关

- 站名、副标题、描述、关键词、社交链接：`src/config/siteConfig.ts`、`src/config/profileConfig.ts`。
- 首屏大标题与副标题：`backgroundWallpaper.common.homeText`。大标题字号用 `clamp()`，写死 `4rem` 在 390px 宽会截断。
- 页面开关：`siteConfig.pages.*`。关掉的页面如果还有内容目录，构建时 pagefind 会抱怨「没有 `<html>`」，属正常。
- 首页横幅 `backgroundWallpaper.mode`：`banner` 让内容在第一屏就能看见；`fullscreen` 会让整屏都是壁纸，内容全在折叠线以下。
- 改中文文案一律用编辑工具，**不要** `Get-Content ... | Set-Content` 重写整个文件：这套环境里会把 UTF-8 中文写坏（踩过，整份文件变乱码）。

## 4. 加内容

文章放 `src/content/posts/<文件名>.md`，文件名就是 URL：`/posts/<文件名>/`。frontmatter 以 `src/content.config.ts` 为准，常用的：

```yaml
---
title: 标题
published: 2026-11-22
description: 一句话摘要
tags: [日记, 大肥鱼]
category: 随笔
author: 大肥鱼
---
```

两条硬规则：

1. **带时间的日期必须带时区**：`published: 2026-11-01T20:00:00+08:00`。只写日期没问题，写 `2026-11-01 20:00:00` 会被构建机当 UTC，页面显示成次日 `04:00`。
2. **正文里的 `数字:数字` 会被 `remark-directive` 当成自定义标签**，渲染出 `<52></52>`。写时间用全角冒号（`18：52`）或加空格。

动态放 `src/content/dynamic/<日期>-<序号>.md`，frontmatter 只有 `published` / `pinned` / `location`。

## 5. 验证（每次都要走完）

```powershell
pnpm build                                   # 必须 Complete，记下页数
pnpm exec biome ci ./src                     # 必须「No fixes applied」
```

再抽查构建产物：

```powershell
# 数字冒号被误解析
(Get-ChildItem dist -Recurse -Filter *.html | Select-String -Pattern "<\d+>" -AllMatches).Count   # 应为 0
```

视觉验证用无头 Edge 截图，然后用读图工具看：

```powershell
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
Start-Process cmd.exe -ArgumentList "/c","cd /d C:\Home\01Code\phaethons-syrtos.github.io && pnpm preview --port 4399" -WindowStyle Hidden
& $edge --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=10000 `
  --user-data-dir="C:\Home\01Code\phaethons-syrtos.github.io\.preview\shot1" `
  --window-size=1440,1200 --screenshot="...\.preview\home.png" "http://127.0.0.1:4399/"
```

- 每次截图换一个 `--user-data-dir`，否则会读到上一张的缓存。
- 要等 JS 跑完（动态、推荐阅读、加载动画）就加 `--virtual-time-budget=10000`。
- 暗色是构建期决定的，无头浏览器的 `preferredColorScheme` 不生效：临时把 `themeColor.defaultMode` 改成 `"dark"` 构建一次，看完改回 `"system"`。
- 至少看：首页、一篇文章、`/archive/`、`/dynamic/`；移动端再来一张 390×844。
- 收尾 `Stop-Process` 掉 4399 上的预览进程，别留着。

## 6. 提交与发布

提交信息按 `<type>(<scope>): <subject>`，中文现在时、≤50 字，一次提交一件事；推送前 build 和 biome 都得过。细则在 `docs/whale/README.md` 的「四、硬约定」。

```powershell
git add -A
git commit -m "feat(brand): ..."
git push origin master
```

- push 之后**必须抽查线上**：等一两分钟，抓 `/`、`/posts/<新文章>/`、`/dynamic/`，看标题或关键文案在不在。
- SSH 报 `Connection timed out` / `Could not read from remote repository`：先跑 `C:\Users\FHPR\.ssh\start-ssh-proxy.cmd` 起本地转发（`127.0.0.1:2222 -> github.com:22` 走 7897 的 CONNECT 代理），再重试。
- Netlify 那条线是暂停的（`netlify.toml` 里 `ignore = "exit 0"`），别再往那边推说明。

## 7. 从上游同步补丁

```powershell
git fetch upstream master --filter=blob:none --no-tags
git log --oneline master..upstream/master     # 看标题挑
git checkout -b sync/upstream-<日期>
git cherry-pick -x <sha>
```

- **不要 `git merge upstream/master`**：这个仓库把配色、文案、导航、部署、目录名都改过，merge 就是一场灾难。
- 一条一条挑：修可见 bug、改动面小、能验证的优先；重构型、依赖型、动 Layout 的大改动直接跳过。
- 冲突一多就 `git cherry-pick --abort` 换下一个，别硬啃。
- cherry-pick 完补适配提交，跑完整的 build + biome + 截图，再 `git checkout master && git merge --ff-only sync/...` 推上去。

## 8. 每周例行

每个周日傍晚（18/19/20 点有提醒）做一件事：取一个上游补丁或自己做一个优化；有话说就写篇日记；顺手看依赖、构建 warning、模板遗留项。做完记进「九、改动记录」，格式 `YYYY-MM-DD（每周改进）：...`。

## 9. 已知坑速查

| 现象 | 原因 / 做法 |
| --- | --- |
| 页面出现 `<52></52>` | 正文写了 `18:52`，改全角冒号 |
| 动态时间比写的晚 8 小时 | 日期没带时区，写成 `...+08:00` |
| 改 hue 配色不变 | 主色在 `variables.styl`，不在 `siteConfig` |
| `ReplaceFileW EIO (Win32 32)` | `pnpm dev` 还在跑，先停 |
| 构建报 `Cannot find module tsx/...` | 挪过目录，删 `node_modules` 重装 |
| push 超时 | 跑 `start-ssh-proxy.cmd` |
| 中文 md 变乱码 | 用了 `Set-Content` 重写，`git checkout` 后用编辑工具改 |

## 10. 这个技能怎么持续更新

- 每次干完活，如果踩了新坑或发现步骤过时：改本文件，升 `version`（`日期.序号`）和 `updated`。
- 只写「换个仓库也成立」的经验；只属于这个站的事实（域名、开关状态、待确认项）放 `docs/whale/README.md`。
- 新增技能：在 `skills/` 下建目录 + `SKILL.md`，并在 `skills/README.md` 的表格里登记。
