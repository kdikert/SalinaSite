#!/usr/bin/env python
import os
import sys


def is_development_environment():
    subpath = os.path.dirname(__file__)
    while True:
        if os.path.basename(subpath) == 'src':
            return True
        next_subpath = os.path.dirname(subpath)
        if next_subpath == subpath:
            return False
        subpath = next_subpath


if __name__ == "__main__":
    if is_development_environment():
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "salinasite.settings_dev")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "salinasite.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

