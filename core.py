import json
from pathlib import Path

from pydantic import BaseModel, Field

T = 50


class Node(BaseModel):
    name: str = Field(default="")
    keys: list[int] = Field(default_factory=list)
    node_refs: list[str] = Field(default_factory=list)
    data: dict[int, str] = Field(default_factory=dict)

    def __init__(self, file_name: str = None):
        if file_name is None:
            file_name = 'node'

        if Path(file_name).is_file():
            with open(file_name, 'r') as file:
                raw_data = file.read()
                data = json.loads(raw_data)
                super().__init__(**data)
        else:
            super().__init__()

        self.name = file_name

    def __del__(self):
        with open(self.name, 'w') as file:
            file.write(self.model_dump_json(exclude={'name'}))

    @property
    def size(self) -> int:
        return len(self.data)

    @property
    def is_full(self) -> bool:
        return self.size == (2 * T - 1)
