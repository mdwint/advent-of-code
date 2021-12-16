import math
from dataclasses import dataclass
from typing import List

hex_to_bin = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


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


@dataclass
class Stream:
    bits: str
    pos: int = 0

    def read(self, length: int) -> str:
        end = self.pos + length
        if len(self.bits) <= end:
            raise EndOfStream()
        result = self.bits[self.pos : end]
        self.pos = end
        return result


def parse(msg: str) -> Node:
    bits = "".join(hex_to_bin[x] for x in msg)
    s = Stream(bits)
    return parse_node(s)


def parse_node(s: Stream) -> Node:
    version = int(s.read(3), 2)
    type_id = int(s.read(3), 2)
    node: Node
    if type_id == 4:
        node = parse_literal(s)
    else:
        node = parse_operator(s)
        node.type_id = type_id
    node.version = version
    return node


def parse_literal(s: Stream) -> Literal:
    number = ""
    while True:
        more = int(s.read(1), 2)
        number += s.read(4)
        if not more:
            break
    return Literal(0, int(number, 2))


def parse_operator(s: Stream) -> Operator:
    children: List[Node] = []
    length_type_id = int(s.read(1), 2)
    if length_type_id == 0:
        length = int(s.read(15), 2)
        end = s.pos + length
        while s.pos < end:
            children.append(parse_node(s))
    else:
        num_subpackets = int(s.read(11), 2)
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
