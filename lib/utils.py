from bs4 import Tag


def write_content(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def get_text_of_n_next_siblings(element: Tag, n: int):
    sibling_list = []
    sibling = element.next_siblings
    appearance = 0
    while sibling:
        sib = next(sibling, None)
        if sib is None:
            break
        if isinstance(sib, Tag) and sib.text.strip():
            sibling_list.append(sib.text)
            appearance += 1
        if appearance >= n:
            break
    return sibling_list
