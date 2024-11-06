import unittest
from block_markdown import *

class TestBlockMarkdown(unittest.TestCase):

    def test_markdown_to_blocks(self):
        markdown_blocks = markdown_to_blocks("This is a test\n\nThis is another test")
        self.assertEqual(markdown_blocks, ["This is a test", "This is another test"])

    def test_markdown_to_blocks_with_newlines(self):
        markdown_blocks = markdown_to_blocks("This is a test\n\n\n\nThis is another test")
        self.assertEqual(markdown_blocks, ["This is a test", "This is another test"])    

    def test_markdown_to_blocks_with_no_newlines(self):
        markdown_blocks = markdown_to_blocks("This is a testThis is another test")
        self.assertEqual(markdown_blocks, ["This is a testThis is another test"])

    def test_markdown_to_blocks_with_empty_string(self):
        markdown_blocks = markdown_to_blocks("")
        self.assertEqual(markdown_blocks, [])   
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )
class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), "heading")
        self.assertEqual(block_to_block_type("## Heading 2"), "heading")
        self.assertEqual(block_to_block_type("###### Heading 6"), "heading")
        self.assertNotEqual(block_to_block_type("####### Invalid heading"), "heading")  # Shouldn't be a valid heading
    
    def test_code_block(self):
        code_block = "```\ncode line 1\ncode line 2\n```"
        self.assertEqual(block_to_block_type(code_block), "code")
        
        # Edge cases
        code_block_incomplete = "```\ncode line 1\ncode line 2"
        self.assertNotEqual(block_to_block_type(code_block_incomplete), "code")
    
    def test_quote_block(self):
        quote_block = "> This is a quote\n> Another quote line"
        self.assertEqual(block_to_block_type(quote_block), "quote")
        
        # Edge case: Not every line starts with ">"
        mixed_quote_block = "> This is a quote\nThis line does not start with >"
        self.assertNotEqual(block_to_block_type(mixed_quote_block), "quote")

    def test_unordered_list(self):
        unordered_list = "* Item 1\n* Item 2"
        self.assertEqual(block_to_block_type(unordered_list), "unordered_list")
        
        another_unordered_list = "- Item A\n- Item B"
        self.assertEqual(block_to_block_type(another_unordered_list), "unordered_list")
        
        # Edge case: not all lines are unordered list items
        mixed_unordered_list = "* Item 1\nNot a list item"
        self.assertNotEqual(block_to_block_type(mixed_unordered_list), "unordered_list")

    def test_ordered_list(self):
        ordered_list = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(ordered_list), "ordered_list")
        
        # Edge case: numbering does not increment correctly
        incorrect_ordered_list = "1. First item\n3. Skipped number"
        self.assertNotEqual(block_to_block_type(incorrect_ordered_list), "ordered_list")
        
    def test_paragraph(self):
        paragraph = "This is a normal paragraph without any special formatting."
        self.assertEqual(block_to_block_type(paragraph), "paragraph")
        
        # Edge case: formatted-like text but doesn't meet any specific block criteria
        tricky_paragraph = "Hello *world*, this isn't a list or heading"
        self.assertEqual(block_to_block_type(tricky_paragraph), "paragraph")
    
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), "heading")
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), "code")
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), "quote")
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), "unordered_list")
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), "ordered_list")
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), "paragraph")




if __name__ == "__main__":
    unittest.main()