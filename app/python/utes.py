# utes.py

import tkinter as tk
from styles import make_formats_dict
import dev_tools as dt

# CENTERING

def center_window(win):
    '''
    Code by Honest Abe at StackOverflow.
    Centers a window in the screen taking account of non-tk elements.
    Doesn't currently work with resize_window() and/or resize_scrollbar().
    '''
    win.update_idletasks()
    width = win.winfo_reqwidth()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_reqheight()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def center_dialog(dlg, frame=None):
    '''
        Try to use center_window() above, it's better.
    '''
    if frame:
        dlg.update_idletasks()
        win_width = frame.winfo_reqwidth()
        win_height = frame.winfo_reqheight()
        right_pos = int(dlg.winfo_screenwidth()/2 - win_width/2)
        down_pos = int(dlg.winfo_screenheight()/2 - win_height/2)
    else:
        dlg.update_idletasks()
        win_width = dlg.winfo_reqwidth()
        win_height = dlg.winfo_reqheight()
        right_pos = int(dlg.winfo_screenwidth()/2 - win_width/2)
        down_pos = int(dlg.winfo_screenheight()/2 - win_height/2)

    return right_pos, down_pos 

formats = make_formats_dict()

#   -   -   -   see widgets.py for statusbar tooltips   -   -   -   #

class ToolTip(object):
    '''
        TOOLTIPS BY MICHAEL FOORD 
        Don't use for anything that'll be destroyed by clicking because
        tooltips are displayed by pointing w/ mouse and thus a tooltip 
        will be displaying when destroy takes place thus leaving the 
        tooltip on the screen since the FocusOut that is supposed to 
        destroy the tooltip can't take place.
    '''

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        ''' Display text in tooltip window '''

        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except tk.TclError:
            pass
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", 10, "normal"),
                      fg='black')
        label.pack(ipadx=6)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()    

def create_tooltip(widget, text):
    ''' Call w/ arguments to use M. Foord's ToolTip class. '''
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()

    toolTip = ToolTip(widget)
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #

# make a canvas scroll with mousewheel
def scroll_on_mousewheel(evt, canvas):
    canvas.yview_scroll(int(-1*(evt.delta/120)), 'units')