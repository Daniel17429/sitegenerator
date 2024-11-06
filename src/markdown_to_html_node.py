from textnode import *
from htmlnode import *
from block_markdown import *
from extract_markdown import *

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = [] 
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

def convert_paragraph_block(text):
    lines = text.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children=children)

# Helper function to convert heading blocks into HTMLNodes
def convert_heading_block(text):
    level = text.count("#")
    heading_text = text[level + 1:].strip()  # Remove # and trailing spaces
    return ParentNode(f"h{level}", children=text_to_children(heading_text))

# Helper function to convert code blocks into HTMLNodes
def convert_code_block(text):
    code_content = text.strip("`").strip()
    code_node = LeafNode("code", value = code_content)
    return ParentNode("pre", children=[code_node])

# Helper function to convert quote blocks into HTMLNodes
def convert_quote_block(text):
    lines = [line.lstrip("> ").strip() for line in text.splitlines()]
    quote_content = " ".join(lines)
    return ParentNode("blockquote", children=text_to_children(quote_content))

# Helper function to convert unordered list blocks into HTMLNodes
def convert_unordered_list_block(text):
    items = text.splitlines()
    list_nodes = []
    for item in items:
        item_text = item[2:]
        list_nodes.append(ParentNode("li", children=text_to_children(item_text)))
    return ParentNode("ul", children=list_nodes)

# Helper function to convert ordered list blocks into HTMLNodes
def convert_ordered_list_block(text):
    items = text.splitlines()
    list_nodes = []
    for item in items:
        item_text = item.split(". ", 1)[1].strip()
        list_nodes.append(ParentNode("li", children=text_to_children(item_text)))
    return ParentNode("ol", children=list_nodes)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children_root = []

    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == "paragraph":
            children_root.append(convert_paragraph_block(block))
        elif block_type == "heading":
            children_root.append(convert_heading_block(block))
        elif block_type == "code":
            children_root.append(convert_code_block(block))
        elif block_type == "quote":
            children_root.append(convert_quote_block(block))
        elif block_type == "unordered_list":
            children_root.append(convert_unordered_list_block(block))
        elif block_type == "ordered_list":
            children_root.append(convert_ordered_list_block(block))

    root = ParentNode("div", children=children_root, props=None)
    
    return root