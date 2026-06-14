from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDLIST = "unordered list"
    ORDLIST = "ordered list"

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
