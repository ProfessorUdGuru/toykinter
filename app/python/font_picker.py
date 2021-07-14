# font_picker.py

import tkinter as tk
from tkinter import ttk, font
import sqlite3
from files import current_file
from query_strings import update_format_fonts, select_font_scheme
from widgets import Label, Frame, Scale, Entry, Button
from styles import make_formats_dict, config_generic
from custom_combobox_widget import Combobox
from dev_tools import looky, seeline



formats = make_formats_dict()

class FontPicker(Frame):
    def __init__(self, master, view, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master
        self.view = view
        self.all_fonts = font.families()

        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_font_scheme)
        font_scheme = cur.fetchall()
        cur.close()
        conn.close()
        self.font_scheme = list(font_scheme[0])
        self.make_widgets()

    def make_widgets(self):

        def combobox_selected(combo):
            '''
                The reason this function is nested is that I have no experience 
                with overriding methods. When I tried to add `self` as the first 
                parameter, there was an error and I didn't know what to do. I 
                nested it so I wouldn't have to use `self`.
            '''
            if combo == self.combos["input_font_chooser"]:
                input_sample.config(
                    font=(self.all_fonts[combo.current], self.fontSize))
            elif combo == self.combos["output_font_chooser"]:
                output_sample.config(
                    font=(self.all_fonts[combo.current], self.fontSize))
            else:
                print("case not handled")
            # update_idletasks() speeds up the redrawing of the app with new font
            self.update_idletasks()  

        sample_text = ["Sample", "Text ABCDEFGHxyz 0123456789 iIl1 o0O"]

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        sample = Frame(self)

        output_sample = Label(
            sample,
            text=" Output ".join(sample_text))

        input_sample = Entry(sample, width=50)
        input_sample.insert(0, " Input ".join(sample_text))

        self.fontSizeVar = tk.IntVar()
        self.fontSize = self.font_scheme[0]

        font_size = Scale(
            self,
            from_=8.0,
            to=26.0,
            tickinterval=6.0,
            label="TEXT SIZE",
            orient="horizontal",
            length=200,
            variable=self.fontSizeVar,
            command=self.show_font_size)

        font_size.set(self.fontSize)

        combo_names = ["output_font_chooser", "input_font_chooser"]
        self.combos = {}

        j = 2
        for name in combo_names:
            cbo = Combobox(
                self, self.view, values=self.all_fonts, 
                height=300, scrollbar_size=12)
            self.combos[name] = cbo
            name = name.replace("_", " ").upper()
            lab = Label(
                self,
                text=name)
            lab.grid(column=0, row=j, pady=(24,6))
            cbo.grid(column=0, row=j+1, pady=(6, 24))
            j += 2

        apply = Button(
            self,
            text="APPLY",
            command=self.apply)

        sample.grid(column=0, row=0)
        output_sample.grid(padx=24, pady=24)
        input_sample.grid(padx=24, pady=24)
        font_size.grid(column=0, row=1, pady=24)
        apply.grid(column=0, row=7, sticky="e", padx=(0,24), pady=(0,24))

        Combobox.combobox_selected = combobox_selected

    def apply(self):
        self.font_scheme[0] = self.fontSizeVar.get()
        if len(self.combos["output_font_chooser"].get()) != 0:
            self.font_scheme[1] = self.combos["output_font_chooser"].get()
        if len(self.combos["input_font_chooser"].get()) != 0:
            self.font_scheme[2] = self.combos["input_font_chooser"].get()
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_format_fonts, tuple(self.font_scheme))
        conn.commit()
        cur.close()
        conn.close()

        config_generic(self.view)

    def show_font_size(self, evt):
        self.fontSize = self.fontSizeVar.get()

if __name__ == "__main__": 

    root = tk.Tk()

    t = FontPicker(root, root)
    t.grid()

    q = Label(root, text="This text represents everything outside of the "
        "font picker.\n It doesn't change until you click the APPLY button.")
    q.grid(padx=24, pady=48)

    config_generic(root)

    root.mainloop()