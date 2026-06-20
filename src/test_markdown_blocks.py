import unittest

from markdown_blocks import (
        block_to_block_type, 
        BlockType, 
        extract_title, 
        markdown_to_blocks, 
        markdown_to_html_node, 
        )


class TestMarkdownToBlocks(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

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
                "> Hello, world!", 
                "- First item\n- Second item\n- Third item", 
                "1. Step 1\n2. Step 2\3. Step 3", 
                "#Paragraph", 
                "####### Paragraph", 
                "```\nParagraph", 
                "```Paragraph```", 
                " - Paragraph\n - abc\n - 123", 
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


    def test_heading(self):
        md = "#### This is a heading."

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(html, "<div><h4>This is a heading.</h4></div>")


    def test_quote(self):
        md = """> 1st line.
>2nd line.
> 3rd line."""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(html, "<div><blockquote>1st line. 2nd line. 3rd line.</blockquote></div>")


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    def test_unordlist(self):
        md = """- list item 1.
- list item 2.
- list item 3.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, 
            "<div><ul><li>list item 1.</li><li>list item 2.</li><li>list item 3.</li></ul></div>", 
        )


    def test_ordlist(self):
        md = """1. list item 1.
2. list item 2.
3. list item 3.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, 
            "<div><ol><li>list item 1.</li><li>list item 2.</li><li>list item 3.</li></ol></div>", 
        )


    def test_extract_title(self):
        md1 = "# Hello"
        md2 = "#   Hello  "
        md3 = """
Some introductory text

# My Title

More content here
"""
        md4 = "## Hi"

        test1 = extract_title(md1)
        test2 = extract_title(md2)
        test3 = extract_title(md3)

        self.assertEqual(test1, "Hello")
        self.assertEqual(test2, "Hello")
        self.assertEqual(test3, "My Title")
        self.assertRaises(Exception, extract_title, md4)
