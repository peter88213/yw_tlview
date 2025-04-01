"""Build the yw_tlview release package.

Note: VERSION must be updated manually before starting this script.
        
For further information see https://github.com/peter88213/yw_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys

sys.path.insert(0, f'{os.getcwd()}/../../yw_tlview/tools')
from package_builder import PackageBuilder
import inliner

VERSION = '0.2.0'

TEMP_FILE = '../test/temp.py'


class ApplicationBuilder(PackageBuilder):

    PRJ_NAME = 'yw_timeline_viewer'
    GERMAN_TRANSLATION = True

    def __init__(self, version):
        super().__init__(version)
        self.sourceFile = f'{self.sourceDir}{self.PRJ_NAME}_.py'
        self.moFile = 'nv_tlview.mo'

    def add_extras(self):
        self.add_icons()

    def build_script(self):
        os.makedirs(self.testDir, exist_ok=True)
        self.inline_modules(self.sourceFile, self.testFile)
        self.insert_version_number(self.testFile, version=self.version)

    def inline_modules(self, source, target):
        """Inline all non-standard library modules."""
        inliner.run(
            source,
            TEMP_FILE,
            'tlviewer',
            '../../yw_tlview/src/'
            )
        inliner.run(
            TEMP_FILE,
            TEMP_FILE,
            'tlv_model',
            '../../yw_tlview/src/'
            )
        inliner.run(
            TEMP_FILE,
            target,
            'nvtlview',
            '../../yw_tlview/src/'
            )
        os.remove(TEMP_FILE)


def main():
    ab = ApplicationBuilder(VERSION)
    ab.run()


if __name__ == '__main__':
    main()
