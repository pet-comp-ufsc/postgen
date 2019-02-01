from pathlib import Path
from sys import argv
from textwrap import dedent

from postgen import Post, Size, make_image, Theme


if __name__ == '__main__':
    post = Post(
        title='Tutoriais do PET CCO',
        description=dedent('''
            Precisando aprender uma linguagem ou ferramenta, seja para a
            graduação, trabalho ou diversão?

            O PET Computação UFSC oferece um repositório de tutoriais!
            Acesse: pet.inf.ufsc.br/tutoriais.
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
