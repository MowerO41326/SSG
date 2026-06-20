import os
import shutil
import sys

from markdown_blocks import extract_title, markdown_to_html_node
from pathlib import Path


def main() -> None:
    copy_tree("static", "public")
    generate_pages_recursive("content", "template.html", "public")


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

    dir_name = os.path.dirname(destination_path)
    os.makedirs(dir_name, exist_ok=True)

    with open(destination_path, "w") as f:
        f.write(html_page)
    print(f'Conversion complete.  Page "{title}" created.')

def generate_pages_recursive(
    source_path: str, template_path: str, destination_path: str
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
            )
        elif os.path.isdir(old_path):
            generate_pages_recursive(old_path, template_path, new_path)
        else:
            raise Exception("Error: <item> is neither file, nor directory")


main()
