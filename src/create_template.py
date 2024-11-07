import os
import shutil
import re

from block_utils import markdown_to_html_node

def delete_files(src = "public"):
    if os.path.exists(src):
        shutil.rmtree(src)


def copy_files(src = "static", dest = "public"):
    if os.path.exists(src) == False:
        raise ValueError(f"source folder not found {src}")
    
    os.mkdir(dest)
    for path in os.listdir(src):
        cur_path = os.path.join(src, path)
        if os.path.isfile(cur_path):
            shutil.copy(cur_path, dest)
        else:
            next_dest = os.path.join(dest, path)
            copy_files(cur_path, next_dest)
        
def extract_title(markdown : str) -> str:
    title = re.findall(r"^# (.*)$", markdown, re.MULTILINE)

    if title == []:
        raise ValueError("there is not title in the markdown")
    
    return title[0].strip()



def generate_page(from_path : str, template_path : str, dest_path : str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_content = read_file(from_path)
    template_content = read_file(template_path)
    html_content = markdown_to_html_node(markdown_content).to_html()
    title =  extract_title(markdown_content)

    full_html = add_content(template_content, html_content, title)
    write_html(full_html, dest_path)
    

def add_content(template, content, title):
    
    elem = re.findall(
        r"(.*)\{\{ Title \}\}(.*)\{\{ Content \}\}(.*)",
        template,
        re.DOTALL
    )
    
    before_title, between, after_content = elem[0]
    return "\n".join([before_title, title, between, content, after_content]) 

def read_file(from_path : str) -> str:
    if not os.path.exists(from_path):
        raise ValueError(f"No file exists {from_path}")
    with open(from_path) as file:
        return file.read()
    
def write_html(html, path):
    dest_dir = os.path.dirname(path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(path, "w") as file:
        file.write(html)
    