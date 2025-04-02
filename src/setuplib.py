"""timeline_viewer installer library module. 

Version @release

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yw_tlview
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from shutil import copytree
from shutil import copy2
import platform
import zipfile
import os
import sys
import stat
from shutil import rmtree
from pathlib import Path
from string import Template
try:
    from tkinter import *
except ModuleNotFoundError:
    print('The tkinter module is missing. Please install the tk support package for your python3 version.')
    sys.exit(1)

APPNAME = 'yw_timeline_viewer'
VERSION = ' @release'
INSTALL_DIR = '.yw_tlview'
START_UP_SCRIPT = 'run.pyw'
APP = f'{APPNAME}.py'
INI_FILE = f'{APPNAME}.ini'
INI_PATH = '/config/'
SAMPLE_PATH = 'sample/'
SUCCESS_MESSAGE = '''

$Appname is installed here:

$DisplayDir'''

SHORTCUT_MESSAGE = '''
Now you might want to create a shortcut on your desktop.  

On Windows, open the installation folder, hold down the Alt key on your keyboard, 
and then drag and drop "run.pyw" to your desktop.

On Linux, create a launcher on your desktop. With xfce for instance, the launcher's command may look like this:
python3 /home/peter/.yw_tlview/run.pyw %F
'''

START_UP_CODE = f'''import logging
from tkinter import messagebox
import traceback

import $Appname
import tkinter as tk

def show_error(self, *args):
    err = traceback.format_exception(*args)
    logger.error('$Appname $Release\\n' + ''.join(err))
    messagebox.showerror('An unexpected error has occurred.', 'See "error.log" in the installation directory.' )

logger = logging.getLogger(__name__)
logging.basicConfig(filename='$InstallDir/error.log', level=logging.ERROR)
tk.Tk.report_callback_exception = show_error
$Appname.main()
'''

root = Tk()
processInfo = Label(root, text='')
message = []

pyz = os.path.dirname(__file__)


def extract_file(sourceFile, targetDir):
    with zipfile.ZipFile(pyz) as z:
        z.extract(sourceFile, targetDir)


def extract_tree(sourceDir, targetDir):
    with zipfile.ZipFile(pyz) as z:
        for file in z.namelist():
            if file.startswith(f'{sourceDir}/'):
                z.extract(file, targetDir)


def cp_tree(sourceDir, targetDir):
    copytree(sourceDir, f'{targetDir}/{sourceDir}', dirs_exist_ok=True)


def output(text):
    message.append(text)
    processInfo.config(text=('\n').join(message))


def open_folder(installDir):
    """Open an installation folder window in the file manager.
    """
    try:
        os.startfile(os.path.normpath(installDir))
        # Windows
    except:
        try:
            os.system('xdg-open "%s"' % os.path.normpath(installDir))
            # Linux
        except:
            try:
                os.system('open "%s"' % os.path.normpath(installDir))
                # Mac
            except:
                pass


def install(novxPath, zipped):
    """Install the script."""
    if zipped:
        copy_file = extract_file
        copy_tree = extract_tree
    else:
        copy_file = copy2
        copy_tree = cp_tree

    # Create a general installation directory, if necessary.
    os.makedirs(novxPath, exist_ok=True)
    installDir = f'{novxPath}'
    cnfDir = f'{installDir}{INI_PATH}'
    if os.path.isfile(f'{installDir}/{APP}'):
        simpleUpdate = True
    else:
        simpleUpdate = False
    os.makedirs(cnfDir, exist_ok=True)

    # Delete the old version, but retain configuration, if any.
    rmtree(f'{installDir}/icons', ignore_errors=True)
    rmtree(f'{installDir}/sample', ignore_errors=True)
    with os.scandir(installDir) as files:
        for file in files:
            if 'config' in file.name:
                continue

            try:
                os.remove(file)
                output(f'"{file}" removed.')
            except:
                pass

    # Install the new version.
    output(f'Copying "{APP}" ...')
    copy_file(APP, installDir)

    # Install the localization files.
    # output('Copying locale ...')
    # copy_tree('locale', installDir)

    # Install the icon files.
    output('Copying icons ...')
    copy_tree('icons', installDir)

    #--- Create a start-up script.
    output('Creating starter script ...')
    mapping = {
        'Appname': APPNAME,
        'Apppath': f'{installDir}/{START_UP_SCRIPT}',
        'InstallDir': installDir,
        'Release': VERSION,
        'DisplayDir': os.path.normpath(f'{installDir}'),
    }
    if platform.system() == 'Windows':
        shebang = ''
    else:
        shebang = '#!/usr/bin/env python3\n'
    with open(f'{installDir}/{START_UP_SCRIPT}', 'w', encoding='utf-8') as f:
        startupCode = Template(f'{shebang}{START_UP_CODE}').safe_substitute(mapping)
        f.write(startupCode)

    #--- Make the scripts executable under Linux.
    st = os.stat(f'{installDir}/{APP}')
    os.chmod(f'{installDir}/{APP}', st.st_mode | stat.S_IEXEC)
    st = os.stat(f'{installDir}/{START_UP_SCRIPT}')
    os.chmod(f'{installDir}/{START_UP_SCRIPT}', st.st_mode | stat.S_IEXEC)

    # Provide the sample files.
    output('Copying sample files ...')
    copy_tree('sample', installDir)

    # Display a success message.
    output(Template(SUCCESS_MESSAGE).safe_substitute(mapping))

    # Ask for shortcut creation.
    if not simpleUpdate:
        output(Template(SHORTCUT_MESSAGE).safe_substitute(mapping))


def main(zipped=True):
    scriptPath = os.path.abspath(sys.argv[0])
    scriptDir = os.path.dirname(scriptPath)
    os.chdir(scriptDir)

    # Open a tk window.
    root.title('Setup')
    output(f'*** Installing {APPNAME}{VERSION} ***\n')
    header = Label(root, text='')
    header.pack(padx=5, pady=5)

    # Prepare the messaging area.
    processInfo.pack(padx=5, pady=5)

    # Run the installation.
    homePath = str(Path.home()).replace('\\', '/')
    novxlibPath = f'{homePath}/{INSTALL_DIR}'
    try:
        install(novxlibPath, zipped)
    except Exception as ex:
        output(str(ex))

    # Show options: open installation folders or quit.
    root.openButton = Button(text="Open installation folder", command=lambda: open_folder(f'{homePath}/{INSTALL_DIR}'))
    root.openButton.config(height=1, width=30)
    root.openButton.pack(padx=5, pady=5)
    root.quitButton = Button(text="Quit", command=quit)
    root.quitButton.config(height=1, width=30)
    root.quitButton.pack(padx=5, pady=5)
    root.mainloop()
