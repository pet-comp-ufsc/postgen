'''Post drawer module.'''
from .post import Post
from dataclasses import dataclass


@dataclass
class PostDrawer:
    post: Post
