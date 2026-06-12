from textnode import TextNode, TextType


def split_nodes_delimiter(
        old_nodes: list[TextNode], 
        delimiter: str, 
        text_type: TextType
    ) -> list[TextNode]:
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
