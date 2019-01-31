from sys import argv
from textwrap import dedent

from postgen import Post, Size, make_image


if __name__ == '__main__':
    post = Post(
        title='Hello, world!',
        description=dedent('''
            Here we are to present you the best lorem ispum for your
            facebook posts. Be awesome and yay yay yay :*.
        '''),
    )

    img = make_image(post, size=Size(1080, 1080))

    if '--display' in argv:
        img.show()
    else:
        img.save('rosca.png')
