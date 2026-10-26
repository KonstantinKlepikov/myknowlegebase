"""
source_generator.py

Generates source-view pages for every note and list in the knowledge base.
For each notes/<slug>.md and lists/<slug>.md creates a flat HTML file:
    notes/<slug>.html
    lists/<slug>.html

These pages use the `markdown_source` Jekyll layout with an explicit permalink
(/notes/<slug>.html) so they are served at the same path regardless of the
global `permalink: pretty` setting.

The rendered pages (notes/<slug>.md → pretty permalink /notes/<slug>/) and
the source pages (/notes/<slug>.html) have distinct URLs and coexist cleanly.

Run before `jekyll build` or `jekyll serve` (see Makefile).
"""

import glob
import os
import re


DIRS = ["notes", "lists"]


def get_title(content: str, fallback: str) -> str:
    m = re.search(r"^title:\s*(.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip().strip('"').strip("'")
    return fallback


def clean_old_sources(directory: str) -> None:
    for path in glob.glob(os.path.join(directory, "*.html")):
        os.remove(path)


def generate_sources(directory: str) -> int:
    count = 0
    for filepath in glob.glob(os.path.join(directory, "*.md")):
        slug = os.path.splitext(os.path.basename(filepath))[0]
        with open(filepath, "r", encoding="utf-8") as f:
            raw_content = f.read()

        title = get_title(raw_content, slug)
        # With permalink:pretty, the rendered page lives at /<dir>/<slug>/
        parent_url = f"/{directory}/{slug}/"
        # Explicit permalink pins this page to /<dir>/<slug>.html regardless
        # of global permalink settings.
        permalink = f"/{directory}/{slug}.html"

        # Escape double quotes in title for YAML
        safe_title = title.replace('"', '\\"')

        output_path = os.path.join(directory, f"{slug}.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(
                f"---\n"
                f"layout: markdown_source\n"
                f'title: "Source: {safe_title}"\n'
                f'parent_url: "{parent_url}"\n'
                f'permalink: "{permalink}"\n'
                f"render_with_liquid: false\n"
                f"robots: noindex\n"
                f"---\n"
                f"{raw_content}"
            )
        count += 1
    return count


if __name__ == "__main__":
    total = 0
    for d in DIRS:
        clean_old_sources(d)
        n = generate_sources(d)
        total += n
        print(f"{d}: {n} source pages generated")
    print(f"Total source pages generated: {total}")
