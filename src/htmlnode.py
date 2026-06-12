class HTMLNode:
    def __init__(
            self, 
            tag: str | None = None, 
            value: str | None = None, 
            children: list["HTMLNode"] | None = None, 
            props: dict[str, str] | None = None, 
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError("to_html() not implemented")


    def props_to_html(self) -> str:
        html = ""
        if self.props:
            for key, value in self.props.items():
                html += f' {key}="{value}"'
        return html


    def __repr__(self) -> str:
        return (
            f"HTMLNode(tag: {self.tag}; value: {self.value}; "
            f"children: {self.children}; properties: {self.props})"        
        )


class ParentNode(HTMLNode):
    def __init__(
            self, 
            tag: str, 
            children: list["HTMLNode"], 
            props: dict[str, str] | None = None, 
    ) -> None:
        super().__init__(tag, None, children, props)


    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have at least one 'child' Node")
        return (
            f"<{self.tag}{self.props_to_html()}>"
            f"{''.join(child.to_html() for child in self.children)}"
            f"</{self.tag}>"
        )


    def __repr__(self) -> str:
        return (
            f"ParentNode(tag: {self.tag}; children: {self.children}; "
            f"properties: {self.props})"
        )


class LeafNode(HTMLNode):
    def __init__(
            self, 
            tag: str | None, 
            value: str, 
            props: dict[str, str] | None = None, 
    ) -> None:
        super().__init__(tag, value, None, props)


    def to_html(self) -> str:
        if not self.value:
            raise ValueError("LeafNode object must have a value")
        if not self.tag:
            return f"{self.value}"
        return (
            f"<{self.tag}{self.props_to_html()}>"
            f"{self.value}"
            f"</{self.tag}>"
        )


    def __repr__(self) -> str:
        return (
            f"LeafNode(tag: {self.tag}; value: {self.value}; "
            f"properties: {self.props})"
        )
