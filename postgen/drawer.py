'''Post drawer module.'''
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from textwrap import wrap
from typing import Tuple, NamedTuple

from cairosvg import svg2png
from PIL import Image, ImageDraw, ImageFont

from .post import Post


class FontNotFound(Exception):
    pass


class RelativePos:
    @dataclass
    class Center:
        offset: int = 0

    @dataclass
    class Opposite:
        offset: int = 0


@dataclass
class Font:
    family: str
    size: int


class Pos(NamedTuple):
    x: int
    y: int


class Size(NamedTuple):
    width: int
    height: int


def apply_relatives(pos: Pos, size: Size, obj_size: Size):
    x, y = pos
    if isinstance(x, RelativePos.Center):
        x = x.offset + (size.width - obj_size.width) / 2
    elif isinstance(x, RelativePos.Opposite):
        x = x.offset + size.width - obj_size.width

    if isinstance(y, RelativePos.Center):
        y = y.offset + (size.height - obj_size.height) / 2
    if isinstance(y, RelativePos.Opposite):
        y = y.offset + size.height - obj_size.height

    return x, y


@dataclass
class Drawer:
    size: Size

    def __post_init__(self):
        self.img = Image.new('RGBA', self.size, (255, 255, 255, 0))
        self.draw = ImageDraw.Draw(self.img)

    def draw_image(self, path: Path, pos: Pos, resize_to: Size = None):
        if not isinstance(path, Path):
            path = Path(path)

        if path.suffix == '.svg':
            mempng = BytesIO(svg2png(url=str(path)))
            img = Image.open(mempng)
        else:
            img = Image.open(path)

        if resize_to:
            rw, rh = resize_to
            if rw == 0:
                rw = img.width * rh // img.height
            elif rh == 0:
                rh = img.height * rw // img.width
            img = img.resize((rw, rh))

        self.img.alpha_composite(
            img,
            apply_relatives(pos, self.size, obj_size=Size(*img.size))
        )

    def draw_line(self, p1: Pos, p2: Pos):
        raise NotImplementedError()

    def draw_rect(self, origin: Pos, size: Size, fill: Tuple[int, int, int]):
        self.draw.rectangle((origin, size), fill=fill)

    def draw_text(self, text: str, pos: Pos, font: Font = None):
        if font:
            try:
                font = ImageFont.truetype(font.family, size=font.size)
                not_found = False
            except OSError:
                not_found = True

            if not_found:
                raise FontNotFound(font.family)
        else:
            font = self.draw.getfont()

        text_size = Size(*self.draw.textsize(text, font=font))

        pos = apply_relatives(pos, self.size, obj_size=text_size)

        self.draw.text(pos, text, font=font)


def fit(text: str, columns: int):
    return '\n'.join(wrap(text, width=32))


def make_image(post: Post, size: Size, bgcolor=(95, 166, 219, 255)):
    drawer = Drawer(size)

    drawer.draw_rect(Pos(0, 0), size, fill=bgcolor)

    drawer.draw_text(
        post.title,
        Pos(RelativePos.Center(), 120),
        font=Font(family='DejaVuSansMono', size=72),
    )

    drawer.draw_text(
        fit(post.description, 32),
        Pos(RelativePos.Center(), 240),
        font=Font(family='DejaVuSansMono', size=48),
    )

    drawer.draw_image(
        post.logo,
        pos=Pos(RelativePos.Opposite(-40), RelativePos.Opposite(-40)),
        resize_to=Size(280, 0)
    )

    return drawer.img
