from pathlib import Path
import markdown

MD_DIR = Path("md")
HTML_DIR = Path("html")

HTML_DIR.mkdir(exist_ok=True)

template = Path("templates/page.html").read_text(encoding="utf-8")

for md_file in MD_DIR.glob("*.md"):
    md_text = md_file.read_text(encoding="utf-8")

    html_content = markdown.markdown(
        md_text,
        extensions=[
            "fenced_code",
            "tables",
        ],
    )

    html = (
        template
        .replace("{{title}}", md_file.stem)
        .replace("{{content}}", html_content)
    )

    output_file = HTML_DIR / f"{md_file.stem}.html"
    output_file.write_text(html, encoding="utf-8")

    print(f"Generated {output_file}")