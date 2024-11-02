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


def split_nodes_image(old_nodes : list[TextNode]) -> list[TextNode]:
    splitted_nodes : list[TextNode] = []
    for node in old_nodes:
        text = node.text
        markdown_images = extract_markdown_images(text)
        if markdown_images == []:
            splitted_nodes.append(node)
            continue

        for markdown_image in markdown_images:
            image_alt, image_link = markdown_image
            delimiter = f"![{image_alt}]({image_link})"
            cur, text = text.split(delimiter, maxsplit=1)
            if cur != "":
                splitted_nodes.append(TextNode(cur, TextType.TEXT))
            splitted_nodes.append(TextNode(image_alt,TextType.IMAGE, image_link))
        
        if text != "":
            splitted_nodes.append(TextNode(text, TextType.TEXT))
    
    return splitted_nodes




def split_nodes_link(old_nodes : list[TextNode]) -> list[TextNode]:
    splitted_nodes : list[TextNode] = []
    for node in old_nodes:
        text = node.text
        markdown_links = extract_markdown_links(text)
        if markdown_links == []:
            splitted_nodes.append(node)
            continue

        for markdown_link in markdown_links:
            link_text, link_url = markdown_link
            delimiter = f"[{link_text}]({link_url})"
            cur, text = text.split(delimiter, maxsplit=1)
            if cur != "":
                splitted_nodes.append(TextNode(cur, TextType.TEXT))
            splitted_nodes.append(TextNode(link_text,TextType.LINK, link_url))
        
        if text != "":
            splitted_nodes.append(TextNode(text, TextType.TEXT))
    
    return splitted_nodes


def text_to_textnodes(text : str) -> list[TextNode]:
    split_functions = {
        "delimiter" : {
            "method" : split_nodes_delimiter,
            "args_list" : [
                ("**", TextType.BOLD),
                ("*", TextType.ITALIC),
                ("`", TextType.CODE),
            ]
        },
        "image" : {
            "method" : split_nodes_image,
            "args_list" : [()]
        },
        "link" : {
            "method" : split_nodes_link,
            "args_list" : [()]
        }
    }
    
    node = TextNode(text, TextType.TEXT)
    text_nodes = [node]
    for split in split_functions.values():
        f = split["method"]
        args_list = split["args_list"]
        for args in args_list:
            text_nodes = f(text_nodes, *args)
    return text_nodes