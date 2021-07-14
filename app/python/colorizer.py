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
    update_color_scheme_null, insert_color_scheme)
from dev_tools import looky, seeline

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
            if widg.winfo_class() == 'Entry':
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
            elif widg.winfo_class() == 'Entry':
                widg.config(bg=scheme[1]),
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

        # if TRY button
        else:
            print("line", looky(seeline()).lineno, "self.colors_content.focus_get().winfo_class():", self.colors_content.focus_get().winfo_class())
            for widg in self.colors_table.winfo_children():

                # if entries not all filled out
                if (widg.winfo_class() == 'Entry' and
                    len(widg.get()) == 0): # prob. shd be break or continue
                        pass

                # if new scheme to try
                if (widg.winfo_class() == 'Entry' and
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
                elif (widg.winfo_class() == 'Entry' and
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
            ent = Entry(self.colors_table, width=12)
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
                    if child.winfo_class() == 'Entry':
                        entries.append(child)
                self.b6.invoke()

    def get_new_scheme(self):
        all_schemes = get_color_schemes()
        inputs = []
        for widg in self.colors_table.winfo_children():
            if widg.winfo_class() == 'Entry':
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



