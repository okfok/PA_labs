import json
import os
from pathlib import Path

from pydantic import BaseModel, Field

T = 2


class Node(BaseModel):
    name: str = Field(default="")
    keys: list[int] = Field(default_factory=list)
    node_refs: list[str] = Field(default_factory=list)
    data: dict[int, str] = Field(default_factory=dict)
    leaf: bool = Field(default=False)

    def __init__(self, file_name: str = None):
        if file_name is None:
            file_name = 'node'

        if Path(file_name).is_file():
            with open(file_name, 'r') as file:
                raw_data = file.read()
                data = json.loads(raw_data)
                super().__init__(**data)
            os.remove(file_name)
        else:
            super().__init__()

        self.name = file_name

    def __del__(self):
        with open(self.name, 'w') as file:
            file.write(self.model_dump_json(exclude={'name'}))

    @property
    def size(self) -> int:
        return len(self.keys)

    @property
    def is_full(self) -> bool:
        return self.size == (2 * T - 1)

    def rename(self, fn: str = None):
        if fn is None:
            fn = self.name
        for i in range(len(self.node_refs)):
            Node(self.node_refs[i]).rename(fn + f'-{i}')
            self.node_refs[i] = fn + f'-{i}'
        self.name = fn


class Tree:
    node: Node

    def __init__(self):
        self.root = Node()
        self.root.leaf = True

    def insert(self, key, val):
        if self.root.is_full:
            temp = Node("temp")
            self.root = temp
            temp.node_refs.insert(0, 'node')
            temp.rename('node')
            self.split_child(temp, 0)
            self.insert_non_full(temp, key, val)
        else:
            self.insert_non_full(self.root, key, val)

    @staticmethod
    def split_child(x: Node, i):
        # y = Node(x.node_refs[i])
        z = Node("temp")
        z.leaf = Node(x.node_refs[i]).leaf
        x.node_refs.insert(i + 1, z.name)


        x.rename()

        x.keys.insert(i, y.keys[T - 1])

        z.keys = y.keys[T:(2 * T) - 1]
        y.keys = y.keys[0:T - 1]
        if not y.leaf:
            z.child = y.child[T:(2 * T)]
            y.child = y.child[0:T - 1]

    def insert_non_full(self, x: Node, key, val):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append((None, None))
            while i >= 0 and key < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = key
        else:
            while i >= 0 and key < x.keys[i]:
                i -= 1
            i += 1
            if (child_i := Node(x.node_refs[i])).is_full:
                self.split_child(x, i)
                if key > x.keys[i]:
                    i += 1
            self.insert_non_full(child_i, key, val)

