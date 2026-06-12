import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "h",
            "The heading goes here.",
            None, 
            {"href": "https://www.boot.dev", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.boot.dev" target="_blank"', 
        )


    def test_values(self):
        node = HTMLNode(
            "a", 
            "Some Link", 
            props = {
                "class": "reference external", 
                "href": "https://www.nasa.gov", 
            }
        )
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Some Link")
        self.assertIsNone(node.children)
        self.assertIsNotNone(node.props)
        self.assertRaises(NotImplementedError, node.to_html)


    def test_repr(self):
        node = HTMLNode(
            "p", 
            "Text goes here.", 
            None, 
            {"margin": "20px 0"}
        )
        self.assertEqual(
            repr(node), (
                f"HTMLNode(tag: p; value: Text goes here.; "
                f"children: None; properties: {{'margin': '20px 0'}})"
            )
        )


    def test_leaf_to_html(self):
        node = LeafNode(
            "p", 
            "Hello, world!", 
            {"font-family": "JHA Bondoni Ritalic"}
        )
        self.assertEqual(
            node.to_html(), 
            '<p font-family="JHA Bondoni Ritalic">Hello, world!</p>'
        )
        self.assertEqual(
            repr(node), (
                f"LeafNode(tag: p; value: Hello, world!; "
                f"properties: {{'font-family': 'JHA Bondoni Ritalic'}})"
            )
        )
        self.assertIsNone(node.children)
        self.assertIsInstance(node, LeafNode)
        self.assertEqual(
            node.props_to_html(), 
            ' font-family="JHA Bondoni Ritalic"'
        )
    

    def test_leaf_raise(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), 
            "<div><span><b>grandchild</b></span></div>",
        )


    def test_parent_raise(self):
        child_node = ParentNode("a", [])
        parent_node = ParentNode("", [child_node])
        self.assertRaises(ValueError, child_node.to_html)
        self.assertRaises(ValueError, parent_node.to_html)


    def test_parent_repr(self):
        child_node1 = LeafNode("p", "child1")
        child_node2 = LeafNode("p", "child2")
        parent_node = ParentNode("c", [child_node1, child_node2])
        self.assertEqual(
            repr(parent_node), 
            "ParentNode(tag: c; children: ["
            "LeafNode(tag: p; value: child1; properties: None), "
            "LeafNode(tag: p; value: child2; properties: None)"
            "]; properties: None)"
        
        )


    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )


    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

