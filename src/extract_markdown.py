import re
from textnode import TextNode, TextType
from splitnode import *

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

def split_nodes_image(old_nodes):
    new_nodes = []
    images_in_node = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images_in_node = extract_markdown_images(original_text)
        if len(images_in_node) == 0:        
            new_nodes.append(old_node)
            continue
        split_nodes = []
        
        for i in range(len(images_in_node)):
            sections = original_text.split(f"![{images_in_node[i][0]}]({images_in_node[i][1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            split_nodes.append(TextNode(images_in_node[i][0], TextType.IMAGES, images_in_node[i][1]))
            if len(sections) > 1:
                original_text = sections[1]
        
        new_nodes.extend(split_nodes)    
    
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
                    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    links_in_node = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links_in_node = extract_markdown_links(original_text)
        if len(links_in_node) == 0:        
            new_nodes.append(old_node)
            continue
        split_nodes = []
        
        for i in range(len(links_in_node)):
            sections = original_text.split(f"[{links_in_node[i][0]}]({links_in_node[i][1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            split_nodes.append(TextNode(links_in_node[i][0], TextType.LINKS, links_in_node[i][1]))
            
            if len(sections) > 1:
                original_text = sections[1]
           
        new_nodes.extend(split_nodes)
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = [node]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def extract_title(markdown):
    if not markdown:
        raise ValueError("Input markdown is empty or None")

    for line in markdown.splitlines():
        if re.match(r"^#{1} ", line):
            return line[2:].strip()
    
    raise ValueError("No title found in markdown")

