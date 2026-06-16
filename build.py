from pathlib import Path
import markdown
import os

MD_DIR = Path("md")
OUT_DIR = Path("docs")

OUT_DIR.mkdir(exist_ok=True)

# ---------- helpers ----------

def rel_path(file: Path):
    return str(file.relative_to(MD_DIR)).replace("\\", "/")

def html_template(title, content, nav_html, breadcrumb):
    return f"""
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<title>{title}</title>

<style>
body {{
  background: #f8f9fa;
}}

.wrapper {{
  display: flex;
  gap: 40px;
}}

.sidebar {{
  width: 260px;
  position: sticky;
  top: 20px;
  height: fit-content;
}}

.content {{
  flex: 1;
  max-width: 900px;
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 18px rgba(0,0,0,0.05);
}}

pre {{
  background: #f1f3f5;
  padding: 12px;
  border-radius: 8px;
}}

code {{
  font-family: ui-monospace, Menlo, monospace;
}}

a {{
  text-decoration: none;
}}

.breadcrumbs {{
  font-size: 14px;
  margin-bottom: 20px;
  color: #6c757d;
}}

.dark {{
  background: #111;
  color: #ddd;
}}

.dark .content {{
  background: #1c1c1c;
  color: #ddd;
}}

.toggle {{
  position: fixed;
  top: 20px;
  right: 20px;
}}
</style>

</head>

<body>

<button class="btn btn-sm btn-outline-secondary toggle" onclick="toggleTheme()">
  🌓
</button>

<div class="container wrapper">

<div class="sidebar">
  <h5>📚 Skillmatrix</h5>
  <hr>
  {nav_html}
</div>

<div class="content">

<div class="breadcrumbs">{breadcrumb}</div>

{content}

</div>

</div>

<script>
function toggleTheme() {{
  document.body.classList.toggle('dark');
}}
</script>

</body>
</html>
"""

# ---------- scan md ----------

files = list(MD_DIR.rglob("*.md"))

nav_items = []

for f in files:
    nav_items.append((rel_path(f), f.stem))

def build_nav(current=None):
    html = "<ul class='list-unstyled'>"
    for path, name in nav_items:
        link = path.replace(".md", ".html")
        active = "fw-bold" if current == path else ""
        html += f"<li><a class='{active}' href='{link}'>{name}</a></li>"
    html += "</ul>"
    return html

# ---------- build pages ----------

for f in files:
    md_text = f.read_text(encoding="utf-8")
    html = markdown.markdown(md_text, extensions=["fenced_code", "tables"])

    rel = rel_path(f)
    out_file = OUT_DIR / rel.replace(".md", ".html")

    out_file.parent.mkdir(parents=True, exist_ok=True)

    breadcrumb = f"Home / {rel.replace('.md','')}"

    page = html_template(
        title=f.stem,
        content=html,
        nav_html=build_nav(rel),
        breadcrumb=breadcrumb
    )

    out_file.write_text(page, encoding="utf-8")

# ---------- index ----------

index_html = html_template(
    title="Skillmatrix",
    content="<h1>📚 Skillmatrix</h1><p>Welcome.</p>",
    nav_html=build_nav(),
    breadcrumb="Home"
)

(OUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

print("Done → /docs")