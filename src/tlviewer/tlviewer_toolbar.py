"""Provide a toolbar class for the timeline viewer.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/yw_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

import tkinter as tk
from tlv.tlv_locale import _
from tlviewer.tlviewer_globals import INSTALL_DIR
from tlviewer.tlviewer_globals import settings
from tlviewer.tooltip import Hovertip


class TlviewerToolbar(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # Prepare the toolbar icons.
        if settings['large_icons']:
            size = 24
        else:
            size = 16
        iconPath = f'{INSTALL_DIR}/icons/{size}'
        self._toolbarIcons = {}
        icons = [
            'rewindLeft',
            'arrowLeft',
            'goToFirst',
            'goToLast',
            'arrowRight',
            'rewindRight',
            'fitToWindow',
            'arrowUp',
            'arrowDown',
            'undo',
            ]
        for icon in icons:
            try:
                self._toolbarIcons[icon] = tk.PhotoImage(file=f'{iconPath}/{icon}.png')
            except:
                self._toolbarIcons[icon] = None

        self.buttons = list()

        # Moving the x position.
        rewindLeftButton = ttk.Button(
            self,
            text=_('Page back'),
            image=self._toolbarIcons['rewindLeft'],
            command=self._event('<<page_back>>')
            )
        rewindLeftButton.pack(side='left')
        rewindLeftButton.image = self._toolbarIcons['rewindLeft']
        self.buttons.append(rewindLeftButton)

        arrowLeftButton = ttk.Button(
            self,
            text=_('Scroll back'),
            image=self._toolbarIcons['arrowLeft'],
            command=self._event('<<scroll_back>>')
            )
        arrowLeftButton.pack(side='left')
        arrowLeftButton.image = self._toolbarIcons['arrowLeft']
        self.buttons.append(arrowLeftButton)

        goToFirstButton = ttk.Button(
            self,
            text=_('First scene'),
            image=self._toolbarIcons['goToFirst'],
            command=self._event('<<go_to_first>>')
            )
        goToFirstButton.pack(side='left')
        goToFirstButton.image = self._toolbarIcons['goToFirst']
        self.buttons.append(goToFirstButton)

        goToLastButton = ttk.Button(
            self,
            text=_('Last scene'),
            image=self._toolbarIcons['goToLast'],
            command=self._event('<<go_to_last>>')
            )
        goToLastButton.pack(side='left')
        goToLastButton.image = self._toolbarIcons['goToLast']
        self.buttons.append(goToLastButton)

        arrowRightButton = ttk.Button(
            self,
            text=_('Scroll forward'),
            image=self._toolbarIcons['arrowRight'],
            command=self._event('<<scroll_forward>>')
            )
        arrowRightButton.pack(side='left')
        arrowRightButton.image = self._toolbarIcons['arrowRight']
        self.buttons.append(arrowRightButton)

        rewindRightButton = ttk.Button(
            self,
            text=_('Page forward'),
            image=self._toolbarIcons['rewindRight'],
            command=self._event('<<page_forward>>')
            )
        rewindRightButton.pack(side='left')
        rewindRightButton.image = self._toolbarIcons['rewindRight']
        self.buttons.append(rewindRightButton)

        # Separator.
        tk.Frame(self, bg='light gray', width=1).pack(side='left', fill='y', padx=6)

        # Changing the scale.
        arrowDownButton = ttk.Button(
            self,
            text=_('Reduce scale'),
            image=self._toolbarIcons['arrowDown'],
            command=self._event('<<reduce_scale>>')
            )
        arrowDownButton.pack(side='left')
        arrowDownButton.image = self._toolbarIcons['arrowDown']
        self.buttons.append(arrowDownButton)

        fitToWindowButton = ttk.Button(
            self,
            text=_('Fit to window'),
            image=self._toolbarIcons['fitToWindow'],
            command=self._event('<<fit_window>>')
            )
        fitToWindowButton.pack(side='left')
        fitToWindowButton.image = self._toolbarIcons['fitToWindow']
        self.buttons.append(fitToWindowButton)

        arrowUpButton = ttk.Button(
            self,
            text=_('Increase scale'),
            image=self._toolbarIcons['arrowUp'],
            command=self._event('<<increase_scale>>')
            )
        arrowUpButton.pack(side='left')
        arrowUpButton.image = self._toolbarIcons['arrowUp']
        self.buttons.append(arrowUpButton)

        # Separator.
        # tk.Frame(self, bg='light gray', width=1).pack(side='left', fill='y', padx=6)

        self.undoButton = ttk.Button(
            self,
            text=_('Undo'),
            image=self._toolbarIcons['undo'],
            command=self._event('<<undo>>'),
            state='disabled',
            )
        # self.undoButton.pack(side='left')
        self.undoButton.image = self._toolbarIcons['undo']

        # Initialize tooltips.
        if not settings['enable_hovertips']:
            return

        Hovertip(rewindLeftButton, rewindLeftButton['text'])
        Hovertip(arrowLeftButton, arrowLeftButton['text'])
        Hovertip(goToFirstButton, goToFirstButton['text'])
        Hovertip(goToLastButton, goToLastButton['text'])
        Hovertip(arrowRightButton, arrowRightButton['text'])
        Hovertip(rewindRightButton, rewindRightButton['text'])
        Hovertip(arrowDownButton, arrowDownButton['text'])
        Hovertip(fitToWindowButton, fitToWindowButton['text'])
        Hovertip(arrowUpButton, arrowUpButton['text'])
        Hovertip(self.undoButton, self.undoButton['text'])

    def _event(self, sequence):

        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)

        return callback

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        for button in self.buttons:
            button.config(state='disabled')
        self.undoButton.config(state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        for button in self.buttons:
            button.config(state='normal')
