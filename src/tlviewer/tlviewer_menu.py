"""Provide a menu class for the timeline viewer.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/yw_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import messagebox

import tkinter as tk
from tlv.platform.platform_settings import KEYS
from tlv.platform.platform_settings import PLATFORM
from tlv.tlv_locale import _
from tlviewer.key_definitions import KEY_OPEN_PROJECT
from tlviewer.key_definitions import KEY_RELOAD_PROJECT
from tlviewer.tlviewer_globals import prefs


class TlviewerMenu(tk.Menu):

    def __init__(self, master, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)

        # "File" menu.
        self.fileMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=_('File'), menu=self.fileMenu)
        self.fileMenu.add_command(label=_('Open...'), accelerator=KEY_OPEN_PROJECT[1], command=self._event('<<open_project>>'))
        self.fileMenu.add_command(label=_('Reload'), accelerator=KEY_RELOAD_PROJECT[1], command=self._event('<<reload_project>>'))
        self.fileMenu.add_command(label=_('Close'), command=self._event('<<close_project>>'))
        if PLATFORM == 'win':
            label = _('Exit')
        else:
            label = _('Quit')
        self.fileMenu.add_command(label=label, accelerator=KEYS.QUIT_PROGRAM[1], command=self._event('<<close_view>>'))

        # "Go to" menu.
        self.goMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=_('Go to'), menu=self.goMenu)
        self.goMenu.add_command(label=_('First event'), command=self._event('<<go_to_first>>'))
        self.goMenu.add_command(label=_('Last event'), command=self._event('<<go_to_last>>'))

        # "Scale" menu.
        self.scaleMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=_('Scale'), menu=self.scaleMenu)
        self.scaleMenu.add_command(label=_('Hours'), command=self._event('<<set_hour_scale>>'))
        self.scaleMenu.add_command(label=_('Days'), command=self._event('<<set_day_scale>>'))
        self.scaleMenu.add_command(label=_('Years'), command=self._event('<<set_year_scale>>'))
        self.scaleMenu.add_command(label=_('Fit to window'), command=self._event('<<fit_window>>'))

        # "Cascading" menu.
        self.cascadeMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=_('Cascading'), menu=self.cascadeMenu)
        self.cascadeMenu.add_command(label=_('Tight'), command=self._event('<<set_casc_tight>>'))
        self.cascadeMenu.add_command(label=_('Relaxed'), command=self._event('<<set_casc_relaxed>>'))
        self.cascadeMenu.add_command(label=_('Standard'), command=self._event('<<reset_casc>>'))

        # "Tools" menu.
        self.toolsMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=_('Tools'), menu=self.toolsMenu)

        # "Options" menu.
        self.optionsMenu = tk.Menu(self, tearoff=0)
        self.toolsMenu.add_cascade(label=_('Options'), menu=self.optionsMenu)

        self._substituteMissingTime = tk.BooleanVar(value=prefs['substitute_missing_time'])
        self.optionsMenu.add_checkbutton(
            label=_('Use 00:00 for missing times'),
            variable=self._substituteMissingTime,
            command=self._change_substitution_mode,
            )
        self._largeIcons = tk.BooleanVar(value=prefs['large_icons'])
        self.optionsMenu.add_checkbutton(
            label=_('Large toolbar icons'),
            variable=self._largeIcons,
            command=self._change_icon_size,
            )

        # "Help" menu.
        self.helpMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=_('Help'), menu=self.helpMenu)
        self.helpMenu.add_command(label=_('Online help'), command=self._event('<<open_help>>'))
        self.helpMenu.add_command(label=_('About yw Timeline viewer'), command=self._event('<<about>>'))
        self.helpMenu.add_command(label=f"yw Timeline viewer {_('Home page')}", command=self._event('<<open_homepage>>'))

        self._fileMenuNormalOpen = [
            _('Close'),
            _('Reload'),
        ]
        self._mainMenuNormalOpen = [
            _('Go to'),
            _('Scale'),
            _('Cascading'),
        ]
        self.disable_menu()

    def _event(self, sequence):

        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)

        return callback

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        for entry in self._fileMenuNormalOpen:
            self.fileMenu.entryconfig(entry, state='disabled')
        for entry in self._mainMenuNormalOpen:
            self.entryconfig(entry, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        for entry in self._fileMenuNormalOpen:
            self.fileMenu.entryconfig(entry, state='normal')
        for entry in self._mainMenuNormalOpen:
            self.entryconfig(entry, state='normal')

    def _change_icon_size(self):
        prefs['large_icons'] = self._largeIcons.get()
        messagebox.showinfo(
            message=_('Icon size changed'),
            detail=f"{_('The change takes effect after next startup')}.",
            title=_('Options'),
            )

    def _change_substitution_mode(self):
        prefs['substitute_missing_time'] = self._substituteMissingTime.get()
        root = self.master.winfo_toplevel()
        root.event_generate('<<refresh_view>>')
