# custom_listbox_widget.py

import tkinter as tk
from widgets import (
    Canvas, FrameHilited4, CanvasHilited, 
    FrameHilited3, LabelHilited, Frame, Text, Button, Entry)
from scrolling import Scrollbar
from styles import make_formats_dict, config_generic
from utes import create_tooltip
import dev_tools as dt



formats = make_formats_dict()

class Listbox(FrameHilited4):
    '''
        Tkinter Listbox and Text widget don't interact well. I 
        don't know why. When using a Tkinter Listbox to select 
        among subtopics for displaying notes in a Text widget, 
        it works but then to select text in the text widget you 
        have to click several times. For example, the first 
        double-click (meant to select a word) sends the cursor to 
        the end of the text. This happens with the code stripped 
        all the way down till there's nothing left but a tk.Listbox 
        and a tk.Text. This class replaces the tk.Listbox for a Text
        widget that selects a single note display topic from a list.

        The scrollbar has some redundant features since you can arrow 
        through the list and if list item doesn't fit horizontally, a
        tooltip tells the user what the hidden text says. So a scrollbar
        is still needed because, if the list is long, and scrollbar=False,
        there's no scrollbar slider to tell how long the list is. But 
        if you use the auto-hiding scrollbar AutoScrollbar instead of
        tk.Scrollbar, scrollbar=False has no effect (the scrollbar
        is there if needed and not there if not needed). But to get rid 
        of the horizontal scrollbar, I've decided to use the autohiding 
        scrollbar for the vertical scrollbar only and use tk.Scrollbar 
        for the horizontal scrollbar so I can use scrollbar=False to turn 
        it off. Kinda silly features roulette but not ready to slash out
        extraneous code till I've used this in practice and tested it more.

        Currently this only lets you select one listbox item at a time, but
        in other ways it's at least as practical as the tkinter Listbox.
    '''

    def __init__(
            self, 
            master, 
            items, 
            view_height=400, 
            view_width=150,
            scrollbar=False, 
            *args, **kwargs):
        FrameHilited4.__init__(self, master, *args, **kwargs)

        self.master = master
        self.items = items       
        self.view_height = view_height
        self.view_width = view_width
        self.scrollbar = scrollbar

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        self.config(takefocus=1, bd=2)
        self.bind('<FocusIn>', self.expand_on_focus)
        self.bind('<FocusOut>', self.shrink_on_unfocus)
        self.bind('<KeyPress>', self.highlight_first_last)        

        self.old_row = 0
        self.valuate = False

        self.make_widgets()
        self.list_height = self.listbox_content.winfo_reqheight()

    def make_widgets(self):

        self.listbox_canvas = CanvasHilited(
            self, 
            width=self.view_width, 
            height=self.view_height)
        xsb = tk.Scrollbar(
            self,
            width=16, 
            orient="horizontal", 
            command=self.listbox_canvas.xview)
        self.ysb = Scrollbar(
            self, 
            width=16,
            orient="vertical", 
            hideable=True,
            command=self.listbox_canvas.yview)
        self.listbox_canvas.configure(
            yscrollcommand=self.ysb.set, xscrollcommand=xsb.set)
        self.listbox_canvas.configure(scrollregion=(0,0,300,1500))

        xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        xsb.grid_remove()
        self.ysb.grid_remove()
        if self.scrollbar is True:
            xsb.grid()
            self.ysb.grid()

        self.listbox_canvas.grid(column=0, row=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.listbox_content = FrameHilited3(self.listbox_canvas)
        self.listbox_content.grid_columnconfigure(0, weight=1, minsize=self.view_width)
        # Currently there can be no other event callbacks
        #   triggered by FocusIn or this virtual event won't work.
        self.listbox_content.event_add('<<ListboxSelected>>', '<FocusIn>')

        self.make_listbox_content()

        self.listbox_canvas.create_window(
            0, 0, anchor='nw', window=self.listbox_content)
        self.resize_scrollbar()

    def make_listbox_content(self):

        def place_entry(evt):

            def destroy_entry(evt):
                
                self.new_subtopic_name = textvars[clicked].get()
                if self.valuate is False:
                    print('128 running')
                    rename_input.destroy()
                    return
                elif(len(self.new_subtopic_name) == 0 or 
                        self.new_subtopic_name == old_subtopic_name):
                    print('133 running')
                    pass                   
                elif self.new_subtopic_name != old_subtopic_name:
                    print('136 running')
                    self.store_new_subtopic_name()
                self.valuate = False
                rename_input.destroy()        

            clicked = evt.widget
            old_subtopic_name = textvars[clicked].get()
            self.valuate = True

            rename_input = Entry(clicked, textvariable=textvars[clicked])
            rename_input.place(x=0, y=0, anchor='nw', relwidth=1.0, relheight=1.0)
            rename_input.focus_set() 
            rename_input.select_range(0, 'end')

            rename_input.bind('<FocusOut>', destroy_entry)

        for child in self.listbox_content.winfo_children():
            child.destroy()

        textvars = {}
        g = 0
        for item in self.items:
            var = tk.StringVar()
            var.set(item)
            lab = LabelHilited(
                self.listbox_content,
                anchor='w', 
                takefocus=0,
                textvariable=var)
            lab.grid(column=0, row=g, sticky='ew', padx=3)
            lab.bind('<FocusOut>', self.unhighlight)
            lab.bind('<Button-1>', self.select_item)
            lab.bind('<Tab>', self.unfocus_listbox)
            lab.bind('<KeyPress>', self.traverse_on_arrow)
            lab.bind('<Double-Button-1>', place_entry)
            lab.bind('<Control-Button-1>', self.on_ctrl_click)
            lab.bind('<Key-Delete>', self.on_delete_key)
            textvars[lab] = var
            if lab.winfo_reqwidth() > self.view_width:
                create_tooltip(lab, item)
            g += 1
        h = g

    def store_new_subtopic_name(self):
        print('174 self.new_subtopic_name is', self.new_subtopic_name)

    def on_ctrl_click(self, evt):
        print('182 evt.widget is', evt.widget)
        self.pass_ctrl_click()

    def pass_ctrl_click(self):
        '''
            Overridden function if that's what it's called, if I'm right
            the reason this is a 2-step process is that on_ctrl_click
            has a Tkinter event to deal with while this 2nd part does not.
        '''
        print('pass evt to another function in the instance that wants to use the Control-Click event (this should not print)')

    def on_delete_key(self, evt):
        print('187 delete key pressed')
        self.pass_delete_key()

    def pass_delete_key(self):
        print('pass evt to another function in the instance that wants to use the Key-Delete event (this should not print)')

    def get(self, idx):
        if idx is not None:
            items = self.listbox_content.winfo_children()
            got = items[idx].cget('text')
            return got

    def delete(self, idx):
        if idx is not None:
            items = self.items
            del items[idx]
            self.items = items
            self.make_listbox_content()

    def selection_set(self, idx):
        if idx is not None:
            items = self.listbox_content.winfo_children()
            items[idx].config(bg=formats['bg'])

    def selection_clear(self):
        for child in self.listbox_content.winfo_children():
            child.config(bg=formats['highlight_bg'])

    def size(self):
        items_qty = len(self.items)
        return items_qty

    def insert(self, idx, stg):
        '''
            Create a new listbox item (stg) and insert it 
            into the list of items at the index referenced
            by before_idx.
        '''
        if idx is not None:
            items = self.items
            new_item = stg
            items.insert(idx, new_item)
            self.items = items
            self.make_listbox_content()
        else:
            print('clw 180 idx is None')

    def curselection(self):
        '''
            Later versions should make it possible to select 
            more than one item but it's not needed right now.
        '''

        selected = None
        items = self.listbox_content.winfo_children()
        highlighted = formats['bg']

        for child in items:
            if child.cget('bg') == highlighted:
                selected = items.index(child)
                break

        return selected

    def highlight_first_last(self, evt):
        if evt.keysym not in ('Down', 'Up'):
            return

        items = self.listbox_content.winfo_children()
       
        len_items = len(items)
        first = items[0]
        last = items[len_items-1]
        if evt.keysym == 'Down':
            first.config(bg=formats['bg'])
            first.focus_set()
            self.listbox_canvas.yview_moveto(0.0)
        elif evt.keysym == 'Up':
            last.config(bg=formats['bg'])
            last.focus_set()
            self.listbox_canvas.yview_moveto(1.0)

    def expand_on_focus(self, evt):
        self.config(bd=4)
        for child in self.listbox_content.winfo_children():
            child.config(takefocus=1)

    def shrink_on_unfocus(self, evt):
        self.config(bd=2)

    def unfocus_listbox(self, evt):
        for child in self.listbox_content.winfo_children():
            child.config(takefocus=0)

    def resize_scrollbar(self):
        self.update_idletasks()  
        self.listbox_canvas.config(
            scrollregion=self.listbox_canvas.bbox("all")) 

    def select_item(self, evt, next_item=None, prev_item=None):

        for widg in self.listbox_content.winfo_children():
            widg.config(bg=formats['highlight_bg'])

        if evt.type == '4':
            selected_item = evt.widget
        elif evt.type == '2' and evt.keysym == 'Down':
            selected_item = next_item
        elif evt.type == '2' and evt.keysym == 'Up':
            selected_item = prev_item

        selected_item.config(bg=formats['bg'])

        widget_ht = int(self.list_height / len(self.items))
        widget_pos_in_screen = selected_item.winfo_rooty()
        widget_pos_in_list = selected_item.winfo_y()
        window_top = self.winfo_rooty()
        window_bottom = window_top + self.view_height
        window_ratio = self.view_height / self.list_height
        list_ratio = widget_pos_in_list / self.list_height
        widget_ratio = widget_ht / self.list_height
        up_ratio = list_ratio - window_ratio + widget_ratio 

        if widget_pos_in_screen > window_bottom - 0.75 * widget_ht:
            self.listbox_canvas.yview_moveto(float(list_ratio))
        elif widget_pos_in_screen < window_top:
            self.listbox_canvas.yview_moveto(float(up_ratio))

        selected_item.focus_set()

    def unhighlight(self, evt):
        evt.widget.config(bg=formats['highlight_bg'])

    def traverse_on_arrow(self, evt):
        if evt.keysym not in ('Up', 'Down'):
            return
        len_items = len(self.items)
        widg_ht = int(
            self.listbox_content.winfo_reqheight()/len_items)
        self.trigger_down = self.view_height - widg_ht * 3
        self.trigger_up = self.view_height - widg_ht * 2
        self.update_idletasks()
        items = self.listbox_content.winfo_children()
        next_item = evt.widget.tk_focusNext()
        prev_item = evt.widget.tk_focusPrev()
        rel_ht = evt.widget.winfo_y()
        if evt.keysym == 'Down':
            if next_item in items:
                self.select_item(evt, next_item=next_item)
            else:
                next_item = items[0]
                next_item.focus_set()
                next_item.config(bg=formats['bg'])
                self.listbox_canvas.yview_moveto(0.0)

        elif evt.keysym == 'Up':
            if prev_item in items:
                self.select_item(evt, prev_item=prev_item)
            else:
                prev_item = items[len_items-1]
                prev_item.focus_set()
                prev_item.config(bg=formats['bg'])
                self.listbox_canvas.yview_moveto(1.0)

if __name__ == '__main__':

    items = [
        'red', 'pink', 'purple', 'magenta',
        'green', 'brown', 'gray', 'black',
        'yellow', 'white', 'chartreuse', 'aqua',
        'beige', 'tan', 'violet', 'teal',
        'ivory', 'rose', 'silver', 'gold',
]



    # items = ['Maecenas lorem ipsem corvallis', 'quis', 'elit', 'eleifen', 'lobortis', 'turpis', 'iaculi', 'odio', 'Phasellus', 'congue', 'urna', 'sit', 'amet', 'posuere', 'luctus', 'mauris', 'risus', 'tincidunt', 'sapie', 'vulputate', 'scelerisqu', 'ipsum', 'libero', 'at', 'neque', 'Nunc', 'accumsan', 'pellentesque', 'nulla', 'a', 'ultricies', 'ex', 'convallis', 'sit', 'ame', 'Etiam', 'ut', 'sollicitudi', 'felis ', 'sit', 'amet', 'dictum', 'lacus', 'Mauris', 'sed', 'mattis', 'diam', 'Pellentesque', 'eu', 'malesuada', 'ipsu', 'vitae', 'sagittis', 'nisl', 'Morbi', 'a', 'mi', 'vitae', 'nunc', 'varius', 'ullamcorper', 'in', 'ut', 'urna', 'Maecenas', 'auctor', 'ultrices', 'orc', 'Donec', 'facilisis', 'tortor', 'pellentesque', 'venenati', 'Curabitur', 'pulvina', 'bibendum', 'se', 'id', 'eleifend', 'lorem', 'sodales', 'ne', 'Mauri', 'eget', 'scelerisque', 'liber', 'Lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'eli', 'Integer', 'vel', 'tellus', 'ne', 'orci', 'finibus', 'ornar', 'Praesent', 'pellentesque', 'aliquet', 'augue', 'nec', 'feugiat', 'augue', 'pos']

    def test_curselection():
        selected = lb.curselection()
        print('264 selected is', selected)

    def test_insert():
        new_item = c.get()
        lb.insert(3, new_item)

    def test_size():
        qty = lb.size()
        print('qty is', qty)

    def test_selection_clear():
        lb.selection_clear()

    def test_selection_set():
        lb.selection_set(8)

    def test_delete():
        lb.delete(6)

    def test_get():
        idx = 4
        got = lb.get(idx)
        print('got is', got)
    
    root = tk.Tk()
    root.geometry('1200x600+900+100')

    left = Frame(root)
    left.grid(column=0, row=0)

    right = Frame(root)
    right.grid(column=1, row=0)

    lb = Listbox(
        left, 
        items,
        view_height=400, 
        view_width=150,
        scrollbar=False)
    lb.grid(column=0, row=0, padx=24, pady=24)

    tx = Text(right)
    tx.grid(column=1, row=0)

    test_box = Frame(root)
    test_box.grid(column=0, row=1, columnspan=2)

    b = Button(
        test_box, text='Test Curselection', command=test_curselection)
    b.grid(column=0, row=0)

    c = Entry(test_box)
    c.grid(column=1, row=0)
    d = Button(test_box, text='Test Insert', command=test_insert)
    d.grid(column=2, row=0)

    e = Button(test_box, text='Test Size', command=test_size)
    e.grid(column=3, row=0)

    f = Button(
        test_box, text='Test Selection_clear', command=test_selection_clear)
    f.grid(column=0, row=1)

    g = Button(
        test_box, text='Test Selection_set', command=test_selection_set)
    g.grid(column=1, row=1)

    h = Button(test_box, text='Test Delete', command=test_delete)
    h.grid(column=2, row=1)

    i = Button(test_box, text='Test Get', command=test_get)
    i.grid(column=3, row=1)

    config_generic(root)

    root.mainloop()


        