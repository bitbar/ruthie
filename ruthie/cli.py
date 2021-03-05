#!/usr/bin/env python3

"""
ruthie

Run Unit Tests Harmoniously Incredibly Easy

Usage:
  ruthie parallel [--threads=<threads>] <path>
  ruthie discover classes [--group] <path>
  ruthie -h | --help
  ruthie --version

Commands:
  parallel                                  Discover all test classes in given path and run them in parallel
  discover classes                          Discover all test classes in given path and print them in the console

Options:
  -t <threads> --threads=<threads>          Number of parallel threads [default: 2]
  -g --group                                Group results [default: False]
  -s --skip-cleanup                         Skip cleanup of results when running on prodbuild
  -h --help                                 Show this screen
  --version                                 Show version

Examples:
  ruthie parallel unittests
"""


from inspect import getmembers, isclass
from docopt import docopt
from ruthie import __version__ as version
from ruthie import commands


def main():
    """Main CLI entrypoint."""
    options = docopt(__doc__, version=version)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in list(options.items()):
        _k = k.replace('-', '_')
        if hasattr(commands, _k) and v:
            module = getattr(commands, _k)
            _commands = getmembers(module, isclass)
            command = [command[1] for command in _commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
