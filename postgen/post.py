'''Module for posts' definition.'''
from dataclasses import dataclass
from pathlib import Path
from textwrap import wrap
from typing import Tuple
import io

from PIL import Image, ImageDraw, ImageFont
from cairosvg import svg2png


def default_draw(
        post,
        logo_pos=(-40, -40),
        logo_resize=None,
        size: Tuple[int, int] = (1200, 628),
        title_size: int = 72,
        desc_size: int = 48,
        ):
    BGCOLOR = 0xffdba65f

    img = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    title_font = ImageFont.truetype('verdana', size=title_size)
    desc_font = ImageFont.truetype('verdana', size=desc_size)

    draw.rectangle(((0, 0), size), fill=BGCOLOR)

    draw_text(
        draw,
        size,
        post.title,
        wcenter=True,
        offset=(0, 120),
        font=title_font
    )

    draw_text(
        draw,
        size,
        '\n'.join(wrap(post.description, width=32)),
        wcenter=True,
        offset=(0, 240),
        font=desc_font,
    )

    draw_logo(
        draw,
        img,
        logo_pos,
        post.logo,
        canvas_size=size,
        logo_resize=logo_resize,
    )

    return img


def draw_logo(
        draw,
        image,
        pos,
        path: Path,
        canvas_size=(0, 0),
        logo_resize=None):
    x, y = pos
    w, h = canvas_size

    if path.suffix == '.svg':
        mempng = io.BytesIO(svg2png(url=str(path)))
        img = Image.open(mempng)
    else:
        img = Image.open(path)

    if logo_resize:
        print('resizing logo...')
        rw, rh = logo_resize
        if rw == 0:
            rw = img.width * rh // img.height
        elif rh == 0:
            rh = img.height * rw // img.width
        img = img.resize((rw, rh))

    if canvas_size != (0, 0):
        if x < 0:
            x = w + x - img.size[0]
        if y < 0:
            y = h + y - img.size[1]

    image.alpha_composite(img, (x, y))


def draw_text(
        draw,
        size,
        text,
        wcenter=False,
        hcenter=False,
        offset=(0, 0),
        **kwargs):
    try:
        font = kwargs['font']
    except KeyError:
        font = draw.getfont()

    w, h = size
    tw, th = draw.textsize(text, font=font)

    ox, oy = offset
    x = (w - tw) / 2 if wcenter else 0
    y = (h - th) / 2 if hcenter else 0

    draw.text((x + ox, y + oy), text, **kwargs)


@dataclass
class Post:
    title: str
    description: str
    logo: Path = Path('logo-pet-notvec.png')
