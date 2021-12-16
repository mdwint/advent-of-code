import io
import math
from dataclasses import dataclass
from typing import List


@dataclass
class Node:
    version: int


@dataclass
class Literal(Node):
    number: int


@dataclass
class Operator(Node):
    type_id: int
    children: List[Node]


class EndOfStream(Exception):
    pass


def read_int(s: io.StringIO, size: int, base: int = 2) -> int:
    return int(s.read(size), base)


def parse(msg: str) -> Node:
    s = io.StringIO("".join(bin(int(x, 16))[2:].zfill(4) for x in msg))
    return parse_node(s)


def parse_node(s: io.StringIO) -> Node:
    version = read_int(s, 3)
    type_id = read_int(s, 3)
    node: Node
    if type_id == 4:
        node = parse_literal(s)
    else:
        node = parse_operator(s)
        node.type_id = type_id
    node.version = version
    return node


def parse_literal(s: io.StringIO) -> Literal:
    number = ""
    while True:
        more = read_int(s, 1)
        number += s.read(4)
        if not more:
            break
    return Literal(0, int(number, 2))


def parse_operator(s: io.StringIO) -> Operator:
    children: List[Node] = []
    length_type_id = read_int(s, 1)
    if length_type_id == 0:
        length = read_int(s, 15)
        end = s.tell() + length
        while s.tell() < end:
            children.append(parse_node(s))
    else:
        num_subpackets = read_int(s, 11)
        for _ in range(num_subpackets):
            children.append(parse_node(s))
    return Operator(0, 0, children)


def version_sum(node: Node) -> int:
    v = node.version
    if isinstance(node, Operator):
        v += sum(version_sum(child) for child in node.children)
    return v


def part1(msg: str):
    root = parse(msg)
    # print(root)
    answer = version_sum(root)
    print("Part 1:", answer)


part1("D2FE28")
part1("38006F45291200")
part1("EE00D40C823060")
part1("8A004A801A8002F478")
part1("620080001611562C8802118E34")
part1("C0015000016115A2E0802F182340")
part1("A0016C880162017C3686B18A3D4780")
part1(open("input.txt").read().strip())


ops = {
    0: sum,
    1: math.prod,
    2: min,
    3: max,
    5: lambda x: int(x[0] > x[1]),
    6: lambda x: int(x[0] < x[1]),
    7: lambda x: int(x[0] == x[1]),
}


def calc(node: Node) -> int:
    if isinstance(node, Literal):
        return node.number

    if isinstance(node, Operator):
        args = [calc(child) for child in node.children]
        return ops[node.type_id](args)

    raise ValueError(node)


def part2(msg: str):
    root = parse(msg)
    # print(root)
    answer = calc(root)
    print("Part 2:", answer)


part2("9C0141080250320F1802104A08")
part2(open("input.txt").read().strip())
