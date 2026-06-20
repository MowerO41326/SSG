from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    """
    Enumeration of block types.
    """
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDLIST = "unordered list"
    ORDLIST = "ordered list"
    PARAGRAPH = "paragraph"


def markdown_to_html_node(markdown: str) -> ParentNode:
    """
    #Convert markdown document to HTML node.
    """
    parents = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            count = block.count("#", 0, 7) # Determine heading level from first 7 characters
            heading = block[count + 1:]
            
            heading_node = ParentNode(f"h{count}", text_to_children(heading))
            parents.append(heading_node)

        elif block_type == BlockType.CODE:
            text = block[4:-3]
            text_node = TextNode(text, TextType.TEXT)
            leaf_node = text_node_to_html_node(text_node)
            code_node = ParentNode("code", [leaf_node])
            pre_node = ParentNode("pre", [code_node])
            parents.append(pre_node)

        elif block_type == BlockType.QUOTE:
            sliced_lines = []
            lines = block.split("\n")
            
            for line in lines:
                sliced_lines.append(line[1:].strip())
            
            quote = " ".join(sliced_lines)
            quote_node = ParentNode("blockquote", text_to_children(quote))
            parents.append(quote_node)

        elif block_type == BlockType.UNORDLIST:
            lines = block.split("\n")
            children = []
            
            for line in lines:
                line = line[1:].strip()
                line_node = ParentNode("li", text_to_children(line))
                children.append(line_node)

            unordlist_node = ParentNode("ul", children)
            parents.append(unordlist_node)

        elif block_type == BlockType.ORDLIST:
            lines = block.split("\n")
            children = []
            
            for line in lines:
                line = line[3:]
                line_node = ParentNode("li", text_to_children(line))
                children.append(line_node)
            
            ordlist_node = ParentNode("ol", children)
            parents.append(ordlist_node)

        else:
            lines = " ".join(block.split("\n"))
            paragraph_node = ParentNode("p", text_to_children(lines))
            parents.append(paragraph_node)            

    node = ParentNode("div", parents)
    
    return node


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Convert markdown document to list of blocks.
    """
    blocks = []
    chunks = markdown.split("\n\n")
    for chunk in chunks:
        chunk = chunk.strip()
        if chunk != "":
            blocks.append(chunk)
    
    return blocks


def block_to_block_type(block: str) -> BlockType:
    """
    Scan the block and return the block type.
    """
    lines = block.split("\n")

    if block.startswith(
            ("# ", "## ", "### ", "#### ", "##### ", "###### ")
        ):
        return BlockType.HEADING
    
    if len(lines) > 1:
        if lines[0].startswith("```") and lines[-1].endswith("```"):
            return BlockType.CODE

    is_quote = True
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE

    is_unordlist = True
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                is_unordlist = False
                break
        if is_unordlist:
            return BlockType.UNORDLIST

    is_ordlist = True
    if block.startswith("1. "):
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i+1}. "):
                is_ordlist = False
                break
        if is_ordlist:
            return BlockType.ORDLIST

    return BlockType.PARAGRAPH


def text_to_children(text: str) -> list[HTMLNode]:
    """
    Convert text to list of LeafNodes
    """
    children = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        children.append(text_node_to_html_node(node))

    return children


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Error: no title found")
