from dataclasses import dataclass
from functools import lru_cache
from typing import Callable

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


class Solver:
    def __init__(self, graph: Graph):
        self.tasks = {t.id: t for t in graph.tasks}
        self.cache: dict[str, int] = {}
        self.seen: set[str] = set()

    def compute(self, task_id: str = "root") -> int:
        return self._compute_task(self.tasks[task_id])

    def _compute_task(self, task: Task) -> int:
        inputs = [self._resolve(value) for value in task.inputs]
        output = task.op(*inputs)
        self.cache[task.id] = output
        return output

    def _resolve(self, value: Value) -> int:
        if isinstance(value, LiteralValue):
            return value.value

        if isinstance(value, OutputValue):
            tid = value.task_id
            if tid in self.cache:
                return self.cache[tid]
            if tid in self.seen:
                raise GraphIsCyclic(tid)
            self.seen.add(tid)
            return self._compute_task(self.tasks[tid])

        raise NotImplementedError(value)

    def find_human_input(self) -> int:
        root = self.tasks["root"]
        humn = self.tasks["humn"]

        @lru_cache(maxsize=None)
        def is_reachable(dst_id: str, src_id: str) -> bool:
            if dst_id == src_id:
                return True

            t = self.tasks[dst_id]
            return any(
                is_reachable(inp.task_id, src_id)
                for inp in t.inputs
                if isinstance(inp, OutputValue)
            )

        def split(root: Task) -> tuple[OutputValue, OutputValue]:
            ours = next(inp for inp in root.inputs if is_reachable(inp.task_id, humn.id))  # type: ignore
            theirs = next(inp for inp in root.inputs if inp is not ours)
            return ours, theirs  # type: ignore

        ours, theirs = split(root)
        target = self.compute(theirs.task_id)

        while ours.task_id != humn.id:
            t = self.tasks[ours.task_id]
            ours, theirs = split(t)
            ours_lhs = t.inputs.index(ours) == 0

            x = self.compute(theirs.task_id)

            if t.op is OPS["+"]:
                target -= x
            elif t.op is OPS["*"]:
                target //= x
            elif t.op is OPS["-"]:
                target = target + x if ours_lhs else x - target
            elif t.op is OPS["/"]:
                target = target * x if ours_lhs else x // target

        # Verify result:
        humn.inputs[0].value = target  # type: ignore
        root.op = lambda a, b: int(a == b)
        self.cache.clear()
        self.seen.clear()
        assert self.compute(root.id) == 1

        return target


class GraphIsCyclic(Exception):
    pass


OPS = {
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
            t = Task(tid, OPS[op], inputs=[OutputValue(dep) for dep in (a, b)])
        else:
            t = Task(tid, op=lambda x: x, inputs=[LiteralValue(x)])
        g.tasks.append(t)
    return g


s = Solver(parse_graph(read_input()))
print("Part 1:", s.compute())
print("Part 2:", s.find_human_input())
