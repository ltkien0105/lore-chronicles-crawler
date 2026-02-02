from bs4 import Tag


def get_n_next_siblings(element: Tag, n: int) -> list[str]:
    siblings = []
    sibling = element.next_siblings
    appearance = 0

    while sibling:
        sib = next(sibling, None)
        if sib is None:
            break

        if isinstance(sib, Tag):
            text = sib.text.strip()
            if text:
                siblings.append(sib)
                appearance += 1

        if appearance >= n:
            break

    return siblings


def get_all_links(soup: Tag) -> list[str]:
    return [a["href"] for a in soup.find_all("a", href=True)]
