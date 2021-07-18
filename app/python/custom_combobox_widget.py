# custom_combobox_widget.py

'''
    Replaces ttk.Combobox with an easily configurable widget.

    Configuration is done tkinter style, instead of pitting ttk.Style
    and Windows themes against each other to see which one wins, as is
    the norm when trying to configure ttk widgets.

    Unlike ttk.Combobox...
        ...dropdown items are selected with mouse, Return key, or spacebar
        ...colors including Entry background are easily configured
        ...clicking either Entry or Arrow opens then closes dropdown on 
            alternate clicks
        ...FocusOut event can be bound to the dropdown items
        ...arrow traversal thru dropdown loops to top or bottom when bottom 
            or top is reached
        ...dropdown opens with either Up or Down arrow key, with either top 
            or bottom item highlighted
        ...a long dropdown auto-scrolls while traversing with arrow keys
        ...a dropdown item with text longer than the window displays a tooltip 
            that shows the whole text
        ...the arrow button changes color when the Entry is in focus.
'''

import tkinter as tk
from widgets import (FrameHilited3, Entry, ToplevelHilited, Frame,
    LabelHilited, ButtonFlatHilited, LabelTip2, CanvasHilited)
from scrolling import Scrollbar
from styles import config_generic, make_formats_dict
import dev_tools as dt
from dev_tools import looky, seeline



