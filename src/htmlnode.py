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
        return " "+" ".join(list(map(lambda val : f'{val[0]}="{val[1]}"', self.props.items())))

    def _print_children(self, depth):
        if self.children == None:
            return "None"
        if depth == 6:
            return "REDACTED..."
        n_whitespace = (depth - 1) * 4 * " "
        return "[\n" \
            + ",\n".join(list(map(lambda child: child._repr(depth), self.children))) \
            + "\n" + n_whitespace + "]"

    def __repr__(self):
        return self._repr(0)
    
    def _repr(self, depth):
        n_whitespace = depth * 4 * " "
        return n_whitespace + "HTMLNode(\n" \
            + n_whitespace + 4 * " " + f"tag: {self.tag}\n" \
            + n_whitespace + 4 * " " + f"value: {self.value}\n" \
            + n_whitespace + 4 * " " + f"children: {self._print_children(depth + 2)}\n" \
            + n_whitespace + 4 * " " + f"props: {self.props_to_html()}\n" \
            + n_whitespace + ")"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"