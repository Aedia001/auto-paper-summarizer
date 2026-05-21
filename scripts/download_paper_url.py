#!/usr/bin/env python3
"""Download a paper PDF from a direct PDF URL or a paper page URL."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download a paper PDF from a URL.")
    parser.add_argument("--url", required=True, help="Paper URL or direct PDF URL.")
    parser.add_argument("--output-dir", required=True, help="Directory to write the downloaded PDF into.")
    parser.add_argument("--filename", default="", help="Optional output filename. Defaults to paper.pdf.")
    parser.add_argument(
        "--user-agent",
        default="codex-paper-downloader/1.0 (local skill)",
        help="HTTP user agent.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Request timeout in seconds.",
    )
    return parser.parse_args()


def maybe_rewrite_arxiv(url: str) -> str:
    if "arxiv.org/abs/" in url:
        base = url.split("#", 1)[0].split("?", 1)[0]
        paper_id = base.rsplit("/", 1)[-1]
        return f"https://arxiv.org/pdf/{paper_id}.pdf"
    return url


def derive_filename(url: str, explicit: str) -> str:
    if explicit.strip():
        return explicit.strip()
    parsed = urlparse(url)
    name = Path(parsed.path).name
    if name.lower().endswith(".pdf") and name:
        return name
    return "paper.pdf"


def guess_title_from_url(url: str) -> str:
    parsed = urlparse(url)
    tail = Path(parsed.path).stem
    tail = re.sub(r"[-_]+", " ", tail).strip()
    return tail or "paper"


def main() -> None:
    args = parse_args()
    source_url = args.url.strip()
    final_url = maybe_rewrite_arxiv(source_url)

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = derive_filename(final_url, args.filename)
    output_path = output_dir / filename

    req = Request(final_url, headers={"User-Agent": args.user_agent})
    with urlopen(req, timeout=args.timeout) as resp:
        content = resp.read()

    output_path.write_bytes(content)

    metadata_path = output_dir / "metadata.md"
    lines = [
        f"- **Source URL**: {source_url}",
        f"- **Resolved Download URL**: {final_url}",
        f"- **Local PDF**: {output_path}",
        f"- **Inferred Title Hint**: {guess_title_from_url(final_url)}",
    ]
    metadata_path.write_text("\n".join(lines) + "\n")

    print(
        json.dumps(
            {
                "ok": True,
                "source_url": source_url,
                "download_url": final_url,
                "output_path": str(output_path),
                "metadata_path": str(metadata_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
