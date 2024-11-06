import re
def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    # Check for heading (1-6 # characters followed by space)
    if re.match(r"^#{1,6} ", block):
        return "heading"
    
    # Check for code block (3 backticks at the start and end)
    if block.startswith("```") and block.endswith("```"):
        return "code"
    
    # Check for quote block (every line starts with ">")
    if all(line.startswith(">") for line in block.splitlines()):
        return "quote"
    
    # Check for unordered list block (every line starts with * or - followed by a space)
    if all(re.match(r"^(\*|\-) ", line) for line in block.splitlines()):
        return "unordered_list"
    
    # Check for ordered list block (every line starts with an incrementing number followed by ". ")
    lines = block.splitlines()
    if all(re.match(r"^\d+\. ", line) for line in lines):
        expected_number = 1
        for line in lines:
            if not line.startswith(f"{expected_number}. "):
                break
            expected_number += 1
        else:
            return "ordered_list"

    # If none of the above conditions match, it’s a paragraph
    return "paragraph"