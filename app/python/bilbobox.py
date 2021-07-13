# bilbobox

# This is like a combobox but only works with the mouse. Tab key, arrow keys, etc. are not used. It also opens the dropdown list on hover instead of click. I like it but I think it will annoy people by not doing what they expect so I'm putting it back in mothballs for now. At the time this worked, it was using a scrolled canvas class which made things harder instead of easier. So to unbreak this code, just scrape off the unusable cruft leftover from the scrolled canvas class, put a frame in a normal canvas with create_window to replace canvas.content and the like, and add a Toykinter scrollbar where this code expects to see a scrollbar (canvas.vert, canvas.horiz etc.). 

import tkinter as tk
from widgets import (FrameHilited3, Entry, ToplevelHilited, 
    LabelHilited, ButtonFlatHilited, LabelTip)
from scrolling import CanvasScrolledBG2
from styles import config_generic, make_formats_dict
import dev_tools as dt



formats = make_formats_dict()

class Bilbobox(FrameHilited3):
    hive = []
    def __init__(self, master, callback, height=480, values=[], scrollbar_size=24, *args, **kwargs):
        FrameHilited3.__init__(self, master, *args, **kwargs)

        self.master = master
        self.callback = callback
        self.height = height
        self.values = values
        self.scrollbar_size = scrollbar_size

        self.buttons = []
        self.selected_button = None
        self.result_string = ''

        self.entered = None

        self.config(bd=0, relief='sunken')

        self.make_widgets()
        # without add='+' the first Bilbobox created can only be 
        #    withdrawn by clicking on one of its dropdown items or on the title bar
        #    Can't be bound to button click; that would remove the button from its own event.
        master.bind_all('<ButtonRelease-1>', self.close_dropdown, add='+')
 
    def make_widgets(self):
        '''
            The entry and arrow need to trigger the same events, but binding
            them to the same events would be a can of worms because of the
            Enter and Leave events. Instead, the binding is to self--the frame 
            that both the entry and the arrow are in--and the underlying frame
            sees the events and responds.
        '''

        self.entry = Entry(self)
        self.arrow = LabelHilited(self, text='\u25EF', width=2)
        self.arrow.bind('<Button-1>', self.focus_entry_on_arrow_click)

        self.entry.grid(column=0, row=0)
        self.arrow.grid(column=1, row=0, padx=0, pady=0)

        self.update_idletasks()
        self.width = self.winfo_reqwidth()

        self.drop = ToplevelHilited(
            self,
            bd=0)
        self.drop.withdraw()
        self.drop.bind('<Unmap>', self.focus_entry_on_unmap)
        Bilbobox.hive.append(self.drop)
        self.master.bind('<Escape>', self.hide_all_drops)

        self.drop.grid_columnconfigure(0, weight=1)
        self.drop.grid_rowconfigure(0, weight=1)

        self.canvas = CanvasScrolledBG2(
            self.drop,
            fixed_width=True,
            scrollregion_width=self.width,
            scrollbar='vert')
        self.canvas.grid(column=0, row=0, sticky='news')

        self.canvas.content.grid_columnconfigure(0, weight=1)
        self.canvas.content.grid_rowconfigure('all', weight=1)

        self.canvas.vert.grid(column=1, row=0, sticky='ns') 

        self.bind('<Enter>', self.open_dropdown)

        for widg in (self, self.canvas.vert, self.canvas.content):
            widg.bind('<Leave>', self.hide_this_drop)
            widg.bind('<Enter>', self.detect_enter, add='+')

        for frm in (self, self.canvas.content):
            frm.bind('<FocusIn>', self.highlight_arrow)
            frm.bind('<FocusOut>', self.unhighlight_arrow)

        self.config_values(self.values)
        config_generic(self.drop)

    def detect_enter(self, evt):
        '''
            Depending on which widget is left and which is entered by mouse,
            a delayed response from a Leave event closes the dropdown if
            the entered widget says it's OK to do so.
        '''
        self.entered = evt.widget

    def hide_this_drop(self, evt):
        '''
            The after() method is needed so that the Enter event has time 
            to set self.entered before the Leave event closes the dropdown. 
            Works if after() runs after 100 microseconds but if 500, it 
            gives the user a chance to recover from overshooting the scrollbar 
            (for example), yet without imposing a noticeable wait if the user 
            was serious about leaving the widget.
        '''
        def do_after_bool_set():
            if self.entered is None or self.entered not in (self, self.canvas.content, self.canvas.vert):
                self.drop.withdraw()
                self.entered = None
        self.entered = None
        evt.widget.after(500, do_after_bool_set)

    def config_values(self, values):
        b = ButtonFlatHilited(self.canvas.content, text='Sample')
        one_height = b.winfo_reqheight()
        b.destroy()
        self.fit_height = one_height * len(values)

        self.values = values

        for button in self.buttons:
            button.destroy()
        self.buttons = []

        if self.drop in Bilbobox.hive:
            idx = Bilbobox.hive.index(self.drop)
            del Bilbobox.hive[idx]

        CanvasScrolledBG2.config_fixed_width_canvas(self)

        c = 0
        for choice in values:
            bt = ButtonFlatHilited(self.canvas.content, text=choice, anchor='w')
            bt.grid(column=0, row=c, sticky='ew') # why t+1 in mockup?
            for event in ('<Button-1>', '<Return>', '<space>'):
                bt.bind(event, self.get_clicked)
            bt.bind('<Enter>', self.highlight)
            bt.bind('<Leave>', self.unhighlight)
            self.buttons.append(bt)
            c += 1
        for b in self.buttons:
            b.config(command=self.callback)

    def show_overwidth_tip(self, widg):
        '''
            Instead of a horizontal scrollbar, if a dropdown item doesn't all
            show in the space allotted, the full text will appear in a tooltip
            on highlight.
        '''

        self.owt = None

        if self.winfo_reqwidth() <= widg.winfo_reqwidth():
            text=widg.cget('text')

            x, y, cx, cy = widg.bbox()
            x = x + widg.winfo_rootx() + 32
            y = y + cy + widg.winfo_rooty() + 32
            self.owt = ToplevelHilited(self)
            self.owt.wm_overrideredirect(1)
            l = LabelTip(self.owt, text=text) 
            l.pack(ipadx=6, ipady=3)
            self.owt.wm_geometry('+{}+{}'.format(x, y))

    def hide_overwidth_tip(self, widg):        
        tip = self.owt
        self.owt = None
        if tip:
            tip.destroy() 

    def highlight_arrow(self, evt):
        self.arrow.config(bg=formats['table_head_bg'])

    def unhighlight_arrow(self, evt):
        self.arrow.config(bg=formats['highlight_bg'])

    def callback(self):
        print('this will not print if overridden')

    def focus_entry_on_unmap(self, evt):
        self.entry.focus_set()
        self.entry.select_range(0, 'end')

    def focus_entry_on_arrow_click(self, evt):
        self.focus_set()
        self.entry.select_range(0, 'end')            

    def get_clicked(self, evt):
        self.selected_button = sb = evt.widget
        self.entry.delete(0, 'end')
        self.entry.insert(0, sb.cget('text')) 

    def hide_other_drops(self):
        for dropdown in Bilbobox.hive:
            if dropdown != self.drop:
                dropdown.withdraw()

    def hide_all_drops(self, evt):
        for dropdown in Bilbobox.hive:
            dropdown.withdraw()

    def open_dropdown(self, evt=None):
        ''' 
            Unlike a combobox, a Bilbobox drops down when hovered
            by the mouse.
        '''
        
        self.update_idletasks()
        x = self.winfo_rootx()
        y = self.winfo_rooty()
        y_off = self.winfo_reqheight()

        self.fit_height = self.canvas.content.winfo_reqheight()
        self.drop.wm_overrideredirect(1)
       
        self.drop.geometry('{}x{}+{}+{}'.format(
                self.width, self.height, x, y + y_off))   
        self.drop.deiconify() 
        self.hide_other_drops()

    def highlight(self, evt):
        widg = evt.widget
        self.update_idletasks()
        widg.config(bg=formats['bg'])
        self.show_overwidth_tip(widg)

    def unhighlight(self, evt):
        widg = evt.widget
        widg.config(bg=formats['highlight_bg'])
        self.hide_overwidth_tip(widg)

    def close_dropdown(self, evt):
        '''
            Runs only on ButtonRelease-1.
        '''

        if evt.widget == self.arrow:
            if self.drop.winfo_ismapped() == 1:
                self.drop.withdraw()
            elif self.drop.winfo_ismapped() == 0:
                self.open_dropdown()
        elif evt.widget in (self.canvas.vert,):
            if evt.type == '8':
                self.drop.withdraw()
            else:
                pass # this pass is needed here, don't delete this condition
        else:
            self.drop.withdraw()


