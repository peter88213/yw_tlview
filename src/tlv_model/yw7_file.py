"""Provide a class for csv data file representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/yw_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import re

from tlv_model.id_generator import new_id
from tlv_model.tlv_constants import SC_PREFIX
from tlv_model.tlv_file import TlvFile
from tlv_model.tlv_section import TlvSection
import xml.etree.ElementTree as ET


class Yw7File(TlvFile):

    DESCRIPTION = 'yWriter 7 project'
    EXTENSION = '.yw7'

    def read(self):

        def strip_illegal_characters(text):
            return re.sub('[\x00-\x08|\x0b-\x0c|\x0e-\x1f]', '', text)

        try:
            try:
                with open(self.filePath, 'r', encoding='utf-8') as f:
                    xmlText = f.read()
            except:
                # yw7 file may be UTF-16 encoded, with a wrong XML header (yWriter for iOS)
                with open(self.filePath, 'r', encoding='utf-16') as f:
                    xmlText = f.read()
        except:
            self.tree = ET.parse(self.filePath)

        xmlText = strip_illegal_characters(xmlText)
        root = ET.fromstring(xmlText)
        del xmlText
        # saving memory

        self._mdl.sections = {}

        for xmlScene in root.find('SCENES'):
            scId = new_id(self._mdl.sections, SC_PREFIX)
            self._mdl.sections[scId] = TlvSection()

            if xmlScene.find('Title') is not None:
                self._mdl.sections[scId].title = xmlScene.find('Title').text

            if xmlScene.find('Desc') is not None:
                self._mdl.sections[scId].desc = xmlScene.find('Desc').text

            #--- Scene start.
            if xmlScene.find('SpecificDateTime') is not None:
                dateTimeStr = xmlScene.find('SpecificDateTime').text
                dateTime = datetime.fromisoformat(dateTimeStr)
                startDateTime = dateTime.isoformat().split('T')
                self._mdl.sections[scId].date = startDateTime[0]
                self._mdl.sections[scId].time = startDateTime[1]

            else:
                if xmlScene.find('Day') is not None:
                    day = xmlScene.find('Day').text

                    # Check if Day represents an integer.
                    try:
                        int(day)
                    except ValueError:
                        day = ''
                    self._mdl.sections[scId].day = day

                hasUnspecificTime = False
                if xmlScene.find('Hour') is not None:
                    hour = xmlScene.find('Hour').text.zfill(2)
                    hasUnspecificTime = True
                else:
                    hour = '00'
                if xmlScene.find('Minute') is not None:
                    minute = xmlScene.find('Minute').text.zfill(2)
                    hasUnspecificTime = True
                else:
                    minute = '00'
                if hasUnspecificTime:
                    self._mdl.sections[scId].time = f'{hour}:{minute}:00'

            #--- Scene duration.
            if xmlScene.find('LastsDays') is not None:
                self._mdl.sections[scId].lastsDays = xmlScene.find('LastsDays').text

            if xmlScene.find('LastsHours') is not None:
                self._mdl.sections[scId].lastsHours = xmlScene.find('LastsHours').text

            if xmlScene.find('LastsMinutes') is not None:
                self._mdl.sections[scId].lastsMinutes = xmlScene.find('LastsMinutes').text

            self._mdl.sections[scId].on_element_change = self._mdl.on_element_change

    def write(self):
        pass
