# auto-paper-summarizer

这是一个用于“读论文 + 生成中文总结 + 发布到 Notion”的 skill。

## 使用方法
```bash
git clone https://github.com/Aedia001/auto-paper-summarizer.git
mv ‘skill_path’ ~/.codex/skills/
```

## 这个 skill 在干什么

这个 skill 主要负责两件事：

1. 读取论文并生成总结
2. 把总结整理成结构化 Notion 页面

它适合以下输入场景：

- 直接给一个本地 PDF 路径，例如 `paper.pdf` 给一个 arXiv 链接
- “把这篇论文总结一下，并同步到 Notion”

## 它会怎么工作

整体流程大致如下：

1. 识别输入来源
   - 如果你给的是本地 PDF，就直接读取
   - 如果你给的是 URL，就先下载论文到本地目录
2. 阅读论文内容
   - 优先基于论文原文理解，不靠脚本拼接摘要
   - 如果能拿到 arXiv source，会优先利用 source 辅助理解
3. 生成 `summary.md`
   - 默认输出中文
   - 使用统一格式写出简洁版论文总结
4. 发布到 Notion
   - 创建一个以论文标题命名的页面
   - 页面里会放论文摘要、关键信息、来源链接或本地路径

## 输出结果

默认会产出两份内容：

- 本地 `summary.md`
- 一篇 Notion 页面

`summary.md` 通常会包含这些部分：

- 一句话总结这篇论文在做什么
- 论文发布时间或最早公开时间
- `**研究动机**`
- `**创新点**`
- `**方法**`
- `**结果**`
- `缺点`

如果论文信息足够完整，也会附带：

- 论文标题
- 作者
- ArXiv ID
- 主分类
- 代码仓库或项目链接

## Notion 账号需要准备什么

要让这个 skill 正常把结果发到 Notion，你需要先准备好 Notion MCP 连接能力。最少需要以下几步：

1. 有一个可正常登录的 Notion 账号
2. 这个账号对目标页面或目标数据库有编辑权限
3. 在本机给 Codex 配置 Notion MCP

按 `SKILL.md` 里的要求，准备步骤是：

```bash
codex mcp add notion --url https://mcp.notion.com/mcp
codex --enable rmcp_client
codex mcp login notion
```

## Notion 使用前提

在实际写入 Notion 前，最好提前确认下面几件事：

- 你已经登录正确的 Notion 工作区
- 你希望写入的页面或数据库，当前账号确实可编辑
- 如果你要写进指定页面，最好提前提供 page URL 或 page ID
- 如果你要写进指定数据库，最好提前提供 database / data source 信息

如果没有指定目标位置，这个 skill 会默认创建一篇独立的私有 Notion 页面。

## 适合的使用方式

你可以这样使用它：

- 给本地文件：`/path/to/paper.pdf`
- 给 arXiv 页面：`https://arxiv.org/abs/xxxx.xxxxx`
- 直接要求：帮我总结这篇论文并发到 Notion

## 仓库里的辅助文件

- `SKILL.md`
  - skill 的主说明，定义了输入、输出、总结格式、Notion 发布流程
- `references/summary-format.md`
  - 摘要分析与写作规范
- `references/summary-example-zh.md`
  - 中文摘要风格示例
- `scripts/download_paper_url.py`
  - 下载通用论文 URL / PDF
- `scripts/download_arxiv_pdf.py`
  - 下载 arXiv PDF
- `scripts/download_arxiv_source.py`
  - 下载 arXiv 源文件

## 一句话说明

这个 skill 的作用，就是把“拿到一篇论文”这件事，自动串成一条流程：

`论文链接/文件 -> 阅读与总结 -> 生成 summary.md -> 发布到 Notion`
