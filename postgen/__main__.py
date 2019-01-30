from sys import argv
from textwrap import dedent

from .post import Post, default_draw


if __name__ == '__main__':
    img = default_draw(
        Post(
            title='Hello, world!',
            description=dedent('''
                Here we are to present you the best lorem ispum for your
                facebook posts. Be awesome and yay yay yay :*.
            '''),
        ),
        size=(1080, 1080),
        logo_resize=(280, 0),
    )

    if '--display' in argv:
        img.show()
    else:
        img.save('rosca.png')
