import tkinter as tk
from tkinter import colorchooser
import sqlite3
from widgets import (
    Frame, Canvas, Button, LabelH3, Label, FrameStay, LabelStay, Entry)
from styles import (get_color_schemes, get_color_schemes_plus, make_formats_dict, 
    get_all_descends, config_generic)
from files import current_file
from query_strings import (
    update_format_color_scheme, delete_color_scheme, select_color_scheme_current, 
    update_color_scheme_null, insert_color_scheme, 
)

PORTWIDTH = 840 # make this bigger if tab gets bigger for ex. if another tab gets bigger this one will too; if it doesn't work out, get rid of move_right & move_left, just a toy not important; if something user can do has the power to make the tabs bigger, then this won't work or at least has to be made into a class or something

formats = make_formats_dict()

class Colorizer(Frame):
    def __init__(self, parent, notebook, view, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.notebook = notebook
        self.view = view

        self.old_col = 0
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)

        self.view.bind('<Return>', self.apply_scheme)

        self.r_col = {}

        self.make_widgets()

    def make_widgets(self):

        stripview = Frame(self.parent)
        stripview.grid(column=0, row=0, padx=12, pady=12)

        self.colors_canvas = Canvas(
            stripview, 
            bd=1, highlightthickness=1, 
            highlightbackground=formats['highlight_bg'], 
            bg=formats['bg'], 
            width=PORTWIDTH, height=100)

        hscroll = tk.Scrollbar(
            stripview, orient='horizontal', command=self.colors_canvas.xview)
        self.colors_canvas.configure(xscrollcommand=hscroll.set)
        hscroll.grid(row=1, column=0, sticky="ew")
        self.colors_canvas.grid(column=0, row=0, sticky='news')

        self.colors_content = Frame(self.colors_canvas)

        bbox1 = Frame(self.parent)
        bbox1.grid(column=0, row=1, padx=12, pady=12, sticky='we')
        bbox1.grid_columnconfigure(1, weight=1)
        bbox1.grid_rowconfigure(1, weight=1)

        b4 = Button(
            bbox1, text='TRY', width=7, command=self.config_local)
        b4.grid(column=0, row=0, sticky='w')

        b5 = Button(
            bbox1, text='COPY', width=7, command=self.copy_scheme)
        b5.grid(column=1, row=0)

        self.b6 = Button(
            bbox1, text='APPLY', width=7, command=self.apply_scheme)
        self.b6.grid(column=2, row=0, sticky='e')

        bottom = Frame(self.parent)
        bottom.grid(column=0, row=2, padx=12, pady=12)

        addlab = LabelH3(bottom, text='New Color Scheme')
        addlab.grid(column=0, row=0, padx=6, pady=6, columnspan=2)

        self.colors_table = Frame(bottom)
        self.colors_table.grid(column=0, row=1, columnspan=2)
        self.colors_table.grid_columnconfigure(0, weight=1)
        self.colors_table.grid_rowconfigure(0, weight=1)

        all_schemes = get_color_schemes()

        self.h1 = Label(
            self.colors_table,
            anchor='w', 
            text=' Domain',
            font=formats['output_font'])

        self.h2 = Label(
            self.colors_table,
            anchor='w',
            text=' Color')

        opening_colors = (
            formats['bg'], 
            formats['highlight_bg'], 
            formats['table_head_bg'], 
            formats['fg'])

        displabel = self.make_colors_table(opening_colors)

        bbox2 = Frame(bottom)
        bbox2.grid(
            column=0, row=2, 
            padx=12, pady=12, 
            sticky='ew', columnspan=2)
        bbox2.grid_columnconfigure(1, weight=1)
        bbox2.grid_rowconfigure(0, weight=1)

        b3 = Button(
            bbox2, 
            text='CREATE NEW COLOR SAMPLE', 
            command=self.make_new_sample)
        b3.grid(column=0, row=0, padx=6, pady=6, columnspan=2)

        self.make_samples()

        visited = [

            (self.colors_content,
                "Color Schemes",
                "Double-click color-scheme sample to select.\n"
                    "Selected schemes can be deleted with Delete key "
                    "unless built-in."),
            (b4, "", 
                "Press button or double_click color sample to\npreview "
                "selected color scheme."),
            (b5, "", 
                "Copy selected color scheme and change one\n"
                     "or more colors to create a new scheme."),
            (self.b6, "",
                "Press button or the Enter key to apply selected\ncolor "
                "scheme to the whole application."),
            (self.colors_table, "",
                "Type common color or double-click entry to select from dialog."),
            (b3, "",
                "Create a new color sample from filled-in entries.")]

        self.colors_canvas.create_window(
            0, 0, anchor='nw', window=self.colors_content)
        self.resize_color_samples_scrollbar()

    def resize_color_samples_scrollbar(self):
        self.colors_content.update_idletasks()                   
        self.colors_canvas.config(scrollregion=self.colors_canvas.bbox("all")) 

    def apply_scheme(self, evt=None):
        # APPLY button not invoked by RETURN key unless its tab is on top
        # change index if tab order changes
        # `self.notebook.index('current')` is from ttk.Notebook, ignoring it for 
        #   now, need to add this method to Toykinter TabBook
        # if self.notebook.index('current') == 2:
        self.recolorize()

    def recolorize(self):

        color_scheme = []
        for child in self.colors_content.winfo_children():
            if self.parent.focus_get() == child:
                frm = child

        foc = self.view.focus_get()

        if foc.master != self.colors_content:
            return

        for child in frm.winfo_children():
            color_scheme.append(child['bg'])
            child = child
        color_scheme.append(child['fg'])

        color_scheme = tuple(color_scheme)

        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_format_color_scheme, color_scheme)
        conn.commit()
        cur.close()
        conn.close()

        mbg = color_scheme[0]
        hbg = color_scheme[1]
        thbg = color_scheme[2]
        fg = color_scheme[3]

        config_generic(self.view)
        self.view.config(bg=mbg)

    def make_samples(self):

        all_schemes_plus = get_color_schemes_plus()

        y = 0
        for scheme in all_schemes_plus:
            frm = FrameStay(
                self.colors_content,
                name = '{}{}'.format('cs_', str(scheme[5])),
                bg='lightgray', 
                takefocus=1, 
                bd=1)
            frm.grid(column=y, row=0)
            frm.bind('<FocusIn>', self.change_border_color)
            frm.bind('<FocusOut>', self.unchange_border_color)
            frm.bind('<Key-Delete>', self.delete_sample)

            frm.bind('<Tab>', self.move_right)
            frm.bind('<Shift-Tab>', self.move_left)
            frm.bind('<FocusIn>', self.locate_focus, add='+')

            z = 0
            for color in scheme[0:3]:
                lab = LabelStay(
                    frm, 
                    width=12, 
                    bg=color, 
                    text=color, fg=scheme[3])
                lab.grid(column=y, row=z, ipadx=6, ipady=6)
                lab.bind('<Double-Button-1>', self.config_local)
                z += 1
            y += 1

        self.resize_color_samples_scrollbar()

        self.clear_entries()

    def clear_entries(self):
        for widg in self.colors_table.winfo_children():
            if widg.winfo_class() == 'TEntry':
                widg.delete(0, tk.END)

    def move_right(self, evt):
        if evt.widget.winfo_x() > PORTWIDTH-250:
            self.colors_canvas.xview_moveto(1.0)
        self.old_col = evt.widget.grid_info()['column']

    def move_left(self, evt):
        if evt.widget.winfo_x() < PORTWIDTH:
            self.colors_canvas.xview_moveto(0.0)
        self.old_col = evt.widget.grid_info()['column']
       
    def locate_focus(self, event):
        new_col = event.widget.grid_info()['column']
        if new_col > self.old_col + 1:
            self.colors_canvas.xview_moveto(1.0)
        elif new_col < self.old_col - 1:
            self.colors_canvas.xview_moveto(0.0)

    def detect_colors(self, frm):

        color_scheme = []
        if frm.winfo_class() == 'Label':
            frm = frm.master

        for child in frm.winfo_children():
            color_scheme.append(child['bg'])
            child = child
        color_scheme.append(child['fg'])

        return color_scheme

    def preview_scheme(self, scheme):
        
        trial_widgets = []
        all_widgets_in_tab1 = get_all_descends(
            self.parent, trial_widgets)
        all_widgets_in_tab1.append(self.parent)

        for widg in (all_widgets_in_tab1):
            if (widg.winfo_class() == 'Label' and 
                widg.winfo_subclass() == 'LabelStay'):
                    pass
            elif (widg in self.colors_table.winfo_children() and 
                widg.grid_info()['row'] == 0):
                    widg.config(
                        bg=scheme[2],
                        fg=scheme[3])
            elif (widg.winfo_class() == 'Label' and 
                    widg.winfo_subclass() in ('Label', 'LabelH3')):
                        widg.config(
                            bg=scheme[0],
                            fg=scheme[3])
            elif widg.winfo_class() == 'Button':
                widg.config(
                        bg=scheme[1], 
                        fg=scheme[3],
                        activebackground=scheme[2])
            elif widg in self.colors_content.winfo_children():
                widg.config(bg='lightgray')
            elif widg.winfo_class() in ('Frame', 'Toplevel', 'Canvas'):
                widg.config(bg=scheme[0])

    def config_local(self, evt=None):

        all_schemes = get_color_schemes()

        self.clear_entries()

        # if double-click
        if evt:
     
            if evt.type == '4':
                evt.widget.master.focus_set()
            color_scheme = self.detect_colors(evt.widget)
            self.preview_scheme(color_scheme)

        # if TRIAL button
        else:

            for widg in self.colors_table.winfo_children():

                # if entries not all filled out
                if (widg.winfo_class() == 'TEntry' and
                    len(widg.get()) == 0):
                        pass

                # if new scheme to try
                if (widg.winfo_class() == 'TEntry' and
                    len(widg.get()) > 0):
                        inputs = []
                        inputs = tuple(inputs)

                        # if typed scheme is new
                        if inputs not in all_schemes:
                            self.preview_scheme(inputs)

                        # if scheme already exists
                        else:
                            self.clear_entries()

                # if no sample hilited
                elif self.colors_content.focus_get().winfo_class() != 'Frame':
                    return
                elif (widg.winfo_class() == 'TEntry' and
                    len(widg.get()) == 0):
                            color_scheme = self.detect_colors(
                                self.parent.focus_get())
                            self.preview_scheme(color_scheme)

    def change_border_color(self, evt):
        evt.widget.config(bg='white', bd=2)        

    def unchange_border_color(self, evt):
        evt.widget.config(bg='lightgray', bd=1)

    def make_colors_table(self, colors):

        def clear_select(evt):
            evt.widget.selection_clear()

        l_col = [
            'background 1', 'background 2', 
            'background 3', 'font color']

        self.h1.grid(
            column=0, row=0, 
            sticky='ew', 
            ipady=3,
            pady=6)

        self.h2.grid(
            column=1, row=0, 
            sticky='ew', 
            ipady=3,
            pady=6)

        entries_combos = []
        j = 1
        for name in l_col:
            lab = Label(
                self.colors_table,
                anchor='w',
                text=name)
            lab.grid(column=0, row=j, sticky='ew', padx=(6,12), pady=3)
            ent = Entry(
                self.colors_table, width=12)
            self.r_col[name] = ent
            ent.grid(column=1, row=j, pady=3)
            entries_combos.append(ent)
            ent.bind('<FocusOut>', clear_select)
            ent.bind('<Double-Button-1>', self.open_color_chooser)
            j += 1

    def drop_scheme_from_db(self, frame, scheme):
        id = frame.split('_')[1]
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(delete_color_scheme, (id,))
        conn.commit()    
        cur.execute(select_color_scheme_current)
        current_scheme = cur.fetchone()

        if scheme == current_scheme:
            cur.execute(update_color_scheme_null)
            conn.commit()

        cur.close()
        conn.close()    

    def delete_sample(self, evt):
        dflt = self.colors_content.winfo_children()[0]
        drop_me = self.colors_content.focus_get()
        all_schemes_plus = get_color_schemes_plus()
        color_scheme = tuple(self.detect_colors(drop_me))
        all_schemes = []
        for scheme_plus in all_schemes_plus:
            all_schemes.append(scheme_plus[0:4])
        if color_scheme in all_schemes:
            idx = all_schemes.index(color_scheme)
            if all_schemes_plus[idx][4] == 1:
                drop_name = drop_me.winfo_name()
                self.drop_scheme_from_db(drop_name, color_scheme)

                drop_me.destroy()
                self.resize_color_samples_scrollbar()

                # reset to default scheme; only current scheme can be deleted
                dflt.focus_set()
                fix = []
                for child in self.parent.focus_get().winfo_children():
                    fix.append(child['bg']) 
                child = child
                fix.append(child['fg'])
                entries = []
                for child in self.colors_table.winfo_children():
                    if child.winfo_class() == 'TEntry':
                        entries.append(child)
                self.b6.invoke()

    def get_new_scheme(self):
        all_schemes = get_color_schemes()
        inputs = []
        for widg in self.colors_table.winfo_children():
            if widg.winfo_class() == 'TEntry':
                inputs.append(widg.get())
        inputs = tuple(inputs)
        for scheme in all_schemes:
            if inputs == scheme:
                return

        self.put_new_scheme_in_db(inputs)

    def put_new_scheme_in_db(self, new_scheme):
        all_schemes = get_color_schemes()
        if new_scheme not in all_schemes:

            conn = sqlite3.connect(current_file)
            conn.execute('PRAGMA foreign_keys = 1')
            cur = conn.cursor()
            cur.execute(insert_color_scheme, (new_scheme))
            conn.commit()
            cur.close()
            conn.close()

    def make_new_sample(self):

        # validate colors

        back = self.r_col['main background'].get()
        high = self.r_col['highlight background'].get()
        table = self.r_col['table head background'].get()
        fonts = self.r_col['font color'].get()    

        try_these = [
            (back, self.r_col['main background']), 
            (high, self.r_col['highlight background']), 
            (table, self.r_col['table head background']), 
            (fonts, self.r_col['font color'])]

        for tup in try_these:
            if len(tup[0]) == 0:
                return
        
        test_color = Frame(self.view) # don't grid this

        for tup in try_these:
            try:
                test_color.config(bg=tup[0])
            except tk.TclError:
                tup[1].delete(0, tk.END)
                messagebox.showerror(
                    'Color Not Recognized.',
                    'A color was entered that is unknown to the system.')
                return

        self.get_new_scheme()
        for child in self.colors_content.winfo_children():
            child.destroy()
        self.make_samples()

    def copy_scheme(self):

        colors = []
        if self.view.focus_get().master == self.colors_content:
            for child in self.view.focus_get().winfo_children():
                colors.append(child['bg'])
                child=child
            colors.append(child['fg'])

        color_entries = []
        for child in self.colors_table.winfo_children():
            if child.grid_info()['row'] == 0:
                pass
            elif child.grid_info()['column'] == 1:
                color_entries.append(child)

        place_colors = dict(zip(color_entries, colors))

        for k,v in place_colors.items():
            k.delete(0, 'end')
            k.insert(0, v)

    def open_color_chooser(self, evt):
        chosen_color = colorchooser.askcolor(parent=self.view)[1]
        if chosen_color:
            evt.widget.delete(0, 'end')
            evt.widget.insert(0, chosen_color)

