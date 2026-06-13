import unittest

from textnode import TextNode, TextType
from inline_markdown import (
        split_nodes_delimiter, 
        extract_markdown_images, 
        extract_markdown_links, 
        split_nodes_image, 
        split_nodes_link, 
        )


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


    def test_extract_md_images(self):
        matches = extract_markdown_images(
            "This is text with an "
            "![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        matches2 = extract_markdown_images(
            "This is text with an "
            "![image!](https://i.imgur.com/zjjcJKZ.png)"
        )
        matches3 = extract_markdown_images(
            "This is text with an "
            "![[image]](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
                [("image", "https://i.imgur.com/zjjcJKZ.png")], matches
                )
        self.assertListEqual(
                [("image!", "https://i.imgur.com/zjjcJKZ.png")], matches2
                )
        self.assertListEqual([], matches3)


    def test_extract_md_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )
        matches2 = extract_markdown_links(
            "This is text with a [link!](https://www.boot.dev)"
        )
        matches3 = extract_markdown_links(
            "This is text with a [[link]](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)
        self.assertListEqual([("link!", "https://www.boot.dev")], matches2)
        self.assertListEqual([], matches3)


    def test_extract_md_wrong_syntax(self):
        img_matches = extract_markdown_images(
            "This is wrong syntax for images [image](www.nasa.gov/img.jpg)"
        )
        img_matches2 = extract_markdown_images(
            "This is wrong sytanx for images ![image]](www.nasa.gov/1.jpg)"
        )
        link_matches = extract_markdown_links(
            "This is wrong syntax for links (link)(www.nasa.gov)"
        )
        link_matches2 = extract_markdown_links(
            "This is wrong syntax for links ![image](www.nasa.com/jpg.png)"
        )
        self.assertFalse(img_matches)
        self.assertFalse(img_matches2)
        self.assertFalse(link_matches)
        self.assertFalse(link_matches2)


    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![second image](https://i.imgur.com/3elNhQu.png)", 
            TextType.TEXT
        )
        node2 = TextNode(
            "This is text with a [link](https://www.xxx.yyy/zzz)", 
            TextType.TEXT
        )
        node3 = [
                TextNode("This is text with an ![image](blah.bmp)", TextType.TEXT),
                TextNode("This is text with another ![image](blah2.bmp)", TextType.TEXT), 
                TextNode("link", TextType.LINK, "https://whocares.org"), 
                TextNode("More [pics](somepichost.com) of my trip to the bottling plant", TextType.TEXT), 
                TextNode("Oops forgot to show you ![this](onemore.net) one!", TextType.TEXT), 
                ]
        new_nodes = split_nodes_image([node])
        new_nodes2 = split_nodes_image([node2])
        new_nodes3 = split_nodes_image(node3)
        self.assertListEqual(
                [
                    TextNode("This is text with an ", TextType.TEXT), 
                    TextNode(
                        "image", 
                        TextType.IMAGE, 
                        "https://i.imgur.com/zjjcJKZ.png"
                    ), 
                    TextNode(" and another ", TextType.TEXT), 
                    TextNode(
                        "second image", 
                        TextType.IMAGE, 
                        "https://i.imgur.com/3elNhQu.png"
                    )
                ], 
                new_nodes, 
            )
        self.assertListEqual(
                [TextNode("This is text with a [link](https://www.xxx.yyy/zzz)", TextType.TEXT)], new_nodes2)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT), 
                TextNode("image", TextType.IMAGE, "blah.bmp"), 
                TextNode("This is text with another ", TextType.TEXT), 
                TextNode("image", TextType.IMAGE, "blah2.bmp"), 
                TextNode("link", TextType.LINK, "https://whocares.org"), 
                TextNode("More [pics](somepichost.com) of my trip to the bottling plant", TextType.TEXT), 
                TextNode("Oops forgot to show you ", TextType.TEXT), 
                TextNode("this", TextType.IMAGE, "onemore.net"), 
                TextNode(" one!", TextType.TEXT), 
            ],
            new_nodes3, 
        )


    def test_split_nodes_link(self):
        node = [
                TextNode(
                    "This is a [link](url) and [another link](url2)", 
                    TextType.TEXT
                ), 
                TextNode(
                    "This is an ![image](https://www.xxx.yyy/zzz.gif)", 
                    TextType.TEXT
                ), 
                TextNode("link", TextType.LINK, "to.the.past"), 
                TextNode("One [link](url), one ![image](img), one more [link](url)", TextType.TEXT), 
            ]
        new_nodes = split_nodes_link(node)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT), 
                TextNode("link", TextType.LINK, "url"), 
                TextNode(" and ", TextType.TEXT), 
                TextNode("another link", TextType.LINK, "url2"), 
                TextNode("This is an ![image](https://www.xxx.yyy/zzz.gif)", TextType.TEXT),
                TextNode("link", TextType.LINK, "to.the.past"),
                TextNode("One ", TextType.TEXT), 
                TextNode("link", TextType.LINK, "url"), 
                TextNode(", one ![image](img), one more ", TextType.TEXT), 
                TextNode("link", TextType.LINK, "url")
            ],
            new_nodes, 
        )
