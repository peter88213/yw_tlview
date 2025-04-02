"""Provide an abstract base class for data file representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/timeline-view-tk
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC
from abc import abstractmethod


class TlvFile(ABC):

    EXTENSION = None

    def __init__(self, model, filePath=None):
        self._mdl = model
        self.filePath = filePath

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass

