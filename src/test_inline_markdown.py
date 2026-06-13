import unittest

from textnode import TextNode, TextType
from inline_markdown import (
        extract_md_links,  
        split_nodes_delimiter, 
        split_nodes_links, 
        text_to_textnodes, 
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
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)


    def test_extract_md_links(self):
        matches = extract_md_links(
            "This is text with an "
            "![image](https://i.imgur.com/zjjcJKZ.png)", 
            TextType.IMAGE
        )
        matches2 = extract_md_links(
            "This is text with an "
            "![image!](https://i.imgur.com/zjjcJKZ.png)", 
            TextType.IMAGE
        )
        matches3 = extract_md_links(
            "This is text with an "
            "![[image]](https://i.imgur.com/zjjcJKZ.png)", 
            TextType.IMAGE
        )
        self.assertListEqual(
                [("image", "https://i.imgur.com/zjjcJKZ.png")], matches
                )
        self.assertListEqual(
                [("image!", "https://i.imgur.com/zjjcJKZ.png")], matches2
                )
        self.assertListEqual([], matches3)


    def test_extract_md_links(self):
        matches = extract_md_links(
            "This is text with a [link](https://www.boot.dev)", TextType.LINK
        )
        matches2 = extract_md_links(
            "This is text with a [link!](https://www.boot.dev)", TextType.LINK
        )
        matches3 = extract_md_links(
            "This is text with a [[link]](https://www.boot.dev)", TextType.LINK
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)
        self.assertListEqual([("link!", "https://www.boot.dev")], matches2)
        self.assertListEqual([], matches3)


    def test_extract_md_wrong_syntax(self):
        img_matches = extract_md_links(
            "This is wrong syntax for images [image](www.nasa.gov/img.jpg)", TextType.IMAGE
        )
        img_matches2 = extract_md_links(
            "This is wrong sytanx for images ![image]](www.nasa.gov/1.jpg)", TextType.IMAGE
        )
        link_matches = extract_md_links(
            "This is wrong syntax for links (link)(www.nasa.gov)", TextType.LINK
        )
        link_matches2 = extract_md_links(
            "This is wrong syntax for links ![image](www.nasa.com/jpg.png)", TextType.LINK
        )
        self.assertFalse(img_matches)
        self.assertFalse(img_matches2)
        self.assertFalse(link_matches)
        self.assertFalse(link_matches2)


    def test_split_nodes_links_images(self):
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
        new_nodes = split_nodes_links([node], TextType.IMAGE)
        new_nodes2 = split_nodes_links([node2], TextType.IMAGE)
        new_nodes3 = split_nodes_links(node3, TextType.IMAGE)
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


    def test_split_nodes_links(self):
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
        new_nodes = split_nodes_links(node, TextType.LINK)
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


    def test_text_to_textnodes(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        text2 = "This is some text with just a [link](https://www.boot.dev) in the middle."
        text3 = ""
        nodes = text_to_textnodes(text)
        nodes2 = text_to_textnodes(text2)
        nodes3 = text_to_textnodes(text3)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], 
            nodes, 
        )
        self.assertListEqual(
            [
                TextNode("This is some text with just a ", TextType.TEXT), 
                TextNode("link", TextType.LINK, "https://www.boot.dev"), 
                TextNode(" in the middle.", TextType.TEXT), 
            ], 
            nodes2, 
        )
        self.assertListEqual([], nodes3)
