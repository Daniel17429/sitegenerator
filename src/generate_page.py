import os
import shutil

from extract_markdown import *
from htmlnode import *
from markdown_to_html_node import *

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:    
        template = file.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    new_html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    directory_path = os.path.dirname(dest_path)
    if directory_path and not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
    with open(os.path.join(directory_path, "index.html"), "w") as file:
        file.write(new_html_page) 
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
           
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path):
            generate_page(item_path, template_path, os.path.join(dest_dir_path, item))
        elif os.path.isdir(item_path):
            generate_pages_recursive(item_path, template_path, os.path.join(dest_dir_path, item))
        

    
