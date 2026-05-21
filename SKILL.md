---
name: arivx_paper_summarize
description: Use when the user wants a paper summarized from either a local `paper.pdf` path or a paper URL, then published to Notion. Download the paper if the input is a link, read and understand the paper using the arXiv-paper-processor style workflow, write `summary.md` using the unified Chinese summary spec, and publish the result to Notion as a structured page.
---

# Arivx Paper Summarize

This skill combines two jobs:

1. Read and summarize a paper from a local PDF path or a URL.
2. Publish the resulting summary into Notion.

Use this skill when the user gives:

- a local paper file such as `/path/to/paper.pdf`
- an arXiv abstract or PDF URL
- a generic PDF URL
- a request to summarize a paper and store the result in Notion

## Output Contract

Always produce both outputs unless the user explicitly asks for only one:

- a local `summary.md`
- a Notion page containing the structured summary

## Input Handling

### Case 1: Local PDF path

- Use the provided file directly.
- Write `summary.md` next to the PDF unless the user specifies another location.

### Case 2: URL

- If it is an arXiv URL, prefer the bundled arXiv download scripts when the target workflow expects a paper directory.
- If it is a direct PDF URL or other paper URL, use `scripts/download_paper_url.py`.
- Download into a paper-specific directory before reading.
- If network access fails under sandbox restrictions, rerun with escalation instead of silently giving up.

## Recommended Local Layout

For URL-driven runs, create a paper directory like:

```text
<run_dir>/<paper_slug>/
  paper.pdf
  metadata.md
  summary.md
```

For a local PDF path, keep the PDF in place and create:

```text
<pdf_dir>/summary.md
```

## Reading and Summarization Rules

Follow the same reading discipline as `arxiv-paper-processor`.

- Scripts are only for artifact download and trace logs.
- Do not auto-generate the prose summary using regex extraction, template autofill, or script-written section text.
- Read the paper content manually from source or PDF.
- Prefer source files when available; otherwise use the PDF.
- If metadata is missing, infer only what is directly supported by the PDF metadata or paper front matter.
- If a detail is unclear, say so explicitly instead of guessing.

## Unified Summary Spec

Use `references/summary-format.md` as the single source of truth.

Required behavior:

- First analyze the paper using the analysis framework in `summary-format.md`.
- Then write the final user-facing result using the output rules in the same file.
- In other words: one file defines both how to think and how to write.
- When writing Chinese output, explicitly use `references/summary-example-zh.md` as the style reference unless the user requests a different style.

## Required Summary Output

By default, write `summary.md` in the concise presentation style required by `references/summary-format.md`.

The output should include:

- one plain-language one-sentence summary
- publication status if published, otherwise the earliest public release time
- concise sections for `**研究动机**`, `**创新点**`, `**方法**`, `**结果**`, and `缺点`
- when suitable, optional front-matter fields such as `代码:` or project links, matching the style in `references/summary-example-zh.md`

Formatting requirements:

- `**研究动机**`, `**创新点**`, `**方法**`, and `**结果**` must be bold labels.
- Do not use ordered lists for those sections.
- Keep the wording brief, readable, and information-dense.
- Still ground the content in full-text reading rather than snippet extraction.
- Prefer the paragraph rhythm, section ordering, and density shown in `references/summary-example-zh.md`.

If the user explicitly asks for the older fixed 10-section format, you may output that instead. Otherwise the concise unified-format output is the default.

## Metadata Requirements

Even when the final output uses the concise presentation, still extract and preserve these metadata fields during analysis:

- `ArXiv ID`
- `Title`
- `Authors`
- `Publish date`
- `Primary category`
- `Reading basis`

If the paper is not from arXiv and no arXiv ID exists, use `ArXiv ID: N/A`.

## Language

- Accept a workflow language such as `English` or `Chinese`.
- The entire `summary.md` and the Notion page content must use that language.

## Notion Workflow

Use `notion-research-documentation` conventions, but this skill is paper-specific rather than multi-source research.

### 0) MCP readiness

If Notion MCP is not connected, stop and tell the user to set it up:

1. `codex mcp add notion --url https://mcp.notion.com/mcp`
2. Enable RMCP client in config or launch with `codex --enable rmcp_client`
3. `codex mcp login notion`

### 1) Determine the Notion target

Before creating the page, determine whether the user gave:

- a target page ID or page URL
- a target database/data source
- no target at all

If no target is given, create a standalone private Notion page.

### 2) Create the Notion page

Create a page whose title is the paper title. The page content should contain:

- a short top summary
- the concise sections defined by `references/summary-format.md`
- the source PDF path or URL
- the reading basis used

If useful, include a short metadata block near the top:

- Title
- Authors
- Publish date
- ArXiv ID
- Primary category
- Source

### 3) Update existing pages when appropriate

If the user provides an existing Notion page for the paper, update that page instead of creating a duplicate.

### 4) Citations and links

- Link the source URL when one exists.
- If the source is a local PDF path only, mention the local path in the page body.
- Keep claims grounded in the paper itself; do not fabricate external citations.

## Suggested Workflow

1. Normalize the user input into either a local PDF path or a downloaded local PDF.
2. Extract metadata from the PDF front matter or metadata fields.
3. Read the paper and analyze it with `references/summary-format.md`.
4. Draft `summary.md` using `references/summary-format.md` unless the user explicitly asks for the 10-section format.
5. Create or update the Notion page with the same summary.
6. Return the local summary path and the Notion page URL or ID.

## Bundled Scripts

- `scripts/download_paper_url.py`: generic PDF or paper URL downloader.
- `scripts/download_arxiv_source.py`: arXiv source downloader.
- `scripts/download_arxiv_pdf.py`: arXiv PDF downloader.
- `scripts/download_papers_batch.py`: batch arXiv artifact downloader.

## References

- `references/summary-format.md`: unified analysis and writing specification.
- `references/summary-example-zh.md`: primary Chinese style reference.
