from textnode import *
from htmlnode import *
from copy_public import *
from generate_page import *

def main():
    copy_directory("./static", "./public")
    generate_pages_recursive("./content", "./template.html", "./public") 

main()