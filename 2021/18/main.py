r"""
              /´¯/)
            ,/¯../
           /..../
     /´¯/'...'/´¯¯`·¸
  /'/.../..../......./¨¯\
('(...´...´.... ¯~/'...')
 \.................'...../
  ''...\.......... _.·´
    \..............(
      \.............\
"""
from __future__ import annotations

import copy
import json
import math
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Tuple


@dataclass
class Node:
    parent: Optional[Node] = field(init=False, default=None)
    left: Optional[Node] = None
    right: Optional[Node] = None
    value: int = 0

    def __post_init__(self):
        if not self.is_leaf:
            self.left.parent = self
            self.right.parent = self

    @classmethod
    def leaf(cls, value: int) -> Node:
        return cls(None, None, value)

    @property
    def is_leaf(self) -> bool:
        return not (self.left or self.right)

    @classmethod
    def parse(cls, text: str) -> Node:
        return cls.from_list(json.loads(text))

    @classmethod
    def from_list(cls, obj) -> Node:
        if isinstance(obj, int):
            return cls.leaf(obj)
        left, right = obj
        return cls(cls.from_list(left), cls.from_list(right))

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.to_list()})"

    def __add__(self, other: Node) -> Node:
        # Our methods are not pure, so we need to copy the inputs here to avoid
        # in-place modifications. Bad!
        left = copy.deepcopy(self)
        right = copy.deepcopy(other)
        return Node(left, right).reduce()

    def __eq__(self, other):
        return self.to_list() == other.to_list()

    def to_list(self):
        if self.is_leaf:
            return self.value
        return [self.left.to_list(), self.right.to_list()]

    def reduce(self):
        if not self.is_leaf:
            while self.try_explode() or self.try_split():
                pass
        return self

    def split(self) -> Node:
        half = self.value / 2
        left = self.leaf(math.floor(half))
        right = self.leaf(math.ceil(half))
        n = Node(left, right)
        n.parent = self.parent
        return n

    def try_explode(self) -> bool:
        match = self._dfs(lambda n, d: d == 4 and not n.is_leaf)
        if not match:
            return False

        n, _ = match
        assert n.parent and n.left and n.right, n

        left = n.left_neighbour()
        right = n.right_neighbour()
        if left:
            left.value += n.left.value
        if right:
            right.value += n.right.value

        n.left = n.right = None
        n.value = 0
        return True

    def left_neighbour(self) -> Optional[Node]:
        child = self
        parent = self.parent
        while parent:
            if parent.left is not child:
                node = parent.left
                while node.right:  # type: ignore
                    node = node.right  # type: ignore
                return node if node.is_leaf else None  # type: ignore
            child = parent
            parent = parent.parent
        return None

    def right_neighbour(self) -> Optional[Node]:
        child = self
        parent = self.parent
        while parent:
            if parent.right is not child:
                node = parent.right
                while node.left:  # type: ignore
                    node = node.left  # type: ignore
                return node if node.is_leaf else None  # type: ignore
            child = parent
            parent = parent.parent
        return None

    def try_split(self) -> bool:
        match = self._dfs(lambda n, _: n.value >= 10)
        if not match:
            return False

        to_split, path = match
        i = path[-1]
        to_split.parent[i] = to_split.split()  # type: ignore
        return True

    def __setitem__(self, i: int, n: Node):
        if i == 0:
            self.left = n
        elif i == 1:
            self.right = n
        else:
            raise IndexError(i)
        if n:
            n.parent = self

    def _dfs(self, cond: Condition) -> Optional[Tuple[Node, Path]]:
        def visit(node: Node, depth: int, path: Path):
            if cond(node, depth):
                return node, path

            if isinstance(node, Node):
                for i, child in enumerate([node.left, node.right]):
                    if child:
                        match = visit(child, depth + 1, path + [i])
                        if match is not None:
                            return match
            return None

        return visit(self, 0, [])

    def magnitude(self) -> int:
        if self.is_leaf:
            return self.value
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()  # type: ignore


Condition = Callable[[Node, int], bool]
Path = List[int]


def main():
    with open("input.txt") as f:
        lines = f.read().splitlines()
    numbers = [Node.parse(line) for line in lines]

    head, *tail = numbers
    total = sum(tail, head)
    print("Part 1:", total.magnitude())

    max_mag = max(
        (a + b).magnitude()
        for i, a in enumerate(numbers)
        for j, b in enumerate(numbers)
        if i != j
    )
    print("Part 2:", max_mag)
    print(__doc__)


if __name__ == "__main__":
    main()


def test_explode():
    def explode(a: list) -> Node:
        n = Node.from_list(a)
        assert n.try_explode()
        return n

    a = [[[[[9, 8], 1], 2], 3], 4]
    b = [[[[0, 9], 2], 3], 4]
    assert explode(a) == Node.from_list(b)

    a = [7, [6, [5, [4, [3, 2]]]]]
    b = [7, [6, [5, [7, 0]]]]
    assert explode(a) == Node.from_list(b)

    a = [[6, [5, [4, [3, 2]]]], 1]
    b = [[6, [5, [7, 0]]], 3]
    assert explode(a) == Node.from_list(b)

    a = [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]
    b = [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]
    assert explode(a) == Node.from_list(b)


def test_split():
    assert Node.leaf(11).split() == Node.from_list([5, 6])


def test_reduce():
    a = [[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]
    b = [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    assert Node.from_list(a).reduce() == Node.from_list(b)


def test_magnitude():
    n = [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
    assert Node.from_list(n).magnitude() == 3488
