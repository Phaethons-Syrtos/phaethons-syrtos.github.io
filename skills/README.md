# skills

这个目录放「可复用的操作手册」——不是仓库说明，是**下次做同类事情时可以直接照着走的步骤**。

- 每个技能一个子目录，里面至少一个 `SKILL.md`。
- `SKILL.md` 开头是 YAML frontmatter：

  ```yaml
  ---
  name: 技能标识（小写、连字符）
  description: 一句话说清「什么时候该用这个技能」
  version: 2026-11-22.1
  updated: 2026-11-22
  ---
  ```

- 正文写成「先看什么 → 怎么做 → 怎么验证 → 怎么回滚」，多写具体命令和路径，少写道理。
- **仓库特有的事实**（域名、分支、部署状态、待确认项）以 `docs/whale/README.md` 为准，技能里引用它，不要复制一份会过期的副本。
- 每次用完一个技能，如果发现漏了坑或步骤不对，顺手改掉并升 `version` / `updated`——技能是活文档。

## 已有技能

| 技能 | 用途 |
| --- | --- |
| [`firefly-site-maintenance`](firefly-site-maintenance/SKILL.md) | 改这个 Astro/Firefly 博客的配色、文案、页面，加内容，验证并发布上线 |
