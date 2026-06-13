import re

from textnode import TextNode, TextType


def text_to_textnodes(text: str) -> list[TextNode]:
    """
    Convert raw markdown text into a list of TextNode objects.
    """
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_links(new_nodes, TextType.IMAGE)
    new_nodes = split_nodes_links(new_nodes, TextType.LINK)

    return new_nodes


def split_nodes_delimiter(
        old_nodes: list[TextNode], 
        delimiter: str, 
        text_type: TextType
    ) -> list[TextNode]:
    """
    Split text nodes on a markdown delimiter; convert delimited text.            
    """

    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            delimited_strings = old_node.text.split(delimiter)
            if len(delimited_strings) % 2 == 0:
                raise ValueError(f"Invalid markdown: unmatched {delimiter!r} delimiter")
            for i, text in enumerate(delimited_strings):
                if text == "":
                    continue
                new_node_type = TextType.TEXT if i % 2 == 0 else text_type
                new_nodes.append(TextNode(text, new_node_type))

    return new_nodes


def split_nodes_links(
        old_nodes: list[TextNode], 
        text_type: TextType
    ) -> list[TextNode]:
    """
    Split text member of each node in list into nodes by type.
    """
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            remaining_text = old_node.text
            if text_type == TextType.IMAGE:
                extracted_links: list[tuple[str, str]] = extract_md_links(
                        old_node.text, TextType.IMAGE
                        )
            else:
                extracted_links: list[tuple[str, str]] = extract_md_links(
                        old_node.text, TextType.LINK
                        )
            if extracted_links:
                for text, url in extracted_links:
                    if text_type == TextType.IMAGE:
                        delimiter = f"![{text}]({url})"
                    else:
                        delimiter = f"[{text}]({url})"
                    chunks = remaining_text.split(delimiter, maxsplit=1)
                    if chunks[0] != "":
                        new_nodes.append(TextNode(chunks[0], TextType.TEXT))
                    new_nodes.append(TextNode(text, text_type, url))
                    remaining_text = chunks[1]
                if remaining_text != "":
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            else:
                new_nodes.append(old_node)
    
    return new_nodes


def extract_md_links(
        text: str, text_type: TextType
        ) -> list[tuple[str, str]]:
    """
    Helper function for split_nodes_links().
    """
    image_regex_pattern = r"\!\[([^\[\]\n\r\t]*)\]\(([^\(\)\n\r\t]*)\)"
    link_regex_pattern = r"(?<!!)\[([^\[\]\n\r\t]*)\]\(([^\(\)\n\r\t]*)\)"
    
    match text_type:
        case TextType.IMAGE:
            return re.findall(image_regex_pattern, text)
        case TextType.LINK:
            return re.findall(link_regex_pattern, text)
        case _:
            raise TypeError(
                "TextType positional argument missing in extract_md_links() call"
            )
