import json
import os
import random
from pathlib import Path

from pydantic import BaseModel, Field

T = 2

CONF_FILE_NAME = 'names.conf'
NAME_PATH = 'nodes/node-'
NAME_CHARS = 'qwertyuiopasdfghjklzxcvbnm1234567890'


class NodeNameConf(BaseModel):
    root: str
    used_names: list[str] = Field(default_factory=list)

    def __init__(self):

        if Path(CONF_FILE_NAME).is_file():
            with open(CONF_FILE_NAME, 'r') as file:
                raw_data = file.read()
                data = json.loads(raw_data)
                super().__init__(**data)
            os.remove(CONF_FILE_NAME)
        else:
            super().__init__(root=NodeNameConf._rand_name())
            self.used_names.append(self.root)

    def save(self):
        with open(CONF_FILE_NAME, 'w') as file:
            file.write(self.model_dump_json())

    @staticmethod
    def _rand_name():
        return NAME_PATH + ''.join(random.choice(NAME_CHARS) for _ in range(50))

    def get_unique_name(self):
        name = NodeNameConf._rand_name()
        while name in self.used_names:
            name = NodeNameConf._rand_name()
        self.used_names.append(name)
        return name


name_conf = NodeNameConf()


class Node(BaseModel):
    name: str = Field(default="")
    keys: list[int] = Field(default_factory=list)
    node_refs: list[str] = Field(default_factory=list)
    data: dict[int, str] = Field(default_factory=dict)

    def __init__(self, file_name: str = None):
        if file_name is None:
            file_name = name_conf.get_unique_name()

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

    @property
    def leaf(self):
        return len(self.node_refs) == 0

    def insert_not_full(self, k):
        i = self.size - 1
        if self.leaf:
            self.keys.append(None)
            while i >= 0 and self.keys[i] > k:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = k
            # TODO: data insert
        else:
            while i >= 0 and self.keys[i] > k:
                i -= 1
            if (child := Node(self.node_refs[i + 1])).is_full:
                self.splitChild(i + 1, child)
                if self.keys[i + 1] < k:
                    i += 1
            child.insert_not_full(k)

    def split_child(self, i, y):
        z = Node("temp")
        for j in range(self.t - 1):
            z.keys[j] = y.keys[j + self.t]
        if not y.leaf:
            for j in range(self.t):
                z.C[j] = y.C[j + self.t]
        y.n = self.t - 1
        for j in range(self.n, i, -1):
            self.C[j + 1] = self.C[j]
        self.C[i + 1] = z
        for j in range(self.n - 1, i - 1, -1):
            self.keys[j + 1] = self.keys[j]
        self.keys[i] = y.keys[self.t - 1]
        self.n += 1


class Tree:
    node: Node

    def __init__(self):
        self.root = Node(name_conf.root)

    def insert(self, key, val):
        if self.root.is_full:
            root = self.root
            temp = Node()
            self.root = temp
            temp.node_refs.insert(0, root.name)

            name_conf.root = self.root.name

            self.split_child(temp, 0)
            self.insert_non_full(temp, key, val)
        else:
            self.insert_non_full(self.root, key, val)

    @staticmethod
    def split_child(x: Node, i):
        z = Node()
        x.node_refs.insert(i + 1, z.name)

        y = Node(x.node_refs[i])
        z = Node(x.node_refs[i + 1])

        x.keys.insert(i, y.keys[T - 1])

        z.keys = y.keys[T:(2 * T) - 1]
        y.keys = y.keys[0:T - 1]
        if not y.leaf:
            z.node_refs = y.node_refs[T:(2 * T)]
            y.node_refs = y.node_refs[0:T - 1]

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


def clean():
    os.remove(CONF_FILE_NAME)
    folder = 'nodes/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
