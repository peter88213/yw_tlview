"""Provide a mixin class for the timeline viewer commands.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/yw_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from tkinter import filedialog
from tkinter import messagebox
import webbrowser

from nvtlview.platform.platform_settings import KEYS
from nvtlview.tlv_locale import _
from tlviewer.doc_open import open_document
from tlviewer.tlviewer_globals import HELP_URL
from tlviewer.tlviewer_globals import HOME_URL


class TlviewerCommands:

    def about(self, event=None):
        """Display a legal notice window.
        
        Important: after building the program, __doc__ will be the yw_timeline_viewer docstring.
        """
        messagebox.showinfo(
            message='yw Timeline viewer',
            detail=__doc__,
            title=_('About yw Timeline viewer'),
            )

    def bind_events(self):
        # Bind the commands to the controller.
        event_callbacks = {
            '<<about>>': self.about,
            '<<close_project>>': self.close_project,
            '<<close_view>>': self.on_quit,
            '<<create_project>>':self.create_project,
            '<<disable_undo>>': self.disable_undo_button,
            '<<enable_undo>>': self.enable_undo_button,
            '<<fit_window>>': self.tlv.fit_window,
            '<<go_to_first>>': self.tlv.go_to_first,
            '<<go_to_last>>': self.tlv.go_to_last,
            '<<increase_scale>>': self.tlv.increase_scale,
            '<<open_help>>': self.open_help,
            '<<open_homepage>>': self.open_homepage,
            '<<open_project>>': self.open_project,
            '<<open_project_file>>': self.open_project_file,
            '<<page_back>>': self.tlv.page_back,
            '<<page_forward>>': self.tlv.page_forward,
            '<<reduce_scale>>': self.tlv.reduce_scale,
            '<<refresh_view>>': self.tlv.refresh,
            '<<reload_project>>': self.reload_project,
            '<<reset_casc>>': self.tlv.reset_casc,
            '<<save_as>>': self.save_as,
            '<<save_project>>': self.save_project,
            '<<scroll_back>>': self.tlv.scroll_back,
            '<<scroll_forward>>': self.tlv.scroll_forward,
            '<<set_casc_relaxed>>': self.tlv.set_casc_relaxed,
            '<<set_casc_tight>>': self.tlv.set_casc_tight,
            '<<set_day_scale>>': self.tlv.set_day_scale,
            '<<set_hour_scale>>': self.tlv.set_hour_scale,
            '<<set_year_scale>>': self.tlv.set_year_scale,
            '<<undo>>': self.tlv.undo,
            KEYS.OPEN_PROJECT[0]: self.open_project,
            KEYS.RELOAD_PROJECT[0]: self.reload_project,
            KEYS.SAVE_AS[0]: self.save_as,
            KEYS.SAVE_PROJECT[0]: self.save_project,
        }
        for sequence, callback in event_callbacks.items():
            self.root.bind(sequence, callback)
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)

    def close_project(self, event=None):
        """Close the project without saving and reset the user interface.
        
        To be extended by subclasses.
        """
        if self.mdl.isModified:
            answer = messagebox.askyesnocancel(
                title=_('Close'),
                message=_('Save changes?'),
                )
            if answer is None:
                return

            elif answer:
                self.save_project_file(self.prjFilePath)
        self.mdl.clear()
        self.prjFilePath = None
        self.show_path()
        self.disable_menu()

    def create_project(self, event=None):
        if self.mdl.isModified:
            answer = messagebox.askyesnocancel(
            title=_('New'),
            message=_('Save changes?'),
            )
            if answer is None:
                return

            elif answer:
                self.save_project_file(self.prjFilePath)
        if self.prjFilePath:
            initDir = os.path.dirname(self.prjFilePath)
        else:
            initDir = './'

        filePath = filedialog.asksaveasfilename(
            filetypes=self.filetypes,
            defaultextension=self.defaultFileClass.EXTENSION,
            initialdir=initDir
            )
        if not filePath:
            return

        self.mdl.clear()
        self.prjFilePath = filePath
        self.show_path()
        self.save_project()
        if messagebox.askyesno(
            title=_('Project created'),
            message=_('Open the file for data entry?'),
            ):
            self.open_project_file()

    def disable_undo_button(self, event=None):
        self._toolbar.undoButton.config(state='disabled')

    def enable_undo_button(self, event=None):
        self._toolbar.undoButton.config(state='normal')

    def open_help(self, event=None):
        webbrowser.open(HELP_URL)

    def open_homepage(self, event=None):
        webbrowser.open(HOME_URL)

    def open_project(self, event=None):
        if self.mdl.isModified:
            answer = messagebox.askyesnocancel(
            title=_('Open'),
            message=_('Save changes?'),
            )
            if answer is None:
                return

            elif answer:
                self.save_project_file(self.prjFilePath)
        if self.prjFilePath:
            initDir = os.path.dirname(self.prjFilePath)
        else:
            initDir = './'

        filePath = filedialog.askopenfilename(
            filetypes=self.filetypes,
            defaultextension=self.defaultFileClass.EXTENSION,
            initialdir=initDir
            )
        if filePath:
            self.read_data(filePath)

    def open_project_file(self, event=None):
        if self.mdl.isModified:
            answer = messagebox.askyesnocancel(
            title=_('Open project file'),
            message=_('Save changes?'),
            )
            if answer is None:
                return

            elif answer:
                self.save_project_file(self.prjFilePath)
        if self.prjFilePath:
            open_document(self.prjFilePath)

    def open_section(self, scId):
        print(scId)

    def reload_project(self, event=None):
        if self.prjFilePath is not None:
            self.read_data(self.prjFilePath)

    def save_as(self, event=None):
        if self.prjFilePath is None:
            return

        if self.prjFilePath:
            initDir = os.path.dirname(self.prjFilePath)
        else:
            initDir = './'

        filePath = filedialog.asksaveasfilename(
            filetypes=self.filetypes,
            defaultextension=self.defaultFileClass.EXTENSION,
            initialdir=initDir
            )
        if filePath:
            self.prjFilePath = filePath
            self.save_project()
            self.refresh()

    def save_project(self, event=None):
        if self.prjFilePath:
            try:
                self.mdl.write_data(self.prjFilePath)
            except Exception as ex:
                messagebox.showerror(
                    self.root.title(),
                    message=_('Cannot write file'),
                    detail=str(ex),
                    )