class Combobox(FrameHilited3):
    hive = []

    def __init__(
            self, 
            master, 
            root, 
            callback=None,
            height=480, 
            values=[], 
            scrollbar_size=24, 
            *args, **kwargs):
        FrameHilited3.__init__(self, master, *args, **kwargs)
        '''
            This is a replacement for ttk.Combobox.
        '''

        self.master = master
        self.callback = callback
        self.root = root
        self.height = height
        self.values = values
        self.scrollbar_size = scrollbar_size
    
        self.formats = make_formats_dict()

        self.buttons = []
        self.selected = None
        self.result_string = ''

        self.entered = None
        self.lenval = len(self.values)
        self.owt = None
        self.scrollbar_clicked = False
        self.typed = None

        self.screen_height = self.winfo_screenheight()
        self.config(bd=0)

        # simulate <<ComboboxSelected>>:
        self.var = tk.StringVar()
        self.var.trace_add('write', lambda *args, **kwargs: self.combobox_selected()) 

        # simulate ttk.Combobox.current()
        self.current = 0

        self.make_widgets()
        self.master.bind_all('<ButtonRelease-1>', self.close_dropdown, add='+')

        # self.root.bind('<Configure>', self.hide_all_drops) # DO NOT DELETE
        # Above binding closes dropdown if Windows title bar is clicked, it
        #   has no other purpose. But it causes minor glitches e.g. if a
        #   dropdown button is highlighted and focused, the Entry has to be
        #   clicked twice to put it back into the alternating drop/undrop
        #   cycle as expected. Without this binding, the click on the title
        #   bar lowers the dropdown below the root window which is good 
        #   enough for now. To get around it, use the custom_window_border.py.

        # expose only unique methods of Entry e.g. not self.config (self is a Frame and
        #    the Entry, Toplevel, Canvas, and window have to be configured together) so
        #    to size the entry use instance.config_drop_width(72)
        self.insert = self.entry.insert
        self.delete = self.entry.delete
        self.get = self.entry.get

    def make_widgets(self):
        self.entry = Entry(self, textvariable=self.var)
        self.arrow = LabelHilited(self, text='\u25BC', width=2)
        # self.arrow = ComboboxArrow(self, text='\u25BC', width=2)

        self.entry.grid(column=0, row=0)
        self.arrow.grid(column=1, row=0)

        self.update_idletasks()
        self.width = self.winfo_reqwidth()

        self.drop = ToplevelHilited(
            self,
            bd=0)
        self.drop.bind('<Destroy>', self.clear_reference_to_dropdown)
        self.drop.withdraw()
        Combobox.hive.append(self.drop)
        for widg in (self.master, self.drop):
            widg.bind('<Escape>', self.hide_all_drops, add='+')

        self.drop.grid_columnconfigure(0, weight=1)
        self.drop.grid_rowconfigure(0, weight=1)

        self.canvas = CanvasHilited(self.drop)
        self.canvas.grid(column=0, row=0, sticky='news')

        self.scrollv_combo = Scrollbar(
            self.drop, hideable=True, command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollv_combo.set)
        self.content = Frame(self.canvas)

        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure('all', weight=1)

        self.scrollv_combo.grid(column=1, row=0, sticky='ns') 

        self.entry.bind('<KeyPress>', self.open_or_close_dropdown)
        self.entry.bind('<Tab>', self.open_or_close_dropdown)

        for widg in (self.entry, self.arrow):
            widg.bind('<Button-1>', self.open_or_close_dropdown, add='+')
    
        self.arrow.bind('<Button-1>', self.focus_entry_on_arrow_click, add='+')        

        for frm in (self, self.content):
            frm.bind('<FocusIn>', self.arrow.highlight)
            frm.bind('<FocusOut>', self.arrow.unhighlight)

        self.drop.bind('<FocusIn>', self.focus_dropdown)
        self.drop.bind('<Unmap>', self.unhighlight_all_drop_items)

        self.current_combo_parts = [self, self.entry, self.arrow, self.scrollv_combo]
        for part in self.current_combo_parts:
            part.bind('<Enter>', self.unbind_combo_parts)
            part.bind('<Leave>', self.rebind_combo_parts)

        self.config_values(self.values)

        config_generic(self.drop)

    def unbind_combo_parts(self, evt):
        self.master.unbind_all('<ButtonRelease-1>')

    def rebind_combo_parts(self, evt):
        self.master.bind_all('<ButtonRelease-1>', self.close_dropdown, add='+')

    def unhighlight_all_drop_items(self, evt):
        for child in self.content.winfo_children():
            child.config(bg=self.formats['highlight_bg'])

    def clear_reference_to_dropdown(self, evt):
        dropdown = evt.widget
        if dropdown in Combobox.hive:
            idx = Combobox.hive.index(dropdown)
            del Combobox.hive[idx]  
            dropdown = None

    def config_values(self, values):
        '''
            The vertical scrollbar, when there is one, overlaps the 
            dropdown button highlight but both still work. To change
            this, the button width can be changed when the scrollbar
            appears and disappears.
        '''

        # a sample button is made to get its height, then destroyed
        b = ButtonFlatHilited(self.content, text='Sample')
        one_height = b.winfo_reqheight()
        b.destroy()
        self.fit_height = one_height * len(values)

        self.values = values
        self.lenval = len(self.values)

        for button in self.buttons:
            button.destroy()
        self.buttons = []

        host_width = self.winfo_reqwidth()
        self.window = self.canvas.create_window(
            0, 0, anchor='nw', window=self.content, width=host_width)
        self.canvas.config(scrollregion=(0, 0, host_width, self.fit_height))
        c = 0
        for item in values:
            bt = ButtonFlatHilited(self.content, text=item, anchor='w')
            bt.grid(column=0, row=c, sticky='ew')  
            for event in ('<Button-1>', '<Return>', '<space>'):
                bt.bind(event, self.get_clicked, add='+')
            bt.bind('<Enter>', self.highlight)
            bt.bind('<Leave>', self.unhighlight)
            bt.bind('<Tab>', self.tab_out_of_dropdown_fwd)
            bt.bind('<Shift-Tab>', self.tab_out_of_dropdown_back)
            bt.bind('<KeyPress>', self.traverse_on_arrow)
            bt.bind('<FocusOut>', self.unhighlight)
            bt.bind('<FocusOut>', self.get_tip_widg, add='+')
            bt.bind('<FocusIn>', self.get_tip_widg)
            bt.bind('<Enter>', self.get_tip_widg, add='+')
            bt.bind('<Leave>', self.get_tip_widg, add='+')
            self.buttons.append(bt)
            c += 1
        for b in self.buttons:
            b.config(command=self.callback)

    def get_tip_widg(self, evt):
        '''
            '10' is FocusOut, '9' is FocusIn
        '''
        if self.winfo_reqwidth() <= evt.widget.winfo_reqwidth():
            widg = evt.widget
            evt_type = evt.type
            if evt_type in ('7', '9'):
                self.show_overwidth_tip(widg)
            elif evt_type in ('8', '10'):
                self.hide_overwidth_tip()

    def show_overwidth_tip(self, widg):
        '''
            Instead of a horizontal scrollbar, if a dropdown item doesn't all
            show in the space allotted, the full text will appear in a tooltip
            on highlight. Most of this code is borrowed from Michael Foord.
        '''
        text=widg.cget('text')
        if self.owt:
            return
        x, y, cx, cy = widg.bbox()
        x = x + widg.winfo_rootx() + 32
        y = y + cy + widg.winfo_rooty() + 32
        self.owt = ToplevelHilited(self)
        self.owt.wm_overrideredirect(1)
        l = LabelTip2(self.owt, text=text) 
        l.pack(ipadx=6, ipady=3)
        self.owt.wm_geometry('+{}+{}'.format(x, y))

    def hide_overwidth_tip(self):    
        tip = self.owt
        self.owt = None
        if tip:
            tip.destroy() 

    def highlight_arrow(self, evt):
        self.arrow.config(bg=self.formats['head_bg'])

    def unhighlight_arrow(self, evt):
        self.arrow.config(bg=self.formats['highlight_bg'])

    def focus_entry_on_arrow_click(self, evt):
        self.focus_set()
        self.entry.select_range(0, 'end')  

    def hide_other_drops(self):
        for dropdown in Combobox.hive:
            if dropdown != self.drop:
                dropdown.withdraw()

    def hide_all_drops(self, evt=None):
        for dropdown in Combobox.hive:
            dropdown.withdraw()

    def close_dropdown(self, evt):
        '''
            Runs only on ButtonRelease-1.

            In the case of a destroyable combobox in a dialog, after the
            combobox is destroyed, this event will cause an error because
            the dropdown no longer exists. I think this is harmless so I
            added the try/except to pass on it instead of figuring out how
            to prevent the error.
        '''
        widg = evt.widget
        if widg == self.scrollv_combo:
            self.scrollbar_clicked = True
        try:
            self.drop.withdraw()
        except tk.TclError:
            pass

    def config_drop_width(self, new_width):
        self.entry.config(width=new_width)
        self.update_idletasks()
        self.width = self.winfo_reqwidth()
        self.drop.geometry('{}x{}'.format(self.width, self.height)) 
        self.scrollregion_width = new_width
        self.canvas.itemconfigure(self.window, width=self.width)
        self.canvas.configure(scrollregion=(0, 0, new_width, self.fit_height))

    def open_or_close_dropdown(self, evt=None):
        if evt is None: # dropdown item clicked--no evt bec. of Button command option
            if self.callback:
                self.callback(self.selected)
            self.drop.withdraw()
            return
        if len(self.buttons) == 0:
            return
        evt_type = evt.type
        evt_sym = evt.keysym
        if evt_sym == 'Tab':
            self.drop.withdraw()
            return
        elif evt_sym == 'Escape':
            self.hide_all_drops()
            return
        first = None
        last = None
        if len(self.buttons) != 0:
            first = self.buttons[0]
            last = self.buttons[len(self.buttons) - 1]
        # self.drop.winfo_ismapped() gets the wrong value
        #   if the scrollbar was the last thing clicked
        #   so drop_is_open has to be used also.
        if evt_type == '4':
            if self.drop.winfo_ismapped() == 1:
                drop_is_open = True
            elif self.drop.winfo_ismapped() == 0:
                drop_is_open = False
            if self.scrollbar_clicked is True:
                drop_is_open = True
                self.scrollbar_clicked = False
            if drop_is_open is True:
                self.drop.withdraw() 
                drop_is_open = False
                return
            elif drop_is_open is False:
                pass
        elif evt_type == '2':
            if evt_sym not in ('Up', 'Down'):
                return
            elif first is None or last is None:
                pass
            elif evt_sym == 'Down':
                first.config(bg=self.formats['bg'])
                first.focus_set()
                self.canvas.yview_moveto(0.0)
            elif evt_sym == 'Up':
                last.config(bg=self.formats['bg'])
                last.focus_set()
                self.canvas.yview_moveto(1.0)

        self.update_idletasks()
        x = self.winfo_rootx()
        y = self.winfo_rooty()
        combo_height = self.winfo_reqheight()

        self.fit_height = self.content.winfo_reqheight()
        self.drop.wm_overrideredirect(1)
        fly_up = self.get_vertical_pos(combo_height, evt)
        if fly_up[0] is False:            
            y = y + combo_height
        else:
            y = fly_up[1]
       
        self.drop.geometry('{}x{}+{}+{}'.format(
            self.width, self.height, x, y)) 
        self.drop.deiconify() 
        self.hide_other_drops()

    def get_vertical_pos(self, combo_height, evt):
        fly_up = False
        vert_pos = evt.y_root - evt.y
        clearance = self.screen_height - (vert_pos + combo_height)
        if clearance < self.height:
            fly_up = True

        return (fly_up, vert_pos - self.height)

    def highlight(self, evt):
        for widg in self.buttons:
            widg.config(bg=self.formats['highlight_bg'])
        widget = evt.widget
        widget.config(bg=self.formats['bg'])
        self.selected = widget
        widget.focus_set()

    def unhighlight(self, evt):
        x, y = self.winfo_pointerxy()
        hovered = self.winfo_containing(x,y)
        if hovered in self.buttons:
            evt.widget.config(bg=self.formats['highlight_bg'])

    def hide_drops_on_title_bar_click(self, evt):
        x, y = self.winfo_pointerxy()
        hovered = self.winfo_containing(x,y)

    def focus_dropdown(self, evt):
        for widg in self.buttons:
            widg.config(takefocus=1)

    def handle_tab_out_of_dropdown(self, go):

        for widg in self.buttons:
            widg.config(takefocus=0)

        self.entry.delete(0, 'end')
        self.entry.insert(0, self.selected.cget('text'))
        self.drop.withdraw()
        self.entry.focus_set()
        if go == 'fwd':
            goto = self.entry.tk_focusNext()
        elif go == 'back':
            goto = self.entry.tk_focusPrev()
        goto.focus_set()

    def tab_out_of_dropdown_fwd(self, evt):
        self.selected = evt.widget
        self.handle_tab_out_of_dropdown('fwd')

    def tab_out_of_dropdown_back(self, evt):
        self.selected = evt.widget
        self.handle_tab_out_of_dropdown('back')

    def get_clicked(self, evt):

        self.selected = evt.widget
        self.current = self.selected.grid_info()['row']
        self.entry.delete(0, 'end')
        self.entry.insert(0, self.selected.cget('text')) 
        self.entry.select_range(0, 'end')
        self.open_or_close_dropdown()  

    def get_typed(self):
        self.typed = self.var.get()    

    def highlight_on_traverse(self, evt, next_item=None, prev_item=None):

        evt_type = evt.type
        evt_sym = evt.keysym # 2 is key press, 4 is button press

        for widg in self.buttons:
            widg.config(bg=self.formats['highlight_bg'])
        if evt_type == '4':
            self.selected = evt.widget
        elif evt_type == '2' and evt_sym == 'Down':
            self.selected = next_item
        elif evt_type == '2' and evt_sym == 'Up':
            self.selected = prev_item

        self.selected.config(bg=self.formats['bg'])
        self.widg_height = int(self.fit_height / self.lenval)
        widg_screenpos = self.selected.winfo_rooty()
        widg_listpos = self.selected.winfo_y()
        win_top = self.drop.winfo_rooty()
        win_bottom = win_top + self.height
        win_ratio = self.height / self.fit_height
        list_ratio = widg_listpos / self.fit_height
        widg_ratio = self.widg_height / self.fit_height
        up_ratio = list_ratio - win_ratio + widg_ratio

        if widg_screenpos > win_bottom - 0.75 * self.widg_height:
            self.canvas.yview_moveto(float(list_ratio))
        elif widg_screenpos < win_top:
            self.canvas.yview_moveto(float(up_ratio))
        self.selected.focus_set()

    def traverse_on_arrow(self, evt):
        if evt.keysym not in ('Up', 'Down'):
            return
        widg = evt.widget
        sym = evt.keysym
        self.widg_height = int(self.fit_height / self.lenval)
        self.trigger_down = self.height - self.widg_height * 3
        self.trigger_up = self.height - self.widg_height * 2
        self.update_idletasks()
        next_item = widg.tk_focusNext()
        prev_item = widg.tk_focusPrev()
        rel_ht = widg.winfo_y()

        if sym == 'Down':
            if next_item in self.buttons:
                self.highlight_on_traverse(evt, next_item=next_item)
            else:
                next_item = self.buttons[0]
                next_item.focus_set()
                next_item.config(bg=self.formats['bg'])
                self.canvas.yview_moveto(0.0)

        elif sym == 'Up':
            if prev_item in self.buttons:
                self.highlight_on_traverse(evt, prev_item=prev_item)
            else:
                prev_item = self.buttons[self.lenval-1]
                prev_item.focus_set()
                prev_item.config(bg=self.formats['bg'])
                self.canvas.yview_moveto(1.0)

    def colorize(self):
        # print("line", looky(seeline()).lineno, "self:", self)
        # print("line", looky(seeline()).lineno, "self.entry:", self.entry)
        # print("line", looky(seeline()).lineno, "self.arrow:", self.arrow)
        # print("line", looky(seeline()).lineno, "self.drop:", self.drop)
        # print("line", looky(seeline()).lineno, "self.canvas:", self.canvas)
        # print("line", looky(seeline()).lineno, "self.scrollv_combo:", self.scrollv_combo)
        # print("line", looky(seeline()).lineno, "self.content:", self.content)
        # print("line", looky(seeline()).lineno, "self.buttons:", self.buttons)
        print("line", looky(seeline()).lineno, "running:")
        # the widgets that don't respond to events are working
        # the scrollbar, which has its own colorize method, is working
        # the arrow label has its own highlight methods, it's working
        self.config(bg=self.formats['bg'])
        self.entry.config(bg=self.formats['highlight_bg'])
        self.drop.config(bg=self.formats['highlight_bg'])
        self.content.config(bg=self.formats['highlight_bg'])
        # The dropdown buttons respond to so many events that it might be
        #   a sort of minor miracle to make them colorize instantly. For
        #   now it's enough that they colorize on reload and they are not
        #   on top, they're only seen on dropdown.
        

    def callback(self):
        '''
            A function specified on instantiation.
        '''
        print('this will not print if overridden (callback)')

    def combobox_selected(self):
        '''
            A function specified on instantiation will run when
            the selection is made. Similar to ttk's <<ComboboxSelected>>
            but instead of binding to a virtual event.
        '''
        print('this will not print if overridden (combobox_selected)')

