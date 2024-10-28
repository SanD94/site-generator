from textnode import TextType, TextNode
from functools import reduce
from collections.abc import Callable
import re



# assuming delimiter and text type share the same meaning and there is no syntax error
def split_nodes_delimiter(old_nodes : list[TextNode], delimiter : str, text_type: TextType) -> list[TextNode]:
    return reduce(
        lambda acc, val: acc + val,
        map(lambda node : _split_node_delimiter(node, delimiter, text_type), old_nodes), 
        []
    )

def _split_node_delimiter(node : TextNode, delimiter : str, text_type: TextType) -> list[TextNode]:
    node_text_type = TextType(node.text_type)
    if node_text_type != TextType.TEXT:
        return [node]
    text_split = node.text.split(delimiter)
    if len(text_split) % 2 == 0:
        raise ValueError(f"Markdown format error: missing {delimiter}")
    return list(filter(
        lambda text_node: text_node.text != "", 
        map(_create_text_node(text_type), enumerate(text_split))
        ))


def _create_text_node(text_type) -> Callable[[tuple[int, str]], TextNode]:
    def wrapper(enum_text : tuple[int, str]) -> TextNode:
        i, text = enum_text
        if i % 2 == 1:
            return TextNode(text, text_type)
        return TextNode(text, TextType.TEXT)
    return wrapper


def extract_markdown_images(text : str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text : str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)