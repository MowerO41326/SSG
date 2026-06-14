import unittest

from markdown_blocks import (
        block_to_block_type, 
        BlockType, 
        markdown_to_blocks, 
        )


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = (
            "# This is a heading\n\n"
            "This is a paragraph of text. It has some **bold** and "
            "_italic_ words inside of it.\n\n"
            "- This is the first list item in a list block\n"
            "- This is a list item\n- This is another list item"
            )

        test1 = markdown_to_blocks(text)

        self.assertListEqual(
            [
                "# This is a heading", 
                (
                    "This is a paragraph of text. It has some **bold** "
                    "and _italic_ words inside of it."
                ), 
                (
                    "- This is the first list item in a list block\n"
                    "- This is a list item\n- This is another list item"
                ), 
            ], 
            test1,
        )


    def test_block_to_block_type(self):
        textblocks = [
                "# ", "## ", "### ", "#### ", "##### ", "###### ", 
                "```\nCode Block\nif x == 1:\n    return y\n```", 
                "> Hello, world!\n", 
                "- First item\n- Second item\n- Third item\n", 
                "1. Step 1\n2. Step 2\3. Step 3\n", 
                "#Paragraph", 
                "####### Paragraph", 
                "```\nParagraph", 
                "```Paragraph```", 
                " - Paragraph\n - abc\n - 123\n", 
                "1.Paragraph", 
            ]
        results = []

        for textblock in textblocks:
            results.append(block_to_block_type(textblock))

        self.assertListEqual(
            [
                BlockType.HEADING, BlockType.HEADING, BlockType.HEADING, 
                BlockType.HEADING, BlockType.HEADING, BlockType.HEADING, 
                BlockType.CODE, BlockType.QUOTE, BlockType.UNORDLIST, 
                BlockType.ORDLIST, BlockType.PARAGRAPH, 
                BlockType.PARAGRAPH, BlockType.PARAGRAPH, 
                BlockType.PARAGRAPH, BlockType.PARAGRAPH, 
                BlockType.PARAGRAPH, 
            ], 
            results, 
        )
