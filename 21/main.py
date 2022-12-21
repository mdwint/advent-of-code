from dataclasses import dataclass
from typing import Any, Callable

from aoc import read_input


@dataclass
class Value:
    pass


@dataclass
class LiteralValue(Value):
    value: int


@dataclass
class OutputValue(Value):
    task_id: str


@dataclass
class Task:
    id: str
    op: Callable
    inputs: list[Value]


@dataclass
class Graph:
    tasks: list[Task]


def compute(graph: Graph) -> int:
    tasks = {t.id: t for t in graph.tasks}

    cache: dict[str, Any] = {}
    seen: set[str] = set()

    def resolve(value: Value):
        if isinstance(value, LiteralValue):
            return value.value

        if isinstance(value, OutputValue):
            tid = value.task_id
            if tid in cache:
                return cache[tid]
            if tid in seen:
                raise GraphIsCyclic(tid)
            seen.add(tid)
            return compute_task(tasks[tid])

        raise NotImplementedError(value)

    def compute_task(task: Task) -> int:
        inputs = [resolve(value) for value in task.inputs]
        output = task.op(*inputs)
        print(task.id, inputs, "->", output)
        cache[task.id] = output
        return output

    return compute_task(tasks["root"])


class GraphIsCyclic(Exception):
    pass


ops = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a // b,
}


def parse_graph(text: str) -> Graph:
    g = Graph([])
    for line in text.splitlines():
        tid, expr = line.split(": ", 1)
        try:
            x = int(expr)
        except ValueError:
            a, op, b = expr.split(" ", 2)
            t = Task(tid, ops[op], inputs=[OutputValue(dep) for dep in (a, b)])
        else:
            t = Task(tid, op=lambda x: x, inputs=[LiteralValue(x)])
        g.tasks.append(t)
    return g


g = parse_graph(read_input())
print("Part 1:", compute(g))
# print("Part 2:", 0)
