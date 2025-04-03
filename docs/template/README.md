[![Download the latest release](docs/img/download-button.png)](https://github.com/peter88213/yw_tlview/raw/main/dist/yw_timeline_viewer_v0.99.0.pyzw)
[![Changelog](docs/img/changelog-button.png)](docs/changelog.md)
[![Feedback](docs/img/feedback-button.png)](https://github.com/peter88213/yw_tlview/discussions)
[![Online help](docs/img/help-button.png)](https://peter88213.github.io/yw_tlview/help/)


# ![](docs/img/tlv32.png) yw_tlview

A timeline viewer for [yWriter](https://spacejock.com/yWriter7.html) projects.

![Screenshot](docs/Screenshots/screen01.png)


## Features

- The application reads the scenes from a *.yw7* file and displays them on a resizable 
  window.
- Scenes with a specific date or with an unspecific day are displayed.
- Scenes without a time can optionally be displayed using 00:00 as a default.
- You can increase and reduce the time scale. 
- You can scroll forward and back in time.
- The application is ready for internationalization with GNU gettext. 

This application is a variant of the [timeline-view-tk](https://github.com/peter88213/timeline-view-tk/)
application that reads and writes csv files.



## Requirements

- Windows or Linux. Mac OS support is experimental.
- [Python](https://www.python.org/) version 3.6+. 

---

[Changelog](docs/changelog.md)

[Feedback](https://github.com/peter88213/yw_tlview/discussions)

---

## Download and install

### Default: Executable Python zip archive

Download the latest release [yw_timeline_viewer_v0.99.0.pyzw](https://github.com/peter88213/yw_tlview/raw/main/dist/yw_timeline_viewer_v0.99.0.pyzw)

- Launch *yw_timeline_viewer_v0.99.0.pyzw* by double-clicking (Windows/Linux desktop),
- or execute `python yw_timeline_viewer_v0.99.0.pyzw` (Windows), resp. `python3 yw_timeline_viewer_v0.99.0.pyzw` (Linux) on the command line.

#### Important

Many web browsers recognize the download as an executable file and offer to open it immediately. 
This starts the installation.

However, depending on your security settings, your browser may 
initially  refuse  to download the executable file. 
In this case, your confirmation or an additional action is required. 
If this is not possible, you have the option of downloading 
the zip file. 


### Alternative: Zip file

The package is also available in zip format: [yw_timeline_viewer_v0.99.0.zip](https://github.com/peter88213/yw_tlview/raw/main/dist/yw_timeline_viewer_v0.99.0.zip)

- Extract the *yw_timeline_viewer_v0.99.0* folder from the downloaded zipfile "yw_timeline_viewer_v0.99.0.zip".
- Move into this new folder and launch *setup.pyw* by double-clicking (Windows/Linux desktop), 
- or execute `python setup.pyw` (Windows), resp. `python3 setup.pyw` (Linux) on the command line.


---

## Credits

- The logo and the toolbar icons are based on the [Eva Icons](https://akveo.github.io/eva-icons/#/), published under the [MIT License](http://www.opensource.org/licenses/mit-license.php). The original black and white icons were adapted for this application by the maintainer. 

---

## License

This is Open Source software, and *yw_tlview* is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/yw_tlview/blob/main/LICENSE) file.


