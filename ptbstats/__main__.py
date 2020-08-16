# !/usr/bin/env python
import sys
import subprocess
from typing import Optional

from . import __version__ as ptb_stats_ver


def _git_revision() -> Optional[str]:
    try:
        output = subprocess.check_output(["git", "describe", "--long", "--tags"],
                                         stderr=subprocess.STDOUT)
    except (subprocess.SubprocessError, OSError):
        return None
    return output.decode().strip()


def print_ver_info() -> None:
    git_revision = _git_revision()
    print('ptbstats {}'.format(ptb_stats_ver) +
          (' ({})'.format(git_revision) if git_revision else ''))
    print('Python {}'.format(sys.version.replace('\n', ' ')))


def main() -> None:
    print_ver_info()


if __name__ == '__main__':
    main()
