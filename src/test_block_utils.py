import unittest
from textwrap import dedent

from block_utils import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_olist,
    block_type_ulist,
    block_type_quote,
)
from textnode import TextNode, TextType

class TestMarkdownBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = (
            "# This is a heading        \n\n\n"
            "   This is a paragraph of text. It has some **bold** and *italic* words inside of it.   \n\n\n\n"
            "* This is the first list item in a list block\n"
            "* This is a list item\n"
            "* This is another list item\n"
        )
        exp_ans = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            (
                "* This is the first list item in a list block\n"
                "* This is a list item\n"
                "* This is another list item"
            )
        ]
        act_ans = markdown_to_blocks(text)
        self.assertListEqual(act_ans, exp_ans)
    
    def test_block_to_block_types(self):
        # simple tests
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_ulist)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_olist)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

        # edge cases
        block = "* list\n- items"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)
        block = "#heading"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)
