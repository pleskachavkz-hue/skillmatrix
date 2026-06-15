from pathlib import Path
import re
import markdown

MD_DIR = Path("md")
HTML_DIR = Path("docs")

HTML_DIR.mkdir(exist_ok=True)

page_template = Path("templates/page.html").read_text(
    encoding="utf-8"
)

index_template = Path("templates/index.html").read_text(
    encoding="utf-8"
)

pages = []

for md_file in sorted(MD_DIR.glob("*.md")):
    md_text = md_file.read_text(encoding="utf-8")

    # Первый H1 используется как заголовок страницы
    title_match = re.search(
        r"^#\s+(.+)$",
        md_text,
        re.MULTILINE
    )

    title = (
        title_match.group(1).strip()
        if title_match
        else md_file.stem.replace("-", " ").replace("_", " ").title()
    )

    html_content = markdown.markdown(
        md_text,
        extensions=[
            "fenced_code",
            "tables",
        ],
    )

    html = (
        page_template
        .replace("{{title}}", title)
        .replace("{{content}}", html_content)
    )

    output_file = HTML_DIR / f"{md_file.stem}.html"

    output_file.write_text(
        html,
        encoding="utf-8"
    )

    pages.append(
        {
            "slug": md_file.stem,
            "title": title,
        }
    )

    print(f"Generated {output_file}")

# ---------- index.html ----------

links = "\n".join(
    f"""
<li>
    <a
        href="{page['slug']}.html"
        class="block rounded-xl border border-zinc-200 bg-white p-5 hover:border-zinc-400 hover:shadow-sm transition"
    >
        <div class="text-lg font-semibold">
            {page['title']}
        </div>
    </a>
</li>
"""
    for page in pages
)

index_html = index_template.replace(
    "{{links}}",
    links
)

(HTML_DIR / "index.html").write_text(
    index_html,
    encoding="utf-8"
)

print("Generated docs/index.html")
print(f"Generated {len(pages)} pages")