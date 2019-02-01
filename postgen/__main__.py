from pathlib import Path
from sys import argv
from textwrap import dedent

from postgen import Post, Size, make_image


if __name__ == '__main__':
    post = Post(
        title='Oficinas de Verão',
        description=dedent('''
            Está em Florianópolis em fevereiro e gostaria de aproveitar as
            férias para aprender ShellScript ou LaTeX?

            Participe de nossas oficinas de verão! Informações e calendário na
            descrição.
        '''),
        logo=Path('logo-pet-notvec.png')
    )

    img = make_image(post, size=Size(1080, 1080), bgcolor=(105, 176, 229, 255))

    if '--display' in argv:
        img.show()
    else:
        img.save('output.png')
