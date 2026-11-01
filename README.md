# FHPR's Astral Express

个人站的源码。线上地址：<https://phaethon0821.netlify.app>

主题是 fork 的 [Firefly](https://github.com/CuteLeaf/Firefly)（MIT），被改成了现在这个样子：Astro 7 + Svelte 群岛 + Tailwind，静态生成，搜索用 pagefind。

## 写文章

在 `src/content/posts/` 新建 `<slug>.md`，**文件名就是 URL**（`/posts/<slug>/`）。frontmatter 的字段以 `src/content.config.ts` 为准；`slug` 字段不参与路由，别写。

一个能用的最小开头：

```yaml
---
title: 标题
published: 2026-11-01
tags: [日记]
category: 随笔
author: 大肥鱼
---
```

两个容易踩的点：

- 正文里 `数字:数字`（比如 `18:52`）会被 remark-directive 当成自定义标签，渲染出 `<52></52>`。写时间用全角冒号 `18：52`，或者中间加空格。
- `pnpm dev` 开着的时候改 md，Windows 上偶发 `ReplaceFileW EIO`，先停 dev 服务。

想写日记：`tags` 里带「日记」就行，归档页可以用 `/archive/?tag=日记` 筛出来。

## 本地开发

```bash
pnpm install
pnpm dev          # 本地预览
pnpm build        # LQIP → astro build → 字体子集 → pagefind
pnpm check        # Astro 诊断
pnpm type-check   # tsc --noEmit
pnpm lint         # Biome
```

## 目录速查

| 路径 | 说明 |
| --- | --- |
| `src/content/posts/` | 文章 |
| `src/content/spec/` | 关于、友链等独立页的内容 |
| `src/content/dynamic/` | 说说（动态） |
| `src/config/` | 站点配置，类型在 `src/types/` |
| `src/plugins/` | remark / rehype 扩展 |
| `docs/whale/` | 维护笔记（哪里改过、踩过什么坑） |

## 部署

推 `master` 触发 Netlify 自动构建，一两分钟上线；响应头写在 `netlify.toml`。

仓库里的 `.github/workflows/build.yml`、`biome.yml` 只是模板留下的检查例子，实际没在跑——别指望 CI 帮你兜底，提交前自己 `pnpm build`。

## 约定

- 只用 `pnpm`。
- Biome 管格式：tab 缩进、JS/TS 双引号。
- 提交用 Conventional Commits。
- 不提交 `dist` 和生成文件。

主题原始说明放在 `docs/README.zh-CN.md`（另有日文、繁体版本）。
