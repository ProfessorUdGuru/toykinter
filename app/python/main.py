# main.py

import tkinter as tk
from widgets import Frame, LabelH3, Label, Message, Canvas, Text, EntryAutofillHilited
from window_border import Border
from scrolling import Scrollbar    
from custom_tabbed_widget import TabBook
from font_picker import FontPicker
from colorizer import Colorizer
from dev_user_docs import intro_head, intro_docs, dev_docs, autofill_docs
from dev_tools import looky, seeline



# tabbed_widgets = {}

class Main(Frame):
    def __init__(self, master, view, treebard, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master # the main canvas (instance of Border class)
        self.view = view
        self.treebard = treebard
        self.make_widgets()
        self.populate_tabbook()
        self.make_scrollbars_docs()
        self.make_font_picker()
        self.make_colorizer()

    def make_scrollbars(self):

        self.vsb = Scrollbar(
            self.view, 
            hideable=True, 
            command=self.master.yview,
            width=20)
        self.hsb = Scrollbar(
            self.view, 
            hideable=True, 
            width=20, 
            orient='horizontal',
            command=self.master.xview)
        self.master.config(
            xscrollcommand=self.hsb.set, 
            yscrollcommand=self.vsb.set)
        self.vsb.grid(column=2, row=4, sticky='ns')
        self.hsb.grid(column=1, row=5, sticky='ew')

    def make_widgets(self):

        self.make_scrollbars()

        scridth = 20
        scridth_n = Frame(self, height=scridth)
        scridth_w = Frame(self, width=scridth)

        self.notebook = TabBook(
            self,
            root=self.view, 
            tabs=[("toykinter", "T"), ("autofill", "A"), ("docs", "D"), ("settings", "S")],
            side="nw",
            case="upper", 
            selected="toykinter",
            minx=0.66, 
            miny=0.66)
        print("line", looky(seeline()).lineno, "self.notebook:", self.notebook)
        prefs = self.notebook.store['settings']

        self.prefsbook = TabBook(
            prefs,
            root=self.view,
            tabs=[("colors", "C"), ("fonts", "F")],
            side="se",
            case="upper",
            selected="colors",
            minx=0.55,
            miny=0.55)
        prefs.columnconfigure(0, weight=1)
        prefs.rowconfigure(0, weight=1)
        self.prefsbook.grid(column=0, row=0)

        # children of self
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.notebook.grid(column=1, row=2)

    def populate_tabbook(self):

        toykinter = self.notebook.store['toykinter']
        toykinter.columnconfigure(0, weight=1)
        toykinter.rowconfigure(1, weight=1)

        content0 = Frame(toykinter)
        content0.columnconfigure(0, weight=1)
        content0.rowconfigure(0, weight=1)
        content0.grid(column=0, row=0, sticky="news")

        head0 = LabelH3(content0, text=intro_head)
        head0.grid(column=0, row=0)

        text0 = Message(content0, text=intro_docs, width=1000)
        text0.grid(column=0, row=1, sticky="news")

        tab1 = self.notebook.store['autofill']
        tab1.columnconfigure(0, weight=1)
        tab1.rowconfigure(1, weight=1)

        content1 = Frame(tab1)
        content1.columnconfigure(0, weight=1)
        content1.rowconfigure(0, weight=1)
        content1.grid(column=0, row=0, sticky="news")
        
        head1 = LabelH3(content1, text="Simple Toykinter Autofill Entry")
        head1.grid(column=0, row=0, pady=24)

        entry = EntryAutofillHilited(content1, width=50)
        entry.grid(column=0, row=1)
        entry.autofill = True
        entry.config(textvariable=entry.var)

        text1 = Message(content1, text=autofill_docs, width=1000)
        text1.grid(column=0, row=2, sticky="news")

    def make_scrollbars_docs(self):

        docs = self.notebook.store["docs"]

        canvas = Canvas(docs)

        scridth = 16
        scridth_n = Frame(docs, height=scridth)
        scridth_w = Frame(docs, width=scridth)
        content = Frame(canvas)
        
        message = Message(content, text=dev_docs, width=1000)
        vsb_docs = Scrollbar(
            docs, 
            hideable=False, 
            command=canvas.yview,
            width=16)
        hsb_docs = Scrollbar(
            docs, 
            hideable=True, 
            width=16, 
            orient='horizontal',
            command=canvas.xview)
        canvas.config(
            xscrollcommand=hsb_docs.set, 
            yscrollcommand=vsb_docs.set)


        canvas.grid(column=1, row=1, sticky="news")

        # children of docs
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        docs.columnconfigure(1, weight=1)
        docs.rowconfigure(1, weight=1)


        vsb_docs.grid(column=2, row=1, sticky='ns')
        hsb_docs.grid(column=1, row=2, sticky='ew')

        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)
        message.grid(column=0, row=0, padx=24, sticky="news")
        canvas.create_window(0, 0, anchor='nw', window=content)
        self.view.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def make_font_picker(self):
        tab3_1 = self.prefsbook.store["fonts"]
        tab3_1.columnconfigure(0, weight=1)
        tab3_1.rowconfigure(0, weight=1)
        font_picker = FontPicker(tab3_1, self.view)
        font_picker.grid(column=0, row=0, sticky="news")

    def make_colorizer(self):
        color_schemer = Colorizer(
            self.prefsbook.store["colors"], 
            self.prefsbook,
            self.view)
        color_schemer.grid(column=0, row=0, sticky="news")