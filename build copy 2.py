from pathlib import Path
import markdown
import shutil

MD_DIR = Path("md")
DOCS_DIR = Path("docs")
TEMPLATES_DIR = Path("templates")

# -----------------------------------------
# Очистка docs
# -----------------------------------------

if DOCS_DIR.exists():
    shutil.rmtree(DOCS_DIR)

DOCS_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------
# Шаблон
# -----------------------------------------

PAGE_TEMPLATE = (
    TEMPLATES_DIR / "page.html"
).read_text(encoding="utf-8")

# -----------------------------------------
# Строим дерево
# -----------------------------------------

tree = {}

all_pages = []

for md_file in MD_DIR.rglob("*.md"):

    rel_path = md_file.relative_to(MD_DIR)

    html_path = rel_path.with_suffix(".html")

    all_pages.append(str(html_path).replace("\\", "/"))

    node = tree

    for part in rel_path.parts[:-1]:
        node = node.setdefault(part, {})

    node.setdefault(
        "__files__",
        []
    ).append(md_file.stem)

# -----------------------------------------
# Sidebar
# -----------------------------------------

def render_sidebar(
    tree,
    current_page,
    root,
    prefix=""
):
    html = ""

    folders = sorted(
        k for k in tree.keys()
        if k != "__files__"
    )

    for folder in folders:

        html += f"""
<details open class="mb-2">

<summary
class="
cursor-pointer
font-semibold
py-1
"
>
📁 {folder}
</summary>

<div class="ml-4">
{render_sidebar(
tree[folder],
current_page,
root,
prefix + folder + "/"
)}
</div>

</details>
"""

    for file_name in sorted(
        tree.get("__files__", [])
    ):

        page = prefix + file_name + ".html"

        active = ""

        if page == current_page:
            active = """
bg-blue-100
text-blue-700
rounded
px-2
"""

        html += f"""
<a
href="{root}{page}"
class="
block
py-1
hover:text-blue-600
{active}
"
>
📄 {file_name}
</a>
"""

    return html

# -----------------------------------------
# Breadcrumbs
# -----------------------------------------

def render_breadcrumbs(
    rel_path,
    root
):

    parts = rel_path.parts

    crumbs = [
        f'<a href="{root}index.html" class="hover:text-slate-900">SkillMatrix</a>'
    ]

    for part in parts[:-1]:
        crumbs.append(part)

    crumbs.append(rel_path.stem)

    return " <span class='mx-2'>›</span> ".join(crumbs)

# -----------------------------------------
# Генерация статей
# -----------------------------------------

count = 0

for md_file in MD_DIR.rglob("*.md"):

    count += 1

    rel_path = md_file.relative_to(MD_DIR)

    html_rel = rel_path.with_suffix(".html")

    output_file = DOCS_DIR / html_rel

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    depth = len(rel_path.parts) - 1

    root = "../" * depth

    current_page = str(
        html_rel
    ).replace("\\", "/")

    sidebar = render_sidebar(
        tree,
        current_page,
        root
    )

    breadcrumbs = render_breadcrumbs(
        rel_path,
        root
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
        .replace(
            "{{title}}",
            md_file.stem
        )
        .replace(
            "{{sidebar}}",
            sidebar
        )
        .replace(
            "{{breadcrumbs}}",
            breadcrumbs
        )
        .replace(
            "{{content}}",
            html_content
        )
        .replace(
            "{{root}}",
            root
        )
    )

    output_file.write_text(
        page_html,
        encoding="utf-8"
    )

# -----------------------------------------
# Главная
# -----------------------------------------

sidebar = render_sidebar(
    tree,
    "",
    ""
)

content = f"""
<h1>SkillMatrix</h1>

<p>Библиотека честного опыта.</p>

<p><strong>{count}</strong> заметок.</p>
"""

index_html = (
    PAGE_TEMPLATE
    .replace(
        "{{title}}",
        "SkillMatrix"
    )
    .replace(
        "{{sidebar}}",
        sidebar
    )
    .replace(
        "{{breadcrumbs}}",
        "Главная"
    )
    .replace(
        "{{content}}",
        content
    )
    .replace(
        "{{root}}",
        ""
    )
)

(
    DOCS_DIR / "index.html"
).write_text(
    index_html,
    encoding="utf-8"
)

print(f"✓ Build complete ({count} pages)")