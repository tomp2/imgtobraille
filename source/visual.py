"""Wrappers for managing normal/silent output with colorful prefixes"""


def good(string):
    """Returns green sign with '+' """
    return f'\033[{32}m{"[+] "}\033[0m{string}'


def bad(string):
    """Returns red sign with '-' """
    return f'\033[{31}m{"[-] "}\033[0m{string}'


def info(string):
    """Returns yellow sign with '!' """
    return f'\033[{33}m{"[!] "}\033[0m{string}'


def silent():
    """Function to do nothing if output is silenced"""
