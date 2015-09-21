from __future__ import print_function
import sys
import argparse
from crypt_keeper.entry import Entry

__allowed_commands__ = ["show", "list", "edit", "delete"]


def _parse_args():
    parser = argparse.ArgumentParser(description="Manage secrets stored in Redis")
    parser.add_argument("--dir", "-d", default="/etc/crypt-keeper",
                        help="The directory containing the encryption keys")
    parser.add_argument("command", metavar="COMMAND", choices=__allowed_commands__,
                        help="the command to run %s" % __allowed_commands__)
    parser.add_argument("key", metavar="KEY", nargs="?", help="The Redis key to work on")

    return parser.parse_args()


def _fetch_entry(args):
    return Entry(key=args.key, crypt_dir=args.dir)


def _handle_show(args):
    return _fetch_entry(args).view()


def _handle_list(args):
    return Entry.list_keys()


def _handle_edit(args):
    return _fetch_entry(args).edit()


def _handle_delete(args):
    return _fetch_entry(args).delete()


def main():
    commands = {
        "list": _handle_list,
        "show": _handle_show,
        "edit": _handle_edit,
        "delete": _handle_delete
    }

    args = _parse_args()
    sys.exit(commands[args.command](args))
