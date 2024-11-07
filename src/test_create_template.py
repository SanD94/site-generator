import unittest
from create_template import extract_title

class TestCreateTemplate(unittest.TestCase):
    def test_extract_title(self):
        text = "empty\n# Hello   \nWorld\nnope"
        act_ans = extract_title(text)
        exp_ans = "Hello"
        self.assertEqual(act_ans, exp_ans)
    
    def test_extract_title_value(self):
        text = "No heading"
        with self.assertRaises(ValueError) as cm:
            extract_title(text)
        self.assertEqual(cm.exception.args[0], "there is not title in the markdown")

    
if __name__ == "__main__":
    unittest.main()