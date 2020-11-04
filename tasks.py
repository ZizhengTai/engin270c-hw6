from collections import defaultdict
from dataclasses import dataclass
from math import ceil
from typing import Dict, List, Sequence, Tuple


@dataclass
class Task:
    id: int
    days: float
    edays: float = 0
    preds: Sequence[int] = ()

    @property
    def total_days(self) -> int:
        return ceil(self.days + self.edays)


@dataclass
class Edge:
    dst: int
    weight: float


Graph = Dict[int, Dict[int, int]]


tasks: Sequence[Task] = [
    Task(id=3, days=127),
    Task(id=5, days=8),
    Task(id=6, days=4, preds=[5]),
    Task(id=7, days=6),
    Task(id=8, days=15, preds=[5, 6]),
    Task(id=9, days=2, preds=[7, 8]),
    Task(id=10, days=0, preds=list(range(11, 21))),
    Task(id=11, days=0, preds=[5, 6, 8]),
    Task(id=12, days=4),
    Task(id=13, days=6, edays=5),
    Task(id=14, days=3, preds=[13]),
    Task(id=15, days=6, edays=6),
    Task(id=16, days=4, preds=[12, 13, 14, 15]),
    Task(id=17, days=3, preds=[16]),
    Task(id=18, days=3, preds=[12, 13]),
    Task(id=19, days=7, preds=[16]),
    Task(id=20, days=4, preds=[11]),
    Task(id=21, days=0, preds=[10]),
    Task(id=22, days=13.5),
    Task(id=23, days=13.5),
    Task(id=24, days=6, preds=[23]),
    Task(id=25, days=6, edays=11),
    Task(id=26, days=16, preds=[22, 23, 24, 25]),
    Task(id=27, days=4, preds=[26]),
    Task(id=28, days=18),
    Task(id=29, days=20, preds=[22, 23, 24, 25]),
    Task(id=31, days=14, edays=23, preds=[11]),
    Task(id=32, days=20, preds=[31, 21]),
    Task(id=33, days=22, preds=[23]),
    Task(id=35, days=20, preds=[9]),
    Task(id=36, days=34.2, preds=[35]),
    Task(id=37, days=3.8, preds=[35]),
    Task(id=38, days=46, preds=[36]),
    Task(id=39, days=4.6, preds=[47]),
    Task(id=40, days=0, preds=[35]),
    Task(id=41, days=13, preds=[22]),
    Task(id=42, days=12, preds=[23]),
    Task(id=43, days=7, preds=[24, 42]),
    Task(id=44, days=6, edays=14, preds=[25]),
    Task(id=45, days=24, preds=[26, 41, 42, 43, 44]),
    Task(id=46, days=6, preds=[27]),
    Task(id=47, days=15.5, preds=[28]),
    Task(id=48, days=18, preds=[29]),
    Task(id=49, days=46, preds=[21]),
    Task(id=50, days=0, preds=list(range(51, 56))),
    Task(id=51, days=0, preds=[31]),
    Task(id=52, days=12, preds=[41, 42, 43]),
    Task(id=53, days=20, preds=[44, 45, 46, 52, 47, 48]),
    Task(id=54, days=160, preds=[51, 32, 33]),
    Task(id=55, days=80, preds=[54]),
    Task(id=56, days=0, preds=[50]),
    Task(id=57, days=80, preds=[56]),
    Task(id=58, days=8, preds=[57]),
    Task(id=59, days=90, preds=[58]),
]


def make_graph(tasks: Sequence[Task]) -> Graph:
    task_id_to_task: Dict[int, Task] = {t.id: t for t in tasks}
    graph: Graph = defaultdict(dict)

    for dst_task in tasks:
        dst = dst_task.id

        for src in dst_task.preds:
            src_task = task_id_to_task[src]
            weight = src_task.total_days

            graph[src][dst] = weight

    return graph


def topo_sort(graph: Graph) -> List[int]:
    visited = set()
    rank = 0
    node_to_rank = {}

    def dfs(node: int) -> None:
        nonlocal rank

        if node in visited:
            return
        visited.add(node)

        for dst in graph[node]:
            dfs(dst)

        node_to_rank[node] = rank
        rank += 1

    for node in list(graph):
        dfs(node)

    def get_rev_rank(task_id: int) -> int:
        return -node_to_rank[task_id]

    return sorted(node_to_rank, key=get_rev_rank)


def longest_path(graph: Graph) -> Tuple[int, List[int]]:
    topo_ordered_nodes: Sequence[int] = topo_sort(graph)

    dist: Dict[int, int] = defaultdict(int)
    prev: Dict[int, int] = {}
    longest_path_len = 0
    longest_path_dst = 0

    for src in topo_ordered_nodes:
        for dst, weight in graph[src].items():
            new_dist = dist[src] + weight
            if dist[dst] < new_dist:
                dist[dst] = new_dist
                prev[dst] = src

            if longest_path_len < dist[dst]:
                longest_path_len = dist[dst]
                longest_path_dst = dst

    node = longest_path_dst
    longest_path_nodes = [node]
    while node in prev:
        node = prev[node]
        longest_path_nodes.append(node)
    longest_path_nodes.reverse()

    return longest_path_len, longest_path_nodes


task_graph = make_graph(tasks)
longest_path_days, longest_path_tasks = longest_path(task_graph)
print(f"{longest_path_days} days")
print(longest_path_tasks)
