import enum


class BlockType(Enum):
    PARA = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORD = "unordered list"
    ORD = "ordered list"

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


def block_to_block_type(text: str) -> BlockType:
    # check for headings
    # (must have 1-6 "#" + " " followed by text)
    # return BlockType.HEAD
    
    # case: multiline code blocks
    # (must start with "```\n" and end with "```")
    # return BlockType.CODE

    # case: quote block
    # (must begin with ">")
    # return BlockType.QUOTE

    # case: unordered list
    # (must begin with "-")
    # return BlockType.UNORD

    # case: ordered list 
    # (must begin with "1. " and each subsequent line must increment by 1)
    # return BlockType.ORD

    # case _:
    # return BlockType.PARA
