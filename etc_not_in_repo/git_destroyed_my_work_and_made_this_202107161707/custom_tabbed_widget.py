# custom_tabbed_widget.py

from widgets import Framex, Frame, FrameHilited2, Labelx
from styles import make_formats_dict, config_generic
from utes import create_tooltip
from dev_tools import looky, seeline

'''
    This is a Frame that can be gridded anywhere. No scrollbar needed, because
    tabbed widgets are meant to retain a fixed size and the space they are in
    has a scrollbar of its own. The space they are in should not resize, so set
    `minx` and `miny` to accomodate the tab with the biggest content.
'''

class LabelTab(Labelx):
    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)
    
        self.formats = make_formats_dict()
        self.chosen = False

        if self.chosen is False:
            self.config(bg=self.formats['bg'], fg=self.formats['fg'])
        else: 
            self.config(bg=self.formats['highlight_bg'])
            


class TabBook(Framex):

    def __init__(
            self, master, root=None, side='nw', bd=0, tabwidth=12, 
            selected='', tabs=[],  minx=0.90, 
            miny=0.85, case='title', *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        '''
            The tab is the part that sticks out with the title 
            you click to activate the page which holds that 
            tab's content. To add widgets grid them with 
            instance.store[page] as the master. For example: 
            inst.store['place'] where 'place' is a string from 
            the original tabs parameter (list of tuples containing
            tab title and accelerator e.g.:
            `[('images', 'I'), ('attributes', 'A')]`). The default
            value of `selected` should not be an empty string since
            a string here is not optional, it has to be the title
            of one of the tabs, the one that is to be open by default. 
            `minx` and `miny` are minimum sizes as proportions of the
            screen size.
        '''

        self.master = master
        self.side = side
        self.bd = bd
        self.tabwidth = tabwidth
        self.selected = selected
        self.minx = self.master.winfo_screenwidth() * minx
        self.miny = self.master.winfo_screenheight() * miny
        self.case = case

        self.formats = make_formats_dict()
        
        self.tabdict = {}
        for tab in tabs:
            self.tabdict[tab[0]] = [tab[1]]

        self.store = {}
        
        self.active = None
        self.make_widgets() 
        self.open_tab_alt(root)

    def make_widgets(self):

        self.tab_base = Frame(self)
        self.border_base = FrameHilited2(self)
        self.notebook = Frame(self.border_base)
        self.tab_frame = FrameHilited2(self.tab_base)
        self.tabless = Frame(self.tab_base)
        self.spacer = Frame(self.tabless)
        self.top_border = FrameHilited2(self.tabless, height=1)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.notebook.grid_columnconfigure(0, weight=1, minsize=self.minx)
        self.notebook.grid_rowconfigure(0, weight=1, minsize=self.miny)

        self.grid_tabs()  

        c = 0
        for tab in self.tabdict:
            lab = LabelTab(
                self.tab_frame,
                width=int(self.tabwidth),
                takefocus=1)  
            if c == 0:
                lab.chosen = True
            if self.case == 'title':
                lab.config(text=tab.title())   
            elif self.case == 'lower':
                lab.config(text=tab.lower())    
            elif self.case == 'upper':
                lab.config(text=tab.upper())     
            self.tabdict[tab].append(lab)

            if self.side in ('ne', 'nw'):
                lab.grid(column=c, row=0, padx=1, pady=(1, 0))
            elif self.side in ('se', 'sw'):
                lab.grid(column=c, row=0, padx=1, pady=(0, 1))

            lab.bind('<Button-1>', self.make_active)
            lab.bind('<FocusIn>', self.highlight_tab)
            lab.bind('<FocusOut>', self.unhighlight_tab)
            lab.bind('<Key-space>', self.make_active)
            lab.bind('<Key-Return>', self.make_active)
            lab.bind('<ButtonRelease-1>', self.unhighlight_tab)
            create_tooltip(lab, 'Alt + {}'.format(self.tabdict[tab][0]))
            page = Frame(self.notebook)
            page.grid(column=0, row=0, sticky='news')
            page.grid_remove()
            self.tabdict[tab].append(page)
            self.store[tab] = page
            c += 1

        selected_page = self.tabdict[self.selected][2] # page
        selected_page.grid()

        self.active = self.tabdict[self.selected][1] # tab
        self.make_active()

    def grid_tabs(self):

        if self.side in ('nw', 'ne'):
            pady = (0, 1)
            tab_row = 0
            body_row = 1
            spacer_row = 0
            border_row = 1

        elif self.side in ('sw', 'se'):
            pady=(1, 0)
            tab_row = 1
            body_row = 0
            spacer_row = 1
            border_row = 0

        if self.side in ('nw', 'sw'):
            tab_col = 0
            tabless_col = 1                

        elif self.side in ('ne', 'se'):
            tab_col = 1
            tabless_col = 0                

        # self.notebook switches pady
        self.notebook.grid(column=0, row=0, padx=1, pady=pady, sticky='news')
        # self.tab_base and borderbase switch rows
        self.tab_base.grid(column=0, row=tab_row, sticky='news')
        self.tab_base.grid_columnconfigure(tabless_col, weight=1)
        self.tab_base.grid_rowconfigure(0, weight=1)
        self.border_base.grid(column=0, row=body_row, sticky='news')
        # self.tab_frame and self.tabless switch cols
        self.tab_frame.grid(column=tab_col, row=0, sticky='ew')
        self.tabless.grid(column=tabless_col, row=0, sticky='news')
        self.tabless.grid_columnconfigure(0, weight=1)
        self.tabless.grid_rowconfigure(spacer_row, weight=1)
        # self.spacer and self.top_border switch rows
        self.spacer.grid(column=0, row=tab_row, sticky='ns')
        self.top_border.grid(column=0, row=border_row, sticky='ew') 

    def highlight_tab(self, evt):
        # accelerators don't work if notebook not visible
        if evt.widget in self.store.values():
            evt.widget.config(fg='yellow')

    def unhighlight_tab(self, evt):
        # accelerators don't work if notebook not visible
        if evt.widget in self.store.values():
            evt.widget.config(fg=self.formats['fg'])

    def make_active(self, evt=None):
        ''' Open the selected tab & reconfigure it to look open. '''

        self.formats= make_formats_dict()

        # position attributes are needed in the instance
        self.posx = self.winfo_rootx()
        self.posy = self.winfo_rooty()    

        # if this method is not running on load
        if evt:
            self.active = evt.widget
            self.active.focus_set()

            # if evt was alt key accelerator
            if (evt.widget is self.master or 
                    evt.keysym not in ('space', 'Return')):

                for k,v in self.tabdict.items():
                    if evt.keysym in (v[0], v[0].lower()):
                        self.active = v[1]
                        self.active.focus_set()
                        
            # if evt was spacebar, return key, or mouse button
            elif evt.type in ('2', '4'):
                self.active.config(fg=formats['fg'])

            # remove all pages and regrid the right one
            for k,v in self.tabdict.items():
                if self.active == v[1]:
                    for widg in self.tabdict.values():
                        widg[2].grid_remove()
                    v[2].grid()
        
        # unhighlight all tabs
        for tab in self.tabdict.values():
            tab[1].config(
                bg=self.formats['highlight_bg'],
                font=self.formats['output_font'])


        # detect which tab is active and set its tab.chosen attribute to True
        #   so config_generic will give it the right background color when
        #   color_scheme is changed
        for tab in self.tabdict.values():
            if tab[1] == self.active:
                tab[1].chosen = True
            else:
                tab[1].chosen = False

        # highlight active tab; doesn't work on load due to config_generic()
        #   but does work on user-initiated events
        self.active.config(
            bg=self.formats['bg'],
            font=self.formats['heading3'])

    def open_tab_alt(self, root_window):
        ''' Bindings for notebook tab accelerators. '''

        for k,v in self.tabdict.items():
            key_combo_upper = '<Alt-Key-{}>'.format(v[0])  
            root_window.bind(key_combo_upper, self.make_active)
            key_combo_lower = '<Alt-Key-{}>'.format(v[0].lower()) 
            root_window.bind(key_combo_lower, self.make_active)

            unkey_combo_upper = '<Alt-KeyRelease-{}>'.format(v[0])            
            root_window.bind_all(unkey_combo_upper, self.unhighlight_tab)
            unkey_combo_lower = '<Alt-KeyRelease-{}>'.format(v[0].lower()) 
            root_window.bind_all(unkey_combo_lower, self.unhighlight_tab)

if __name__ == '__main__':

    import tkinter as tk
    from widgets import LabelStay, Label

    formats = make_formats_dict()

    root = tk.Tk()
    root.config(bg=formats['bg'])

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    titles = [
        ('person', 'P'), ('place', 'L'), ('source', 'S'), 
        ('reports', 'R'), ('charts', 'C'), ('graphics', 'G'), 
        ('projects', 'J'), ('preferences', 'F')]

    tab_book = TabBook(
        root,
        root=root,
        tabwidth=12,
        selected='place', 
        case='title',
        side='se',
        minx=0.57,
        miny=0.45,
        tabs=titles)
    tab_book.grid(column=0, row=0, padx=48, pady=48, sticky='news')

    # put stuff in pages with a loop...
    for k,v in tab_book.store.items():
        l = LabelStay(v, text=k+k, font=('arial', 75))
        l.grid(column=0, row=0, pady=100, sticky='ew')
    # ...or one at a time.
    ll = Label(
        tab_book.store['person'],
        text='say hello to non-ttk notebook')
    ll.grid(column=0, row=1)
    mm = Label(
         tab_book.store['place'],
        text='say goodbye to ttk.Notebook')
    mm.grid(column=0, row=1)

    config_generic(root)

    root.mainloop()