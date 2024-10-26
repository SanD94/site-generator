import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_str(self):
        node = TextNode("This is a text node", TextType.BOLD)
        str_node = "TextNode(This is a text node, bold, None)"
        self.assertEqual(repr(node), str_node)
    
    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_str(self):
        node = TextNode("This is another text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

class TestToLeafMethod(unittest.TestCase):
    def test_raw_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf, LeafNode(None, "This is a text node"))
        
    def test_bold_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf, LeafNode("b", "This is a text node"))

    def test_italic_text(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf, LeafNode("i", "This is a text node"))

    def test_code_text(self):
        node = TextNode("This is a text node", TextType.CODE)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf, LeafNode("code", "This is a text node"))

    def test_link_text(self):
        node = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf, LeafNode("a", "This is a text node", {"href" : "https://boot.dev"}))

    def test_image_text(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://boot.dev")
        leaf = text_node_to_html_node(node)
        self.assertEqual(
            leaf,
            LeafNode("img", "", {"src" : "https://boot.dev", "alt" : "This is a text node"})
        )

    def test_err_text(self):
        node = TextNode("This is a text node", TextType.NONE)
        with self.assertRaises(ValueError) as cm:
            text_node_to_html_node(node)
        self.assertEqual(cm.exception.args[0], f"Invalid TextType: {node.text_type}") 
        



if __name__ == "__main__":
    unittest.main()