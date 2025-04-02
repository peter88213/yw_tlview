
# yWriter Timeline viewer

**User guide**

This page refers to the latest
[yw_tlview](https://github.com/peter88213/yw_tlview/) release. You can
open it with **Help \> Online help**.


## Operation


### Mouse scrolling

-   Scroll the timeline horizontally with `Shift`-`Mousewheel`.
-   Scroll the timeline vertically with the mousewheel.
-   Scroll the timeline in any direction by right-clicking on the canvas
    and dragging the mouse.
-   Increase or reduce the time scale with `Ctrl`-`Mousewheel`.
-   Change the distance limits for stacking with
    `Shift`-`Ctrl`-`Mousewheel`.


## Command reference

### \"Go to\" menu

First event

:   Shift the timeline so that the earliest event is positioned near the
    left edge of the window.

Last event

:   Shift the timeline so that the latest event is positioned near the
    right edge of the window.

    project tree is positioned in the center of the window.

### \"Scale\" menu

Hours

:   This sets the scale to one hour per line.

Days

:   This sets the scale to one day per line.

Years

:   This sets the scale to one year per line.

Fit to window

:   This sets the scale and moves the timeline, so that all sections
    with valid or substituted date/time information fit into the window.

### \"Cascading\" menu

The section marks are stacked on the timeline canvas, so that they would
not overlap or cover the title of previous sections. If the stacking
algorithm does not seem good enough to you, you can adjust its limits.

Tight

:   Arrange consecutive events behind each other, even if they are close
    together.

Relaxed

:   Arrange consecutive events in a stack, even if they are some
    distance apart.

Standard

:   Reset the cascading to default.

---

**Hint** 

- You can fine-tune the stacking limits with `Shift`-`Ctrl`-`Mousewheel`.

---

### \"Options\" menu

Use 00:00 for missing times

:   -   If ticked, \"00:00\" is used as display time for sections
        without time information. This does not affect the section
        properties.
    -   If unticked, sections without time information are not
        displayed.

### \"Help\" menu

Online help

:   Open this help page in a web browser.

### Buttons in the footer toolbar

![rewindLeft](images/rewindLeft.png) Go one page back

:   Shift the timeline to go about one screen width back in time. Same
    as the \"back\" mouse button (Windows).

![arrowLeft](images/arrowLeft.png) Scroll back

:   Shift the timeline to go 1/5 screen width back in time. You can move
    it more precisely with the mouse wheel.

![goToFirst](images/goToFirst.png) Go to the first event

:   Shift the timeline so that the earliest event is positioned near the
    left edge of the window.

![goToLast](images/goToLast.png) Go to the last event

:   Shift the timeline so that the latest event is positioned near the
    right edge of the window.

![arrowRight](images/arrowRight.png) Scroll forward

:   Shift the timeline to go 1/5 screen width forward in time. You can
    move it more precisely with the mouse wheel.

![rewindRight](images/rewindRight.png) Go one page forward

:   Shift the timeline to go about one screen width forward in time.
    Same as the \"forward\" mouse button (Windows).

![arrowDown](images/arrowDown.png) Reduce the time scale

:   Reduce the time scale in major steps. Fine scaling is meant to be
    done with the mouse wheel.

![fitToWindow](images/fitToWindow.png) Fit to window

:   This sets the scale and moves the timeline, so that all sections
    with valid or substituted date/time information fit into the window.

![arrowUp](images/arrowUp.png) Increase the time scale

:   Increase the time scale in major steps. Fine scaling is meant to be
    done with the mouse wheel.

![undo](images/undo.png) Undo the last change

:   This restores date/time/duration before the last mouse operation on
    a section.

