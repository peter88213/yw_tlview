"""Provide a class with key definitions.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvtlview.tlv_locale import _


class GenericKeys:

    OPEN_HELP = ('<F1>', 'F1')
    OPEN_PROJECT = ('<Control-o>', f'{_("Ctrl")}-O')
    QUIT_PROGRAM = ('<Control-q>', f'{_("Ctrl")}-Q')
    RELOAD_PROJECT = ('<Control-r>', f'{_("Ctrl")}-R')
    SAVE_AS = ('<Control-S>', f'{_("Ctrl")}-{_("Shift")}-S')
    SAVE_PROJECT = ('<Control-s>', f'{_("Ctrl")}-S')
    UNDO = ('<Control-z>', f'{_("Ctrl")}-Z')
