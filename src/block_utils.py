import re
from functools import reduce
from htmlnode import ParentNode, HTMLNode
from enum import Enum
from inline_utils import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_blocks(markdown : str) -> list[str]:
    blocks = list(filter(
        lambda str: str != "",
        map(
            lambda str: str.strip(),
            markdown.split("\n\n")
        )
    ))
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"
    NONE = "none"

def _is_heading(block_markdown : str) -> bool:
    return re.match(r"^#{1,6} ", block_markdown)

def _is_code(block_markdown : str) -> bool:
    code_backtick = "```"

    return (
        block_markdown[0:3] == code_backtick and 
        block_markdown[-3:] == code_backtick
    )

def _is_quote(block_markdown : str, n_line : int) -> bool:
    return len(re.findall(r"^>", block_markdown, re.MULTILINE)) == n_line

def _is_ulist(block_markdown : str, n_line : int) -> bool:
    unordered_list = re.findall(r"^([-\*]) ", block_markdown, re.MULTILINE)
    if len(unordered_list) == 0:
        return False
    
    first_elem = unordered_list[0]
    all_same = reduce(
        lambda acc, val: acc and val == first_elem,
        unordered_list,
        True
    )
    return all_same and len(unordered_list) == n_line

def _is_olist(block_markdown : str, n_line : int) -> bool:
    ordered_list_str = re.findall(r"^(\d+)\. ", block_markdown, re.MULTILINE)
    if len(ordered_list_str) == 0:
        return False
    
    ordered_list = list(map(int, ordered_list_str))
    return ordered_list == list(range(1, n_line + 1))

def block_to_block_type(block_markdown : str) -> BlockType:
    n_line = len(block_markdown.split("\n"))

    if _is_heading(block_markdown):
        return BlockType.HEADING
    if _is_code(block_markdown):
        return BlockType.CODE
    if _is_quote(block_markdown, n_line):
        return BlockType.QUOTE
    if _is_ulist(block_markdown, n_line):
        return BlockType.ULIST
    if _is_olist(block_markdown, n_line):
        return BlockType.OLIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown : str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    
    children = []
    for block in blocks:
        html_node = _create_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, )


def _create_paragraph_html_node(block : str) -> ParentNode:
    paragraph = " ".join(block.split("\n"))
    text_nodes = text_to_textnodes(paragraph)
    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return ParentNode("p", html_nodes)

def _create_heading_html_node(block : str) -> ParentNode:
    ### assuming there is only one heading
    header, block = re.findall(r"^(#{1,6}) (.*)", block)[0]
    header_len = len(header)
    text_nodes = text_to_textnodes(block)
    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return ParentNode(f"h{header_len}", html_nodes)


def _create_code_html_node(block : str) -> ParentNode:
    block = block[3:-3]
    text_nodes = text_to_textnodes(block)
    html_nodes = list(map(text_node_to_html_node, text_nodes))
    code = ParentNode("code", html_nodes)
    return ParentNode("pre", [code])

def _create_quote_html_node(block : str) -> ParentNode:
    lines = block.split("\n")
    quote = " ".join(list(map(lambda line: re.findall(r"^(>) (.*)", line)[0][1], lines)))
    text_nodes = text_to_textnodes(quote)
    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return ParentNode("blockquote", html_nodes)

def _create_ulist_html_node(block : str) -> ParentNode:
    lines = block.split("\n")
    elems = map(lambda line: re.findall(r"^([-\*]) (.*)", line)[0][1], lines)
    elem_textnode_list = map(text_to_textnodes, elems)
    
    ul_children = []
    for li_textnode_list in elem_textnode_list:
        li_html_node_list = list(map(text_node_to_html_node, li_textnode_list))
        ul_children.append(ParentNode("li", li_html_node_list))
    return ParentNode("ul", ul_children)


def _create_olist_html_node(block : str) -> ParentNode:
    lines = block.split("\n")
            
    elems = map(lambda line: re.findall(r"^(\d+)\. (.*)", line)[0][1], lines)
    elem_textnode_list = map(text_to_textnodes, elems)
    
    ul_children = []
    for li_textnode_list in elem_textnode_list:
        li_html_node_list = list(map(text_node_to_html_node, li_textnode_list))
        ul_children.append(ParentNode("li", li_html_node_list))
    
    return ParentNode("ol", ul_children)

def _create_html_node(block : str) -> ParentNode:
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return _create_paragraph_html_node(block)
            
        case BlockType.HEADING:
            return _create_heading_html_node(block)
            
        case BlockType.CODE:
            return _create_code_html_node(block)
            
        case BlockType.QUOTE:
            return _create_quote_html_node(block)
            
        case BlockType.ULIST:
            return _create_ulist_html_node(block)
            
        case BlockType.OLIST:
            return _create_olist_html_node(block)
            
        case _:
            raise ValueError("Invalid Block Type")

