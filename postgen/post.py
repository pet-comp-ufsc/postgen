'''Module for posts' definition.'''
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent

import toml


@dataclass
class Post:
    title: str
    description: str
    logo: Path

    @staticmethod
    def from_path(path: Path) -> 'Post':
        data = toml.load(path)

        return Post(
            title=data['about']['title'],
            description=dedent(data['about']['description']),
            logo=data['images']['logo'],
        )
