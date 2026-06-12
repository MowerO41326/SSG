import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_ineq(self):
        node = TextNode(
            "This is a text node", 
            TextType.BOLD, 
            "https://www.someurl.org"
        )
        node2 = TextNode(
            "This is an text node", 
            TextType.BOLD, 
            "https://www.someurl.org"
        )
        self.assertNotEqual(node, node2)


    def test_ineq2(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)


    def test_eq2(self):
        node = TextNode(
            "This is a text node", 
            TextType.BOLD, 
            "https://www.someurl.org"
        )
        node2 = TextNode(
            "This is a text node", 
            TextType.BOLD, 
            "https://www.someurl.org"
        )
        self.assertEqual(node, node2)


    def test_url_None(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertIsNone(node.url)


    def test_text_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node.text, node2.text)


    def test_url_NotNone(self):
        node = TextNode(
            "This is a text node", 
            TextType.ITALIC, 
            "https://nasa.gov"
        )
        self.assertIsNotNone(node.url)


    def test_text(self):
        node = TextNode("This is a plain text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a plain text node")


    def test_tag_b(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_tag_i(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")


    def test_tag_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")


    def test_tag_link(self):
        node = TextNode(
            "This is a link text node", 
            TextType.LINK, 
            "http://www.myspace.com"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {
                "href": "http://www.myspace.com"
            }
        )


    def test_tag_image(self):
        node = TextNode(
            "This is an image text node", 
            TextType.IMAGE, 
            "http://www.myspace.com/my_pic.jpg"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(
            html_node.props, {
                "src": "http://www.myspace.com/my_pic.jpg", 
                "alt": "This is an image text node"
            }
        )

    
    def test_wrong_text_type(self):
        node = TextNode("This node has the wrong type", "under")
        self.assertRaises(Exception, text_node_to_html_node, node)


if __name__ == "__main__":
    unittest.main()