if __name__ == '__main__':

    '''
        This example shows the use of `combobox_selected()`, the `callback`
        parameter, and a sample binding to the dropdown items themselves.
        * `combobox_selected()` does something when a dropdown item is selected
        * the `callback` parameter is a function passed in the constructor
        * unlike ttk Combobox, this one can bind functions to dropdown item events
    '''

    from widgets import FrameStay, Label, Frame

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

    caseless_colors = []
    for color in color_strings:
        color = color.lower()
        caseless_colors.append(color)

    short_list = ('yellow', 'red', 'blue')

    def color_background(button=None, combo=None):
        '''
            Selects the right widget because only one at a time is not None.
        '''
        def do_it():
            frm.config(bg=color)
            combo.selected = None
            combo.typed = None
        combo = None
        if button == flat:
            combo = b
        elif button is flat2:
            combo = bb
        if combo == None:
            return
        combo.get_typed()
        if combo.selected:
            color = combo.selected.cget('text')
            do_it()
        elif combo.typed:
            color = combo.typed
            do_it()

    def combobox_selected(cbo):
        string_input = cbo.var.get()
        if string_input in caseless_colors:
            color = string_input
            ok = '{}\nis a\nvalid\ncolor.'.format(color.title())
            cbox_select.config(text=ok)
        else:
            cbox_select.config(text=msg)  

    def test_bind_to_dropdown_items(evt):
        print("evt.widget.cget('text'):", evt.widget.cget('text'))

    root = tk.Tk()
    root.focus_set()
    root.grid_columnconfigure(0, weight=1)
    root.geometry('+500+200')

    content = Frame(root)
    content.grid()

    b = Combobox(
        content,
        root,
        callback=color_background,
        height=75, 
        values=caseless_colors,
        scrollbar_size=16)
    flat = ButtonFlatHilited(content, text='Apply Combo 1')
    flat.config(command=lambda button=flat: color_background(button))
    b.config_values(short_list)

    # You can't do this in ttk.Combobox:
    for widg in b.buttons:
        widg.bind('<FocusOut>', test_bind_to_dropdown_items)

    bb = Combobox(
        content,
        root,
        callback=color_background,
        height=450, 
        values=caseless_colors,
        scrollbar_size=16)
    bb.config_drop_width(50)
    bb.update_idletasks()

    flat2 = ButtonFlatHilited(content, text='Apply Combo 2')
    flat2.config(command=lambda button=flat2: color_background(button))

    b.grid(column=0, row=0, padx=6, pady=6)
    flat.grid(column=1, row=0, padx=6, pady=6)
    bb.grid(column=2, row=0, padx=6, pady=6)
    flat2.grid(column=3, row=0, padx=6, pady=6)

    frm = FrameStay(content)
    for i in range(10):
        lab = Label(frm, text=i)
        lab.grid(column=0, row=i+1, sticky='ew')

    msg = 'No valid\ncolor\nhas been\nchosen'
    cbox_select = Label(content, text=msg)
    frm.grid(column=0, row=1, sticky='news', columnspan=3)
    cbox_select.grid(column=3, row=1, sticky='news')

    # Extra line if any Combobox has a combobox_selected function to perform:
    Combobox.combobox_selected = combobox_selected

    root.mainloop()