if __name__ == '__main__':

    from widgets import FrameStay, Label
    from scrolling import CanvasScrolledBG1, CanvasScrolled

    color_strings = [
        'AliceBlue',
        'AntiqueWhite',
        'Aqua',
        'Aquamarine',
        'Azure',
        'Beige',
        'Bisque',
        'Black',
        'BlanchedAlmond',
        'Blue',
        'BlueViolet',
        'Brown',
        'BurlyWood',
        'CadetBlue',
        'Chartreuse',
        'Chocolate',
        'Coral',
        'CornflowerBlue',
        'Cornsilk',
        'Crimson',
        'Cyan',
        'DarkBlue',
        'DarkCyan',
        'DarkGoldenRod',
        'DarkGray',
        'DarkGrey',
        'DarkGreen',
        'DarkKhaki',
        'DarkMagenta',
        'DarkOliveGreen',
        'DarkOrange',
        'DarkOrchid',
        'DarkRed',
        'DarkSalmon',
        'DarkSeaGreen',
        'DarkSlateBlue',
        'DarkSlateGray',
        'DarkSlateGrey',
        'DarkTurquoise',
        'DarkViolet',
        'DeepPink',
        'DeepSkyBlue',
        'DimGray',
        'DimGrey',
        'DodgerBlue',
        'FireBrick',
        'FloralWhite',
        'ForestGreen',
        'Fuchsia',
        'Gainsboro',
        'GhostWhite',
        'Gold',
        'GoldenRod',
        'Gray',
        'Grey',
        'Green',
        'GreenYellow',
        'HoneyDew',
        'HotPink',
        'IndianRed',
        'Indigo',
        'Ivory',
        'Khaki',
        'Lavender',
        'LavenderBlush',
        'LawnGreen',
        'LemonChiffon',
        'LightBlue',
        'LightCoral',
        'LightCyan',
        'LightGoldenRodYellow',
        'LightGray',
        'LightGrey',
        'LightGreen',
        'LightPink',
        'LightSalmon',
        'LightSeaGreen',
        'LightSkyBlue',
        'LightSlateGray',
        'LightSlateGrey',
        'LightSteelBlue',
        'LightYellow',
        'Lime',
        'LimeGreen',
        'Linen',
        'Magenta',
        'Maroon',
        'MediumAquaMarine',
        'MediumBlue',
        'MediumOrchid',
        'MediumPurple',
        'MediumSeaGreen',
        'MediumSlateBlue',
        'MediumSpringGreen',
        'MediumTurquoise',
        'MediumVioletRed',
        'MidnightBlue',
        'MintCream',
        'MistyRose',
        'Moccasin',
        'NavajoWhite',
        'Navy',
        'OldLace',
        'Olive',
        'OliveDrab',
        'Orange',
        'OrangeRed',
        'Orchid',
        'PaleGoldenRod',
        'PaleGreen',
        'PaleTurquoise',
        'PaleVioletRed',
        'PapayaWhip',
        'PeachPuff',
        'Peru',
        'Pink',
        'Plum',
        'PowderBlue',
        'Purple',
        'Red',
        'RosyBrown',
        'RoyalBlue',
        'SaddleBrown',
        'Salmon',
        'SandyBrown',
        'SeaGreen',
        'SeaShell',
        'Sienna',
        'Silver',
        'SkyBlue',
        'SlateBlue',
        'SlateGray',
        'SlateGrey',
        'Snow',
        'SpringGreen',
        'SteelBlue',
        'Tan',
        'Teal',
        'Thistle',
        'Tomato',
        'Turquoise',
        'Violet',
        'Wheat',
        'White',
        'WhiteSmokewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww',
        'Yellow']

    short_list = ('yellow', 'red', 'blue')

    def colorize():
        '''
            Selects the right widget because only one at a time is not None.
        '''
        def do_it():
            frm.config(bg=color)
            
        colors = []
        for widg in (b, bb):
            if widg.selected_button:
                color = widg.selected_button.cget('text')
                widg.selected_button = None
                do_it()        

    root = tk.Tk()
    root.focus_set()
    root.grid_columnconfigure(0, weight=1)

    # main canvas
    canvas_0 = CanvasScrolledBG1(root, resizable=True, scrollbar='both')
    CanvasScrolledBG1.config_resizable_canvas(canvas_0) # *****
    canvas_0.grid(column=0, row=0, sticky='news')
    canvas_0.vert.grid(column=1, row=0, sticky='ns')
    canvas_0.horiz.grid(column=0, row=1, sticky='ew') 
    canvas_0.content.grid_columnconfigure(0, weight=1)
    canvas_0.content.grid_rowconfigure(1, weight=1)

    b = Bilbobox(
        canvas_0.content,   
        colorize, 
        height=300, 
        values=color_strings,
        scrollbar_size=16)
    bb = Bilbobox(
        canvas_0.content, 
        colorize, 
        height=600, 
        values=color_strings,
        scrollbar_size=16)
    # bb.config_values(short_list)

    flat = ButtonFlatHilited(canvas_0.content, text='Flat Button', command=colorize)

    b.grid(column=0, row=0, padx=6, pady=6)
    bb.grid(column=1, row=0, padx=6, pady=6)
    flat.grid(column=2, row=0, padx=6, pady=6)
        
    frm = FrameStay(canvas_0.content)
    frm.grid(column=0, row=1, sticky='news', columnspan=3)
    for i in range(10):
        lab = Label(frm, text=i)
        lab.grid(column=0, row=i+1, sticky='ew')

    CanvasScrolled.config_scrolled_canvases(main_app=root)

    root.mainloop()