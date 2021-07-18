# main.py

import tkinter as tk
from widgets import (
    Frame, LabelH1, LabelH2, LabelH3, LabelH4, Label, Message, Canvas, Text, 
    EntryAutofillHilited, Separator, LabelMovable, LabelStylable, LabelItalic)
from window_border import Border
from scrolling import Scrollbar    
from custom_tabbed_widget import TabBook
from font_picker import FontPicker
from colorizer import Colorizer
from dev_user_docs import (
    intro_head, intro_docs, dev_docs, autofill_docs, morewidg_docs, italics)
from dev_tools import looky, seeline



class Main(Frame):
    def __init__(self, master, view, treebard, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        '''
            `master` is an instance of `Border` which is an instance of 
            `Canvas`. `self` is the content window.
        '''

        self.canvas = master 
        self.view = view
        self.treebard = treebard
        self.make_widgets()
        self.populate_tabbook() 
        self.make_scrollbars_docs()
        self.make_font_picker()
        self.make_colorizer()

    def make_scrollbars_main(self):

        self.vsb = Scrollbar(
            self.view, 
            hideable=True, 
            command=self.canvas.yview,
            width=20)
        self.hsb = Scrollbar(
            self.view, 
            hideable=True, 
            width=20, 
            orient='horizontal',
            command=self.canvas.xview)
        self.canvas.config(
            xscrollcommand=self.hsb.set, 
            yscrollcommand=self.vsb.set)
        self.vsb.grid(column=2, row=4, sticky='ns')
        self.hsb.grid(column=1, row=5, sticky='ew')

    def make_widgets(self):

        self.make_scrollbars_main()

        scridth = 20
        scridth_n = Frame(self, height=scridth)
        scridth_w = Frame(self, width=scridth)

        self.notebook = TabBook(
            self,
            root=self.view, 
            tabs=[
                ("toykinter", "T"), ("autofill", "A"), 
                ("docs", "D"), ("more widgets", "M"), ("settings", "S")],
            side="nw",
            tabwidth=16,
            case="upper", 
            selected="toykinter",
            minx=0.66, 
            miny=0.66)
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
        self.populate_tab0()
        self.populate_tab1()
        self.populate_tab3()

    def populate_tab0(self):

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

    def populate_tab1(self):

        tab1 = self.notebook.store['autofill']
        tab1.columnconfigure(0, weight=1)
        tab1.rowconfigure(1, weight=1)

        content1 = Frame(tab1)
        content1.columnconfigure(0, weight=1)
        content1.rowconfigure(0, weight=1)
        content1.grid(column=0, row=0, sticky="news")
        
        head1 = LabelH3(content1, text="Simple Toykinter Autofill Entry")
        head1.grid(column=0, row=0, pady=18)

        entry = EntryAutofillHilited(content1, width=50)
        entry.grid(column=0, row=1)
        entry.autofill = True
        entry.config(textvariable=entry.var)

        text1 = Message(content1, text=autofill_docs, width=1000)
        text1.grid(column=0, row=2, sticky="news")

    def populate_tab3(self):

        tab3 = self.notebook.store['more widgets']
        tab3.columnconfigure(0, weight=1)
        tab3.rowconfigure(4, weight=1)
        head3 = LabelH3(tab3, text="More Toykinter Widgets")
        sep1 = Separator(tab3)
        text3 = Message(tab3, text=morewidg_docs, width=1000)
        sep2 = Separator(tab3, height=5)
        widgets = Frame(tab3)
        txt = Text(widgets, width=36, height=4)
        txt.insert(
            0.1, 
            "This Text widget changes fonts and colors instantly and has "
            "all the same options as a tkinter.Text widget, from which it "
            "inherits everything.")
        labf = Frame(widgets)
        h1 = LabelH1(labf, text='This Label is heading_1')
        h2 = LabelH2(labf, text='This Label is heading_2')
        h3 = LabelH3(labf, text='This Label is heading_3')
        h4 = LabelH4(labf, text='This Label is heading_4')

        movables = "You can move these labels around with the arrow keys. First just Tab or Shift+Tab into the one you want to move."
        split = movables.split()

        mover = Frame(widgets)
        for i in range(len(split)):
            mov = LabelMovable(mover, text=split[i])
            mov.grid(column=i, row=0, padx=1)

        stylin = LabelStylable(widgets, width=75)
        stylin.insert("end", "This label is copiable and ", "italic") 
        stylin.insert("end", "can also use a ") 
        stylin.insert("end", "variety of font stylings.", "bold")

        head3.grid(column=0, row=0, pady=18)
        sep1.grid(column=0, row=1, sticky='ew')
        text3.grid(column=0, row=2, sticky="news")
        sep2.grid(column=0, row=3, sticky='ew')

        widgets.grid(column=0, row=4, sticky='news')
        txt.grid(column=0, row=0, padx=9)
        labf.grid(column=1, row=0, padx=9, pady=9, sticky='news')
        h1.grid(column=0, row=0, sticky='ew')
        h2.grid(column=0, row=1, sticky='ew')
        h3.grid(column=0, row=2, sticky='ew')
        h4.grid(column=0, row=3, sticky='ew')
        mover.grid(column=0, row=1, sticky='news', columnspan=2, padx=9, pady=9)
        stylin.grid(column=0, row=2, columnspan=2)

        bottom = LabelItalic(
            widgets, 
            text=italics, 
            # wraplength=500, 
            justify='left', 
            anchor='w')
        bottom.grid(column=0, row=3, columnspan=2, pady=9)

    def make_scrollbars_toyk(self):

        toyk = self.notebook.store["toykinter"]

        self.canvas_toyk = Canvas(toyk)

        scridth = 16
        scridth_n = Frame(toyk, height=scridth)
        scridth_w = Frame(toyk, width=scridth)
        self.content_toyk = Frame(self.canvas_toyk)

        head0 = LabelH3(self.content_toyk, text=intro_head)
        text0 = Message(self.content_toyk, text=intro_docs, width=1000)

        vsb_toyk = Scrollbar(
            toyk, 
            hideable=False, 
            command=self.canvas_toyk.yview,
            width=16)
        hsb_toyk = Scrollbar(
            toyk, 
            hideable=True, 
            width=16, 
            orient='horizontal',
            command=self.canvas_toyk.xview)
        self.canvas_toyk.config(
            xscrollcommand=hsb_toyk.set, 
            yscrollcommand=vsb_toyk.set)

        self.canvas_toyk.grid(column=1, row=1, sticky="news")

        # children of toyk
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        toyk.columnconfigure(1, weight=1)
        toyk.rowconfigure(1, weight=1)

        vsb_toyk.grid(column=2, row=1, sticky='ns')
        hsb_toyk.grid(column=1, row=2, sticky='ew')

        self.content_toyk.columnconfigure(0, weight=1)
        self.content_toyk.rowconfigure(0, weight=1)
        # message.grid(column=0, row=0, padx=24, sticky="news")

        head0.grid(column=0, row=0)
        text0.grid(column=0, row=1, sticky="news")

        self.canvas_toyk.create_window(
            0, 0, anchor='nw', window=self.content_toyk)
        self.view.update_idletasks()
        self.canvas_toyk.configure(scrollregion=self.canvas_toyk.bbox("all"))

    def make_scrollbars_docs(self):

        docs = self.notebook.store["docs"]

        self.canvas_docs = Canvas(docs)

        scridth = 16
        scridth_n = Frame(docs, height=scridth)
        scridth_w = Frame(docs, width=scridth)
        self.content_docs = Frame(self.canvas_docs)
        
        message = Message(self.content_docs, text=dev_docs, width=1000)
        vsb_docs = Scrollbar(
            docs, 
            hideable=False, 
            command=self.canvas_docs.yview,
            width=16)
        hsb_docs = Scrollbar(
            docs, 
            hideable=True, 
            width=16, 
            orient='horizontal',
            command=self.canvas_docs.xview)
        self.canvas_docs.config(
            xscrollcommand=hsb_docs.set, 
            yscrollcommand=vsb_docs.set)

        self.canvas_docs.grid(column=1, row=1, sticky="news")

        # children of docs
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        docs.columnconfigure(1, weight=1)
        docs.rowconfigure(1, weight=1)

        vsb_docs.grid(column=2, row=1, sticky='ns')
        hsb_docs.grid(column=1, row=2, sticky='ew')

        self.content_docs.columnconfigure(0, weight=1)
        self.content_docs.rowconfigure(0, weight=1)
        message.grid(column=0, row=0, padx=24, sticky="news")
        self.canvas_docs.create_window(0, 0, anchor='nw', window=self.content_docs)
        self.view.update_idletasks()
        self.canvas_docs.configure(scrollregion=self.canvas_docs.bbox("all"))

    def make_font_picker(self):
        tab3_1 = self.prefsbook.store["fonts"]
        tab3_1.columnconfigure(0, weight=1)
        tab3_1.rowconfigure(0, weight=1)
        font_picker = FontPicker(tab3_1, self)
        font_picker.grid(column=0, row=0, sticky="news")

    def make_colorizer(self):
        color_schemer = Colorizer(
            self.prefsbook.store["colors"], 
            self.prefsbook,
            self.view)
        color_schemer.grid(column=0, row=0, sticky="news")

