'''Module for posts' definition.'''
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Post:
    title: str
    description: str
    logo: Path = Path('logo-pet-notvec.png')
