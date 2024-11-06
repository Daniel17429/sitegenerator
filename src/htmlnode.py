class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children 
        self.props = props 

    def to_html(self):
        raise NotImplementedError("to_html method not implemented") 
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_to_html = ' '.join([f'{key}="{value}"' for key, value in self.props.items()])
        return props_to_html
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag = tag, value = value, children=None, props = props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value.")
        if self.tag is None:
            return self.value
        props_html = self.props_to_html()
        return f"<{self.tag} {props_html}>{self.value}</{self.tag}>" if props_html else f"<{self.tag}>{self.value}</{self.tag}>"
       
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not children:
            raise ValueError("ParentNode must have children.")
        if not tag:
            raise ValueError("ParentNode must have a tag.")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag.")
        if self.children is None:
            raise ValueError("Invalid HTML: no children")
        props_html = self.props_to_html()
        opening_tag = f"<{self.tag} {props_html}>" if props_html else f"<{self.tag}>"
        children_html = ''.join(child.to_html() for child in self.children)
        return f"{opening_tag}{children_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    