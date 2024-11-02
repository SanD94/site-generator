import re
from functools import reduce

def markdown_to_blocks(markdown : str) -> list[str]:
    blocks = list(filter(
        lambda str: str != "",
        map(
            lambda str: str.strip(),
            markdown.split("\n\n")
        )
    ))
    return blocks

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

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

def block_to_block_type(block_markdown : str) -> str:
    n_line = len(block_markdown.split("\n"))

    if _is_heading(block_markdown):
        return block_type_heading
    if _is_code(block_markdown):
        return block_type_code
    if _is_quote(block_markdown, n_line):
        return block_type_quote
    if _is_ulist(block_markdown, n_line):
        return block_type_ulist
    if _is_olist(block_markdown, n_line):
        return block_type_olist
    
    return block_type_paragraph