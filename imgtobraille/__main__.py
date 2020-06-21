"""Main program."""
import argparse
import sys
import time

import tqdm
from imgtobraille import iutils
from imgtobraille.converter import Braille


def initialize_args(args) -> argparse.Namespace:
    """Initialize commandline arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'PATH',
        action='store',
        metavar='path',
        help='Input path (file/dir)',
    )
    parser.add_argument(
        '-w',
        action='store',
        metavar='width',
        default=100,
        type=int,
        help='Width of print in characters',
    )
    parser.add_argument(
        '-d',
        action='store',
        metavar='dithering',
        default=2,
        type=int,
        help='1=threshold, 2=Floyd–Steinberg, 3=random, 4=none',
    )
    parser.add_argument(
        '-t',
        action='store',
        metavar='time',
        default=0.05,
        type=float,
        help='Frame time in seconds',
    )
    parser.add_argument(
        '-s',
        action='store_true',
        default=False,
        help='Silent',
    )
    return parser.parse_args(args)


def main():
    """Run main loop."""

    def good(string):
        """Returns green sign with '+' """
        return f'\033[{32}m{"[+] "}\033[0m{string}'

    def bad(string):
        """Returns red sign with '-' """
        return f'\033[{31}m{"[-] "}\033[0m{string}'

    def info(string):
        """Returns yellow sign with '!' """
        return f'\033[{33}m{"[!] "}\033[0m{string}'

    verbose = '-s' not in sys.argv
    locals()['good'] = good if verbose else lambda string: None
    locals()['bad'] = bad if verbose else lambda string: None
    locals()['info'] = info if verbose else lambda string: None

    args = initialize_args(["/home/kemali2/Pycharm/1-Projects/ImgToBraille/demos/1.jpg"])

    print(good('Getting image path(s)'))
    paths = iutils.get_paths(args.PATH)
    print(good(f'Found {len(paths)} images'))

    brailles = [Braille(path, width=args.w, method=args.d) for path in tqdm.tqdm(
        paths,
        unit=' f',
        disable='-s' in sys.argv,
        ascii=True,
    )]

    print(brailles[0])
    if len(brailles) > 1 and input('Play animation? [Y/n]: ') in 'Yy':
        while True:
            for new_frame in brailles:
                print(new_frame)
                time.sleep(args.t)


if __name__ == '__main__':
    main()
