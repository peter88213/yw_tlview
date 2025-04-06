"""Helper module for opening documents.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/yw_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

from tlv.platform.platform_settings import PLATFORM


def open_document(document):
    """Open a document with the operating system's standard application."""
    if PLATFORM == 'win':
        os.startfile(os.path.normpath(document))
        return

    if PLATFORM == 'ix':
        os.system('xdg-open "%s"' % os.path.normpath(document))
        return

    if PLATFORM == 'mac':
        os.system('open "%s"' % os.path.normpath(document))
