from pathlib import Path
from sys import argv
from textwrap import dedent

from postgen import Post, Size, make_image, Theme


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

    theme = Theme(
        fgcolor=(95, 166, 219, 255),
        bgcolor=(255, 255, 255, 255)
    )

    img = make_image(post, size=Size(1080, 1080), theme=theme)

    if '--display' in argv:
        img.show()
    else:
        output_index = argv.index('--output')
        if output_index > 0:
            img.save(argv[output_index + 1])
        else:
            img.save('output.png')
