from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Optional


@dataclass
class Node:
    name: str


@dataclass
class Directory(Node):
    parent: Optional["Directory"]
    children: dict[str, Node] = field(default_factory=dict)

    def __str__(self):
        return f"{self.name} (dir)"


@dataclass
class File(Node):
    size: int

    def __str__(self):
        return f"{self.name} (file, size={self.size})"


class Session:
    def __init__(self):
        self.root = Directory("/", parent=None)
        self.pwd = self.root

    def replay(self, log: str) -> Directory:
        for block in log.split("$ ")[1:]:
            cmd, *output = block.splitlines()
            match cmd.split(" "):
                case "cd", name:
                    self.change_dir(name)
                case "ls", *_:
                    self.list_dir(output)
                case _:
                    raise ValueError(f"Invalid command: {cmd}")
        return self.root

    def change_dir(self, name: str) -> None:
        if name == "/":
            self.pwd = self.root
        elif name == "..":
            self.pwd = self.pwd.parent or self.root
        else:
            self.pwd = self.get_or_create_dir(name)

    def get_or_create_dir(self, name: str) -> Directory:
        node = self.pwd.children.get(name)
        if not node:
            node = Directory(name, parent=self.pwd)
            self.pwd.children[name] = node
        elif not isinstance(node, Directory):
            raise ValueError(f"Not a directory: {node}")
        return node

    def list_dir(self, output: list[str]) -> None:
        for line in output:
            prefix, name = line.split(" ", 1)
            if prefix == "dir":
                self.get_or_create_dir(name)
            else:
                file = File(name, size=int(prefix))
                self.pwd.children.setdefault(name, file)


def print_tree(node: Node, level: int = 0) -> None:
    indent = "  " * level
    print(f"{indent}- {node}")
    if isinstance(node, Directory):
        for child in node.children.values():
            print_tree(child, level + 1)


def total_size(node: Node) -> int:
    if isinstance(node, Directory):
        return sum(total_size(child) for child in node.children.values())
    if isinstance(node, File):
        return node.size
    raise NotImplementedError(node)


def find_leaf_dirs(root: Directory) -> Iterator[Directory]:
    subdirs = [c for c in root.children.values() if isinstance(c, Directory)]
    if not subdirs:
        yield root
    else:
        for child in subdirs:
            yield from find_leaf_dirs(child)


def find_total_size_bounded(root: Directory, max_size: int = 100_000) -> int:
    total = 0
    todo = deque(find_leaf_dirs(root))
    while todo:
        d = todo.popleft()
        size = total_size(d)
        if size <= max_size:
            total += size
            if d.parent:
                todo.append(d.parent)
    return total


total_disk_size = 70_000_000
wanted_free_size = 30_000_000


def find_smallest_dir_to_delete(root: Directory, min_size: int) -> int:
    smallest = total_disk_size
    todo = deque(find_leaf_dirs(root))
    while todo:
        d = todo.popleft()
        size = total_size(d)
        if size < smallest:
            if size >= min_size:
                smallest = size
            elif d.parent:
                todo.append(d.parent)
    return smallest


def main() -> None:
    log = Path("input.txt").read_text()
    root = Session().replay(log)
    print_tree(root)
    print()

    print("Part 1:", find_total_size_bounded(root))

    free_size = total_disk_size - total_size(root)
    min_size_to_delete = wanted_free_size - free_size
    print("Part 2:", find_smallest_dir_to_delete(root, min_size_to_delete))


if __name__ == "__main__":
    main()
