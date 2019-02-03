from pathlib import Path

from carl import command, Arg
import toml

from postgen import Post, Size, make_image, Theme


@command
def run(
        post: Path,
        theme: Path = None,
        display: Arg(action='store_true') = False,
        output: Path = None,
):
    post = Post.from_path(post)
    theme = Theme.from_path(theme)

    img = make_image(post, size=Size(1080, 1080), theme=theme)

    if display:
        img.show()

        if output is not None:
            img.save(output)
    else:
        img.save(output if output else 'output.png')


if __name__ == '__main__':
    run.run()
