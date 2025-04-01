"""A timeline viewer application using tkinter.

Version @release
Requires Python 3.6+
Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/yw_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify \
it under the terms of the GNU General Public License as published by \
the Free Software Foundation, either version 3 of the License, or \
(at your option) any later version.

This program is distributed in the hope that it will be useful, \
but WITHOUT ANY WARRANTY; without even the implied warranty of \
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the \
GNU General Public License for more details.
"""
import locale
import os
import sys
from tkinter import messagebox
from tkinter import ttk

from nvtlview.tlv_controller import TlvController
from nvtlview.tlv_locale import _
import tkinter as tk
from tlv_model.yw7_file import Yw7File
from tlv_model.tlv_data_model import TlvDataModel
from tlviewer.configuration import Configuration
from tlviewer.set_icon_tk import set_icon
from tlviewer.tlviewer_commands import TlviewerCommands
from tlviewer.tlviewer_globals import INSTALL_DIR
from tlviewer.tlviewer_globals import prefs
from tlviewer.tlviewer_menu import TlviewerMenu
from tlviewer.tlviewer_path_bar import TlviewerPathBar
from tlviewer.tlviewer_toolbar import TlviewerToolbar

SETTINGS = dict(
    last_open='',
    window_geometry='1200x800',
)
OPTIONS = dict(
    enable_hovertips=True,
    substitute_missing_time=False,
    large_icons=False,
    localize_date=True,
    )


class TimelineViewer(TlviewerCommands):

    def __init__(self):

        #--- Set up the data model.
        self.defaultFileClass = Yw7File
        self.mdl = TlvDataModel(self.defaultFileClass)
        self.filetypes = [
            (self.defaultFileClass.DESCRIPTION, self.defaultFileClass.EXTENSION),
        ]
        self.prjFilePath = None

        #--- Set up the GUI.
        if prefs['localize_date']:
            locale.setlocale(locale.LC_TIME, "")
            # enabling localized time display

        self.root = tk.Tk()
        self.root.title('Timeline viewer')
        self.root.geometry(prefs['window_geometry'])
        set_icon(self.root, icon='tlv')

        self._mainMenu = TlviewerMenu(self.root)
        self.root.config(menu=self._mainMenu)

        mainWindow = ttk.Frame(self.root)
        mainWindow.pack(fill='both', expand=True)
        self._pathBar = TlviewerPathBar(mainWindow, self.mdl, text='', anchor='w', padx=5, pady=3)
        self._pathBar.pack(side='bottom', expand=False, fill='x')
        self.mdl.add_observer(self._pathBar)
        self._toolbar = TlviewerToolbar(mainWindow)
        self._toolbar.pack(side='bottom', fill='x', padx=5, pady=2)

        #--- Set up the timeline view widget.
        self.tlv = TlvController(
            self.mdl,
            mainWindow,
            prefs,
            onDoubleClick=self.open_section,
            )
        self.mdl.add_observer(self.tlv)

        #--- Connect the controls.
        self.bind_events()

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        To be extended by subclasses.
        """
        self._mainMenu.disable_menu()
        self._toolbar.disable_menu()

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        To be extended by subclasses.
        """
        self._mainMenu.enable_menu()
        self._toolbar.enable_menu()

    def on_quit(self, event=None):
        try:
            if self.mdl.isModified:
                answer = messagebox.askyesnocancel(
                    title=_('Quit'),
                    message=_('Save changes?'),
                    )
                if answer is None:
                    return

                elif answer:
                    self.save_project_file(self.prjFilePath)
            prefs['window_geometry'] = self.root.winfo_geometry()
            self.tlv.on_quit()
        except Exception as ex:
            messagebox.showerror(
                message=_('Unhandled exception on exit'),
                detail=str(ex),
                title=_('Error'),
                )
        finally:
            self.root.quit()

    def read_data(self, filePath):
        self.mdl.clear()
        try:
            self.mdl.read_data(filePath)
        except Exception as ex:
            self.mdl.clear()
            self.prjFilePath = None
            self.disable_menu()
            messagebox.showerror(
                self.root.title(),
                message=_('Cannot read file'),
                detail=str(ex),
                )
        else:
            self.prjFilePath = filePath
        finally:
            self.refresh()
        prefs['last_open'] = filePath

    def refresh(self, event=None):
        self.tlv.refresh()
        self.tlv.fit_window()
        self.enable_menu()
        self.show_path()

    def show_path(self):
        """Put text on the path bar."""
        if self.prjFilePath is None:
            filePath = ''
        else:
            filePath = os.path.normpath(self.prjFilePath)
        self._pathBar.config(text=filePath)

    def start(self):
        self.root.mainloop()


def main():
    #--- Set up the directories for configuration and temporary files.
    os.makedirs(INSTALL_DIR, exist_ok=True)
    configDir = f'{INSTALL_DIR}/config'
    os.makedirs(configDir, exist_ok=True)

    #--- Load configuration.
    iniFile = f'{configDir}/tlviewer.ini'
    configuration = Configuration(SETTINGS, OPTIONS)
    try:
        configuration.read(iniFile)
    except:
        pass
        # skipping the configuraton if faulty
    prefs.update(configuration.settings)
    prefs.update(configuration.options)

    #--- Instantiate the app object.
    app = TimelineViewer()

    #--- Load a project, if specified.
    try:
        filePath = sys.argv[1]
    except IndexError:
        filePath = ''
    if not filePath or not os.path.isfile(filePath):
        filePath = prefs['last_open']
    if filePath and os.path.isfile(filePath):
        app.read_data(filePath)

    #--- Run the GUI application.

    app.start()

    #--- Save project specific configuration
    for keyword in prefs:
        if keyword in configuration.options:
            configuration.options[keyword] = prefs[keyword]
        elif keyword in configuration.settings:
            configuration.settings[keyword] = prefs[keyword]
    configuration.write(iniFile)


if __name__ == '__main__':
    main()

