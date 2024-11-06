import unittest

from markdown_to_html_node import *
from htmlnode import *
from textnode import *
from extract_markdown import *

class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_paragraph(self):
        md = "This is a simple paragraph."
        html = markdown_to_html_node(md)
        self.assertEqual(html.children[0].tag, "p")
        self.assertEqual(html.children[0].children[0].value, "This is a simple paragraph.")

    def test_heading(self):
        md = "# Heading 1"
        html = markdown_to_html_node(md)
        self.assertEqual(html.children[0].tag, "h1")
        self.assertEqual(html.children[0].children[0].value, "Heading 1")

    def test_code_block(self):
        md = "```\ncode line\n```"
        html = markdown_to_html_node(md)
        self.assertEqual(html.children[0].tag, "pre")
        self.assertEqual(html.children[0].children[0].tag, "code")
        self.assertEqual(html.children[0].children[0].value, "code line")

    def test_quote_block(self):
        md = "> This is a quote."
        html = markdown_to_html_node(md)
        self.assertEqual(html.children[0].tag, "blockquote")
        self.assertEqual(html.children[0].children[0].value, "This is a quote.")

    def test_unordered_list(self):
        md = "* Item 1\n* Item 2"
        html = markdown_to_html_node(md)
        self.assertEqual(html.children[0].tag, "ul")
        self.assertEqual(html.children[0].children[0].tag, "li")
        self.assertEqual(html.children[0].children[0].children[0].value, "Item 1")

    def test_ordered_list(self):
        md = "1. First item\n2. Second item"
        html = markdown_to_html_node(md)
        self.assertEqual(html.children[0].tag, "ol")
        self.assertEqual(html.children[0].children[0].tag, "li")
        self.assertEqual(html.children[0].children[0].children[0].value, "First item")

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

if __name__ == '__main__':
    unittest.main()