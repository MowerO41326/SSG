from textnode import TextNode, TextType


def main() -> None:
    print(TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev"))


main()
