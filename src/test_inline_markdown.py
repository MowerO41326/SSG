import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter


class TestInlineMarkdown(unittest.TestCase):
    def test_single_delimiter(self):
        node = TextNode("This is only a **test**.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0].text, "This is only a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "test")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, ".")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    
    def test_multi_delimiter(self):
        node = TextNode("_This_ is only a _test_.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes[0].text, "This")
        self.assertEqual(new_nodes[0].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[1].text, " is only a ")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "test")
        self.assertEqual(new_nodes[2].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[3].text, ".")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)


    def test_chain_calls(self):
        node = TextNode("**This** is _only_ a **test**.", TextType.TEXT)
        new_nodes = split_nodes_delimiter(
                split_nodes_delimiter(
                    [node], 
                    "**", 
                    TextType.BOLD
                    ), 
                "_", 
                TextType.ITALIC
                )
        self.assertEqual(new_nodes[0].text, "This")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, " is ")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "only")
        self.assertEqual(new_nodes[2].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[3].text, " a ")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[4].text, "test")
        self.assertEqual(new_nodes[4].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[5].text, ".")
        self.assertEqual(new_nodes[5].text_type, TextType.TEXT)


    def test_unbalanced(self):
        node = TextNode("This is **only** a **test.", TextType.TEXT)
        with self.assertRaises(SyntaxError):
            split_nodes_delimiter([node], "**", TextType.BOLD)
