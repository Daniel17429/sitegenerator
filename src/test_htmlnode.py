import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_prop(self):
        node = HTMLNode("p", "This is value", ["object", "object"], {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(
            'href="https://www.google.com" target="_blank"', node.props_to_html()
        )

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            'class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

class TestLeafNode(unittest.TestCase):
    def test_leafnode_with_tag_and_value(self):
        # Test with tag and value, no props
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leafnode_with_tag_value_and_props(self):
        # Test with tag, value, and props
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leafnode_without_tag_returns_raw_text(self):
        # Test without a tag, should return raw text
        node = LeafNode(None, "Raw text content")
        self.assertEqual(node.to_html(), "Raw text content")
       
    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

class TestParentNode(unittest.TestCase):
    def test_parentnode_with_tag_and_children(self):
        # Test with tag and multiple LeafNode children
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parentnode_with_tag_and_props(self):
        # Test with tag, properties, and children
        node = ParentNode(
            "div",
            [
                LeafNode("span", "Some text", {"class": "highlight"})
            ],
            props={"id": "container"}
        )
        self.assertEqual(node.to_html(), '<div id="container"><span class="highlight">Some text</span></div>')

    def test_parentnode_without_tag_raises_error(self):
        # Test with no tag, should raise ValueError
        with self.assertRaises(ValueError) as context:
            ParentNode(
                None,
                [LeafNode("b", "Bold text")]
            )
        self.assertEqual(str(context.exception), "ParentNode must have a tag.")

    def test_parentnode_without_children_raises_error(self):
        # Test with empty children, should raise ValueError
        with self.assertRaises(ValueError) as context:
            ParentNode("div", [])
        self.assertEqual(str(context.exception), "ParentNode must have children.")

    def test_parentnode_with_nested_parentnodes(self):
        # Test with nested ParentNode and LeafNode children
        node = ParentNode(
            "div",
            [
                LeafNode("h1", "Title"),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text in paragraph"),
                        LeafNode(None, "Some more text")
                    ]
                )
            ]
        )
        expected_html = "<div><h1>Title</h1><p><b>Bold text in paragraph</b>Some more text</p></div>"
        self.assertEqual(node.to_html(), expected_html)

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


if __name__ == "__main__":
    unittest.main()

