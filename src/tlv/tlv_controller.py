"""Provide a controller class for nv_tlview.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from datetime import datetime

from tlv.tlv_helper import from_timestamp
from tlv.tlv_helper import get_duration
from tlv.tlv_helper import get_seconds
from tlv.tlv_helper import get_specific_date
from tlv.tlv_helper import get_timestamp
from tlv.tlv_helper import get_unspecific_date
from tlv.tlv_main_frame import TlvMainFrame
from tlv.tlv_public_api import TlvPublicApi
from tlv.tlv_section_canvas import TlvSectionCanvas


class TlvController(TlvPublicApi):

    def __init__(self, model, window, settings, onDoubleClick=None):
        """Initialize the timeline viewer.
        
        Positional arguments: 
            model - Reference to the data model.
            window - Parent window for the view.
            settings - Dictionary with optional settings. 
            
        Optional arguments:
            onDoubleClick - Callback for double-clicking a section.
        
        Optional members in the "settings" dictionary:
            substitute_missing_time: Boolean  
                - If True, use "00:00" for sections without time.
                - If False, do not display sections without time. 
            localize_date: Boolean 
                - If True, display dates in localized format.
                - If False, display dates in ISO-format.
        """
        self._dataModel = model
        self.settings = settings

        # Create the view component.
        self.view = TlvMainFrame(
            self._dataModel,
            window,
            self,
            settings,
        )
        self.isOpen = True
        self.firstTimestamp = None
        self.lastTimestamp = None

        self.controlBuffer = []
        # stack for operations that can be undone

        self.on_double_click = onDoubleClick
        # hook for double-clicking a section marker
        self.view.get_canvas().bind('<<double-click>>', self._on_double_click)

    def datestr(self, dt):
        """Return a localized date string, if the localize_date option is set.
        
        Otherwise return the ISO date string.
        """
        if self.settings.get('localize_date', True):
            return dt.strftime("%x")
        else:
            return dt.isoformat().split('T')[0]

    def get_minutes(self, pixels):
        return pixels * self.view.scale // 60

    def get_section_timestamp(self, scId):
        section = self._dataModel.sections[scId]
        if section.scType != 0:
            return

        try:
            refIso = self._dataModel.referenceDate
            if section.time is None:
                if not self.settings.get('substitute_missing_time', False):
                    return

                scTime = '00:00'
            else:
                scTime = section.time

            if section.date is not None:
                scDate = section.date
            elif section.day is not None:
                if refIso is None:
                    refIso = '0001-01-01'
                scDate = get_specific_date(section.day, refIso)
            else:
                return

            return get_timestamp(datetime.fromisoformat(f'{scDate} {scTime}'))

        except:
            return

    def get_section_id(self, event):
        """Return the ID of the section assigned to event.
        
        This can be used for <<double-click>> callbacks.
        """
        return self.view.get_canvas().get_section_id(event)

    def get_section_title(self, scId):
        return self._dataModel.sections[scId].title

    def on_quit(self):
        """Actions to be performed when the viewer is closed."""
        if not self.isOpen:
            return

        self.view.on_quit()
        self.isOpen = False

    def shift_section(self, scId, pixels):
        self.push_section(scId)

        deltaSeconds = int(pixels * self.view.scale)
        section = self._dataModel.sections[scId]
        refIso = self._dataModel.referenceDate
        if section.time is None:
            scTime = '00:00'
        else:
            scTime = section.time
        if section.date is not None:
            scDate = section.date
        elif section.day is not None:
            scDate = get_specific_date(section.day, refIso)
        else:
            scDate = refIso

        timestamp = get_timestamp(
            datetime.fromisoformat(f'{scDate} {scTime}')
        ) + deltaSeconds
        dt = from_timestamp(timestamp)
        dateStr, timeStr = datetime.isoformat(dt).split('T')
        section.time = timeStr
        if section.date is not None:
            section.date = dateStr
        else:
            dayStr = get_unspecific_date(dateStr, refIso)
            section.day = dayStr

    def shift_section_end(self, scId, pixels):
        self.push_section(scId)

        deltaSeconds = int(pixels * self.view.scale)
        section = self._dataModel.sections[scId]
        seconds = get_seconds(
            section.lastsDays,
            section.lastsHours,
            section.lastsMinutes
        )
        seconds += deltaSeconds
        if seconds < 0:
            seconds = 0

        days, hours, minutes = get_duration(seconds)
        if days:
            section.lastsDays = str(days)
        else:
            section.lastsDays = None
        if hours:
            section.lastsHours = str(hours)
        else:
            section.lastsHours = None
        if minutes:
            section.lastsMinutes = str(minutes)
        else:
            section.lastsMinutes = None

    def push_section(self, scId):
        section = self._dataModel.sections[scId]
        scnData = (
            scId,
            section.date,
            section.time,
            section.day,
            section.lastsDays,
            section.lastsHours,
            section.lastsMinutes
        )
        self.controlBuffer.append(scnData)
        root = self.view.winfo_toplevel()
        root.event_generate('<<enable_undo>>')

    def pop_section(self, event=None):
        if not self.controlBuffer:
            return

        if TlvSectionCanvas.isLocked:
            return

        scnData = self.controlBuffer.pop()
        (
            scId,
            sectionDate,
            sectionTime,
            sectionDay,
            sectionLastsDays,
            sectionLastsHours,
            sectionLastsMinutes
        ) = scnData
        section = self._dataModel.sections[scId]
        section.date = sectionDate
        section.time = sectionTime
        section.day = sectionDay
        section.lastsDays = sectionLastsDays
        section.lastsHours = sectionLastsHours
        section.lastsMinutes = sectionLastsMinutes
        if not self.controlBuffer:
            root = self.view.winfo_toplevel()
            root.event_generate('<<disable_undo>>')

    def _on_double_click(self, event):
        scId = self.get_section_id(event)
        if self.on_double_click is not None:
            self.on_double_click(scId)

