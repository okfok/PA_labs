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

    def insert_not_full(self, key, val):
        i = self.size - 1
        if self.leaf:
            self.keys.append(None)
            while i >= 0 and self.keys[i] > key:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = key
            self.data[key] = val
        else:
            while i >= 0 and self.keys[i] > key:
                i -= 1
            if (child := Node(self.node_refs[i + 1])).is_full:
                self.split_child(i + 1, child)
                if self.keys[i + 1] < key:
                    i += 1
            child.insert_not_full(key, val)

    def split_child(self, i, y: 'Node'):
        z = Node()
        z.keys = y.keys[T:(2 * T) - 1]
        if not y.leaf:
            z.node_refs = y.node_refs[T:2 * T]
            y.node_refs = y.node_refs[0:T]
        self.node_refs.insert(i + 1, z.name)
        self.keys.insert(i, y.keys[T - 1])
        y.keys = y.keys[0:T - 1]

        z.data = {key: y.data[key] for key in z.keys}

        for key in self.keys:
            if (val := y.data.get(key)) is not None:
                self.data[key] = val

        y.data = {key: y.data[key] for key in y.keys}


class Tree:
    node: Node

    def __init__(self):
        self.root = Node(name_conf.root)

    def insert(self, key, val):
        if self.root.is_full:
            s = Node()
            s.node_refs.append(self.root.name)

            s.split_child(0, self.root)
            i = 0
            if s.keys[0] < key:
                i += 1
            Node(s.node_refs[i]).insert_not_full(key, val)
            self.root = s
            name_conf.root = self.root.name
        else:
            self.root.insert_not_full(key, val)


def clean():
    folder = 'nodes/'
    try:
        os.remove(CONF_FILE_NAME)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (CONF_FILE_NAME, e))
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
