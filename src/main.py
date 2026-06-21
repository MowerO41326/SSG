import os
import shutil
import sys

from markdown_blocks import extract_title, markdown_to_html_node
from pathlib import Path


source_path = "content"
destination_path = "docs"
static_path = "static"
template_path = "template.html"
default_basepath = "/"


def main() -> None:
    basepath = default_basepath
    if len(sys.argv) > 2:
        print("Error: too many arguments")
        print("Usage: python3 main.py <source_path>")
        sys.exit(1)
    else:
        basepath = sys.argv[1]

    copy_tree(static_path, destination_path)
    generate_pages_recursive(source_path, template_path, destination_path, basepath)


def copy_tree(source: str, destination: str) -> None:
    """
    Delete <destination> and copy contents of <source> to <destination>.
    """
    print(f"Deleting contents of: {destination}...")
    
    if os.path.exists(destination):
        shutil.rmtree(destination)
        print(f"Deletion of {destination} contents successful.")
    
    os.mkdir(destination)

    print(f"Copying contents of {source} to {destination}...")
    
    dir_contents = os.listdir(path=source)

    for item in dir_contents:
        old_path = os.path.join(source, item)
        new_path = os.path.join(destination, item)
        if os.path.isfile(old_path):
            print(f"Copying file: {old_path} to {new_path}")
            shutil.copy(old_path, new_path)
        elif os.path.isdir(old_path):
            print(f"Creating directory: {item}")
            os.mkdir(new_path)
            copy_tree(old_path, new_path)
        else:
            raise Exception(
                "Error: <item> is neither file, nor directory"
            )


def generate_page(
    source_path: str | Path, 
    template_path: str, 
    destination_path: str | Path, 
    basepath: str, 
) -> None:
    """
    Generate HTML page from markdown file using template.
    """
    print(
        f"Converting {source_path} to {destination_path}"
    )
    with open(source_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    title = extract_title(markdown)
    node = markdown_to_html_node(markdown)
    article = node.to_html()

    html_page = template.replace("{{ Title }}", title)
    html_page = html_page.replace("{{ Content }}", article)
    html_page = html_page.replace('href="/', f'href="{basepath}')
    html_page = html_page.replace('src="/', f'src="{basepath}')

    dir_name = os.path.dirname(destination_path)
    os.makedirs(dir_name, exist_ok=True)

    with open(destination_path, "w") as f:
        f.write(html_page)
    print(f'Conversion complete.  Page "{title}" created.')

def generate_pages_recursive(
    source_path: str, 
    template_path: str, 
    destination_path: str, 
    basepath: str, 
) -> None:
    """
    Generate HTML pages from markdown files using template, recursively.
    """
    print(f"Generating pages from {source_path}...")

    dir_contents = os.listdir(path=source_path)

    for item in dir_contents:
        old_path = Path(source_path) / item
        new_path = Path(destination_path) / item

        if os.path.isfile(old_path):
            generate_page(
                old_path, 
                template_path, 
                new_path.with_suffix(".html"), 
                basepath, 
            )
        elif os.path.isdir(old_path):
            generate_pages_recursive(old_path, template_path, new_path, basepath)
        else:
            raise Exception("Error: <item> is neither file, nor directory")


main()