# # custom_tabbed_widget.py

# from widgets import Framex, Frame, FrameHilited2, Label
# from styles import make_formats_dict
# from utes import create_tooltip
# from dev_tools import looky, seeline

# '''
    # This is a Frame that can be gridded anywhere. No scrollbar needed, because
    # tabbed widgets are meant to retain a fixed size and the space they are in
    # has a scrollbar of its own. The space they are in should not resize, so set
    # `minx` and `miny` to accomodate the tab with the biggest content.
# '''

# class TabBook(Framex):

    # def __init__(
            # self, master, root=None, side='nw', bd=0, tabwidth=12, 
            # selected='', tabs=[],  minx=0.90, 
            # miny=0.85, case='title', *args, **kwargs):
        # Framex.__init__(self, master, *args, **kwargs)
        # '''
            # The tab is the part that sticks out with the title 
            # you click to activate the page which holds that 
            # tab's content. To add widgets grid them with 
            # instance.store[page] as the master. For example: 
            # inst.store['place'] where 'place' is a string from 
            # the original tabs parameter (list of tuples containing
            # tab title and accelerator e.g.:
            # `[('images', 'I'), ('attributes', 'A')]`). The default
            # value of `selected` should not be an empty string since
            # a string here is not optional, it has to be the title
            # of one of the tabs, the one that is to be open by default. 
            # `minx` and `miny` are minimum sizes as proportions of the
            # screen size.
        # '''

        # self.master = master
        # self.side = side
        # self.bd = bd
        # self.tabwidth = tabwidth
        # self.selected = selected
        # self.minx = self.master.winfo_screenwidth() * minx
        # self.miny = self.master.winfo_screenheight() * miny
        # self.case = case

        # self.formats = make_formats_dict()
        
        # self.tabdict = {}
        # for tab in tabs:
            # self.tabdict[tab[0]] = [tab[1]]
            # # key is 'title', value is ['acceLerator']
            # # value will have page appended to it

        # self.store = {}

        # self.make_widgets() 
        # self.open_tab_alt(root)

    # def make_widgets(self):
        # '''  '''

        # self.tab_base = Frame(self)
        # self.border_base = FrameHilited2(self)
        # self.notebook = Frame(self.border_base)
        # self.tab_frame = FrameHilited2(self.tab_base)
        # self.tabless = Frame(self.tab_base)
        # self.spacer = Frame(self.tabless)
        # self.top_border = FrameHilited2(self.tabless, height=1)

        # self.grid_columnconfigure(1, weight=1)
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=1)

        # self.notebook.grid_columnconfigure(0, weight=1, minsize=self.minx)
        # self.notebook.grid_rowconfigure(0, weight=1, minsize=self.miny)

        # self.grid_tabs()  

        # c = 0
        # for tab in self.tabdict:
            # print("line", looky(seeline()).lineno, "tab:", tab)
            # lab = Label(
                # self.tab_frame,
                # width=int(self.tabwidth),
                # takefocus=1)  
            # if self.case == 'title':
                # lab.config(text=tab.title())   
            # elif self.case == 'lower':
                # lab.config(text=tab.lower())    
            # elif self.case == 'upper':
                # lab.config(text=tab.upper())     
            # self.tabdict[tab].append(lab)

            # if self.side in ('ne', 'nw'):
                # lab.grid(column=c, row=0, padx=1, pady=(1, 0))
            # elif self.side in ('se', 'sw'):
                # lab.grid(column=c, row=0, padx=1, pady=(0, 1))

            # lab.bind('<Button-1>', self.make_active)
            # lab.bind('<FocusIn>', self.highlight_tab)
            # lab.bind('<FocusOut>', self.unhighlight_tab)
            # lab.bind('<Key-space>', self.make_active)
            # lab.bind('<Key-Return>', self.make_active)
            # lab.bind('<ButtonRelease-1>', self.unhighlight_tab)
            # create_tooltip(lab, 'Alt + {}'.format(self.tabdict[tab][0]))
            # page = Frame(self.notebook)
            # page.grid(column=0, row=0, sticky='news')
            # page.grid_remove()
            # self.tabdict[tab].append(page)
            # self.store[tab] = page
            # c += 1
        # selected_page = self.tabdict[self.selected][2] # page
        # selected_page.grid()

        # self.active = self.tabdict[self.selected][1] # tab
        # self.make_active()

    # def grid_tabs(self):

        # if self.side in ('nw', 'ne'):
            # pady = (0, 1)
            # tab_row = 0
            # body_row = 1
            # spacer_row = 0
            # border_row = 1

        # elif self.side in ('sw', 'se'):
            # pady=(1, 0)
            # tab_row = 1
            # body_row = 0
            # spacer_row = 1
            # border_row = 0

        # if self.side in ('nw', 'sw'):
            # tab_col = 0
            # tabless_col = 1                

        # elif self.side in ('ne', 'se'):
            # tab_col = 1
            # tabless_col = 0                

        # # self.notebook switches pady
        # self.notebook.grid(column=0, row=0, padx=1, pady=pady, sticky='news')
        # # self.tab_base and borderbase switch rows
        # self.tab_base.grid(column=0, row=tab_row, sticky='news')
        # self.tab_base.grid_columnconfigure(tabless_col, weight=1)
        # self.tab_base.grid_rowconfigure(0, weight=1)
        # self.border_base.grid(column=0, row=body_row, sticky='news')
        # # self.tab_frame and self.tabless switch cols
        # self.tab_frame.grid(column=tab_col, row=0, sticky='ew')
        # self.tabless.grid(column=tabless_col, row=0, sticky='news')
        # self.tabless.grid_columnconfigure(0, weight=1)
        # self.tabless.grid_rowconfigure(spacer_row, weight=1)
        # # self.spacer and self.top_border switch rows
        # self.spacer.grid(column=0, row=tab_row, sticky='ns')
        # self.top_border.grid(column=0, row=border_row, sticky='ew') 

    # def highlight_tab(self, evt):
        # # accelerators don't work if notebook not visible
        # if evt.widget in self.store.values():
            # evt.widget.config(fg='yellow')

    # def unhighlight_tab(self, evt):
        # # accelerators don't work if notebook not visible
        # if evt.widget in self.store.values():
            # evt.widget.config(fg=self.formats['fg'])

    # def make_active(self, evt=None):
        # ''' Open the selected tab & reconfigure it to look open. '''

        # self.formats = make_formats_dict()

        # # position attributes are needed in the instance
        # self.posx = self.winfo_rootx()
        # self.posy = self.winfo_rooty()    

        # # if this method is not running on load
        # if evt:
            # self.active = evt.widget
            # self.active.focus_set()

            # # if evt was alt key accelerator
            # if (evt.widget is self.master or 
                    # evt.keysym not in ('space', 'Return')):

                # for k,v in self.tabdict.items():
                    # if evt.keysym in (v[0], v[0].lower()):
                        # self.active = v[1]
                        # self.active.focus_set()
                        
            # # if evt was spacebar, return key, or mouse button
            # elif evt.type in ('2', '4'):
                # self.active.config(fg=self.formats['fg'])

            # # remove all pages and regrid the right one
            # for k,v in self.tabdict.items():
                # if self.active == v[1]:
                    # for widg in self.tabdict.values():
                        # widg[2].grid_remove()
                    # v[2].grid()

        # # unhighlight all tabs
        # for tab in self.tabdict.values():
            # # if tab[1] is not self.active:
            # tab[1].config(
                # bg=self.formats['highlight_bg'],
                # font=self.formats['output_font'])

        

        # # highlight active tab
        # self.active.config(
            # bg=self.formats['bg'],
            # font=self.formats['heading3'])

        # # self.active.focus_set()



    # def open_tab_alt(self, root_window):
        # ''' Bindings for notebook tab accelerators. '''

        # for k,v in self.tabdict.items():
            # key_combo_upper = '<Alt-Key-{}>'.format(v[0])  
            # root_window.bind(key_combo_upper, self.make_active)
            # key_combo_lower = '<Alt-Key-{}>'.format(v[0].lower()) 
            # root_window.bind(key_combo_lower, self.make_active)

            # unkey_combo_upper = '<Alt-KeyRelease-{}>'.format(v[0])            
            # root_window.bind_all(unkey_combo_upper, self.unhighlight_tab)
            # unkey_combo_lower = '<Alt-KeyRelease-{}>'.format(v[0].lower()) 
            # root_window.bind_all(unkey_combo_lower, self.unhighlight_tab)

