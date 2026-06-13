import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
        old_nodes: list[TextNode], 
        delimiter: str, 
        text_type: TextType
    ) -> list[TextNode]:
    """
    Splits raw markdown text from each TextNode in a list of TextNodes 
    using the delimiter provided and converting the TextType.

    Args:
        old_nodes (list[TextNode]): A list of TextNodes to be split 

        delimiter (str): Delimiter character(s) used in .split() call

        text_type (TextType): TextType for the TextNode to be converted
                              to if delimiter is present

    Returns:
        list[TextNode]: A list of split TextNodes
            
    """

    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            delimited_strings = old_node.text.split(delimiter)
            if len(delimited_strings) % 2 == 0:
                raise SyntaxError("Invalid Markdown Syntax found")
            for i, text in enumerate(delimited_strings):
                if text == "":
                    continue
                new_node_type = TextType.TEXT if i % 2 == 0 else text_type
                new_nodes.append(TextNode(text, new_node_type))

    return new_nodes


def split_nodes_by_type(
        old_nodes: list[TextNode], 
        text_type: TextType
    ) -> list[TextNodes]:
    """
    Helper function for split_nodes_image() and split_nodes_link

    Args:
        old_node_text (str): A string of raw text to be split
        delimiter (str): Image or link inside old text
        text_type (TextType): Correspinging TextType of the caller

    Returns:
        list[TextNode]: A list of split TextNodes
    """
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            remaining_text = old_node.text
            if text_type == TextType.IMAGE:
                extracted_images: list[tuple[str, str]] = extract_markdown_images(old_node.text)
            else:
                extracted_images: list[tuple[str, str]] = extract_markdown_links(old_node.text)
            if extracted_images:
                for text, url in extracted_images:
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
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes


def split_nodes_image(nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits the text member of each TextNode in a list into new 
    TextNodes, setting qualifying nodes to TextType.IMAGE.

    Args:
        nodes (list[TextNode]): A list of TextNodes to be processed

    Returns:
        list[TextNode]: A list of split TextNodes
    """

    return split_nodes_by_type(nodes, TextType.IMAGE)


def split_nodes_link(nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits the text member of each TextNode in a list into new 
    TextNodes, setting qualifying nodes to TextType.LINK.

    Args:
        nodes (list[TextNode]: A list of TextNodes to be processed

    Returns:
        list[TextNode]: A list of split TextNodes
    """

    return split_nodes_by_type(nodes, TextType.LINK)


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    r"""
    Extracts markdown images from raw markdown text.

    Args:
        text: str - The raw markdown string

    Returns:
        list[tuple[str, str]] - A list of tuples containing:
            (alt_text, url)

            Prohibited characters in alt_text: [, ], \n, \r, \t
            Prohibited characters in url: (, ), \n, \r, \t
    """
    image_regex_pattern = r"\!\[([^\[\]\n\r\t]*)\]\(([^\(\)\n\r\t]*)\)"   
    return re.findall(image_regex_pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    r"""
    Extracts markdown links from raw markdown text.

    Args:
        text: str - The raw markdown string

    Returns:
        list[tuple[str,str]] - A list of tuples containing:
            (title, url)

            Prohibited characters in title: [, ], \n, \r, \t
            Prohibited characters in url: (, ), \n, \r, \t
    """
    link_regex_pattern = r"(?<!!)\[([^\[\]\n\r\t]*)\]\(([^\(\)\n\r\t]*)\)"
    return re.findall(link_regex_pattern, text)
