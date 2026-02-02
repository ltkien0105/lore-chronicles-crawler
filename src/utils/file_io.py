def write_content(filename, content) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
