"""Provide platform-dependent key definitions.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/yw_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tlv.tlv_locale import _
from tlv.platform.platform_settings import PLATFORM

if PLATFORM == 'mac':
    KEY_OPEN_PROJECT = ('<Command-o>', 'Cmd-O')
    KEY_RELOAD_PROJECT = ('<Command-r>', 'Cmd-R')
else:
    KEY_OPEN_PROJECT = ('<Control-o>', f'{_("Ctrl")}-O')
    KEY_RELOAD_PROJECT = ('<Control-r>', f'{_("Ctrl")}-R')

