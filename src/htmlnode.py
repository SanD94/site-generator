class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props == None:
            return ""
        return " "+" ".join(map(lambda val : f'{val[0]}="{val[1]}"', self.props.items()))

    def _print_children(self, depth, tab):
        if self.children == None:
            return "None"
        if depth == 6:
            return "REDACTED..."
        n_tab = (depth - 1) * tab
        return "[\n" \
            + ",\n".join(map(lambda child: child._repr(depth), self.children)) \
            + "\n" + n_tab + "]"

    def __repr__(self):
        return self._repr(0)
    
    def _repr(self, depth):
        one_tab = 4 * " " # assumption with 4 spaces to print pretty
        n_tab = depth * one_tab
        return n_tab + f"{self.__class__.__name__}(\n" \
            + n_tab + one_tab + f"tag: {self.tag}\n" \
            + n_tab + one_tab + f"value: {self.value}\n" \
            + n_tab + one_tab + f"children: {self._print_children(depth + 2, one_tab)}\n" \
            + n_tab + one_tab + f"props: {self.props_to_html()}\n" \
            + n_tab + ")"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None:
            raise ValueError("Invalid HTML: no children")
        children_html =  "".join(map(lambda child: child.to_html(), self.children))
        return f"<{self.tag}>{children_html}</{self.tag}>"