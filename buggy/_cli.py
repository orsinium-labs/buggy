# built-in
import sys
import webbrowser
from argparse import ArgumentParser
from typing import List, NoReturn, TextIO

# app
from ._core import get_links, get_tracker_url


def main(argv: List[str], stream: TextIO = sys.stdout) -> int:
    parser = ArgumentParser()
    parser.add_argument('name')
    args = parser.parse_args(argv)

    links = get_links(name=args.name)
    url = get_tracker_url(links=links)
    if url is None:
        print('cannot find bug tracker URL', file=stream)
        return 1
    print(url, file=stream)
    webbrowser.open_new_tab(url=url)
    return 0


def entrypoint() -> NoReturn:
    sys.exit(main(argv=sys.argv[1:]))
