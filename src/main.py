from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(text_node)
    x = HTMLNode(None, None, None, {"a" : 15, "b" : 20})
    y = HTMLNode(None, None, None, None)
    z = HTMLNode(None, None, None, None)
    k = HTMLNode(None, None, None, None)
    x.children = []
    y.children = []
    z.children = []
    z.children.append(k)
    y.children.append(z)
    x.children.append(y)
    x.children.append(y)
    print(z)
    print(y)
    print(x)
    

  

if __name__ == "__main__":
    main()