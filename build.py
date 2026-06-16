from pathlib import Path
import markdown
import shutil

MD_DIR = Path("md")
DOCS_DIR = Path("docs")
TEMPLATES_DIR = Path("templates")

# -----------------------------
# Очистка docs
# -----------------------------

if DOCS_DIR.exists():
    shutil.rmtree(DOCS_DIR)

DOCS_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Шаблоны
# -----------------------------

PAGE_TEMPLATE = (
    TEMPLATES_DIR / "page.html"
).read_text(encoding="utf-8")

INDEX_TEMPLATE = (
    TEMPLATES_DIR / "index.html"
).read_text(encoding="utf-8")

# -----------------------------
# Дерево навигации
# -----------------------------

tree = {}

# -----------------------------
# Генерация страниц
# -----------------------------

for md_file in MD_DIR.rglob("*.md"):

    rel_path = md_file.relative_to(MD_DIR)

    output_file = DOCS_DIR / rel_path.with_suffix(".html")

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    md_text = md_file.read_text(
        encoding="utf-8"
    )

    html_content = markdown.markdown(
        md_text,
        extensions=[
            "extra",
            "tables",
            "toc",
            "pymdownx.superfences",
            "pymdownx.highlight",
        ]
    )

    page_html = (
        PAGE_TEMPLATE
        .replace("{{title}}", md_file.stem)
        .replace("{{content}}", html_content)
    )

    output_file.write_text(
        page_html,
        encoding="utf-8"
    )

    # дерево для index

    node = tree

    for part in rel_path.parts[:-1]:
        node = node.setdefault(part, {})

    node.setdefault(
        "__files__",
        []
    ).append(md_file.stem)

# -----------------------------
# Рендер дерева
# -----------------------------

def render_tree(tree, prefix=""):

    html = ""

    folders = sorted(
        k for k in tree.keys()
        if k != "__files__"
    )

    for folder in folders:

        html += f"""
<details
class="
bg-white
border
border-slate-200
rounded-xl
shadow-sm
mb-3
"
open>

<summary
class="
cursor-pointer
font-semibold
p-4
select-none
"
>
📁 {folder}
</summary>

<div class="px-4 pb-4">

{render_tree(
tree[folder],
prefix + folder + "/"
)}

</div>

</details>
"""

    for file_name in sorted(
        tree.get("__files__", [])
    ):

        html += f"""
<a
href="{prefix}{file_name}.html"
class="
block
py-2
px-3
rounded-lg
hover:bg-slate-100
transition
"
>
📄 {file_name}
</a>
"""

    return html

# -----------------------------
# Главная страница
# -----------------------------

count = len(
    list(MD_DIR.rglob("*.md"))
)

index_html = (
    INDEX_TEMPLATE
    .replace(
        "{{content}}",
        render_tree(tree)
    )
    .replace(
        "{{count}}",
        str(count)
    )
)

(DOCS_DIR / "index.html").write_text(
    index_html,
    encoding="utf-8"
)

print(
    f"✓ Build complete ({count} pages)"
)