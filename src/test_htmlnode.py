import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_tag(self):
        node = HTMLNode(None, "value", None, None)
        self.assertEqual(node.tag, None)
        self.assertNotEqual(node.value, None)
        
    def test_value(self):
        child = HTMLNode(None, "value", None, None)
        node = HTMLNode("a", None, [child], None)
        self.assertEqual(node.value, None)
        self.assertNotEqual(node.children, None)
    
    def test_children(self):
        node = HTMLNode(None, "value", None, None)
        self.assertEqual(node.children, None)
        self.assertNotEqual(node.value, None)
    
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode("div", "I wish I could read",)
        self.assertEqual(node.tag, "div",)
        self.assertEqual(node.value, "I wish I could read")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

class TestLeafNode(unittest.TestCase):
    def test_value(self):
        node = LeafNode("a", "value", {"href": "https://www.google.com"})
        self.assertEqual(node.children, None)
        self.assertNotEqual(node.value, None)
        
    def test_print(self):
        node = LeafNode("a", None, {"href": "https://www.google.com"})
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(cm.exception.args[0], "Invalid HTML: no value")

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
    

if __name__ == "__main__":
    unittest.main()