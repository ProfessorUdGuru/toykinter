# autofill.py

# this is the new autofill as of 20210722 which I'm translating from JS to Python
# It hasn't been added to the Toykinter demo yet, but it's fully functional.

import tkinter as tk
from widgets import EntryUnhilited, Entry
import dev_tools as dt
from dev_tools import looky, seeline

class EntryAuto(EntryUnhilited):
    '''
        To use this class, after instantiating it, you have to call 
        EntryAuto.create_lists(all_items). Other than getting all_items
        (e.g. from a database query), the class is self-contained. Every
        instance of the widget in the same module will use the same autofill
        values, so if that's a problem it will have to be redesigned to
        add a column number parameter (or something) so it knows which list 
        to use.
        
    '''


    recent_items = []
    all_items_unique = []

    def create_lists(all_items):
        for item in all_items:
            if item not in EntryAuto.recent_items:
                EntryAuto.all_items_unique.append(item)
        EntryAuto.final_items = EntryAuto.recent_items + EntryAuto.all_items_unique

    def __init__(self, master, autofill=False, values=[], *args, **kwargs):
        EntryUnhilited.__init__(self, master, *args, **kwargs)

        self.master = master
        self.autofill = autofill
        
        self.bind("<KeyPress>", self.detect_pressed)
        self.bind("<KeyRelease>", self.get_typed)
        self.bind("<FocusOut>", self.prepend_match, add="+")
        self.bind("<FocusIn>", self.deselect, add="+")

    def detect_pressed(self, evt):
        '''
            runs on every key press
        '''
        if self.autofill is False:
            return
        key = evt.keysym
        if len(key) == 1:
            self.pos = self.index('insert')
            keep = self.get()[0:self.pos]
            self.delete(0, 'end')
            self.insert(0, keep)

    def get_typed(self, evt):
        '''
            runs on every key release; filters out non-alpha-numeric 
            keys; runs the functions not triggered by events.
        '''
        if self.autofill is False:
            return
        key = evt.keysym
        if len(key) == 1:
            hits = self.match_string()
            self.show_hits(hits, self.pos)

    def match_string(self):
        hits = []
        got = self.get()
        use_list = EntryAuto.final_items
        for item in use_list:
            if item.lower().startswith(got.lower()):
                hits.append(item)
        return hits

    def show_hits(self, hits, pos):
        cursor = pos + 1
        if len(hits) != 0:
            self.delete(0, 'end')
            self.insert(0, hits[0])
            self.icursor(cursor)

    def prepend_match(self, evt):
        content = self.get()
        print("line", looky(seeline()).lineno, "content:", content)
        if content in EntryAuto.final_items:
            idx = EntryAuto.final_items.index(content)
            del EntryAuto.final_items[idx]
            EntryAuto.final_items.insert(0, content)
        print("line", looky(seeline()).lineno, "EntryAuto.final_items[0]:", EntryAuto.final_items[0])

    def deselect(self, evt):
        '''
            This callback was added because something in the code for this 
            widget caused the built-in replacement of selected text with 
            typed text to stop working. So if you
            tabbed into an autofill entry that already had text in it, the text
            was all selected as expected but if you typed, the typing was added
            to the end of the existing text instead of replacing it, which is
            unexpected. Instead of finding out why this is happening, I added
            this callback so that tabbing into a filled-out autofill will not
            select its text. This might be better since the value in the field
            is not often changed and should not be easy to change by mistake.
        '''
        self.select_clear()

if __name__ == "__main__":

    all_items = [
        "Flagstaff, Coconino County, Arizona",
        "Fond du Lac, USA",
        "Fort Pierce, USA",
        "Fort Morgan, USA",
        "Flagstaff, USA",
        "Fairmont, USA",
        "Fitchburg, USA",
        "Falmouth, USA",
        "Flagstaff, Arizona, USA",
        "Fairbanks, USA",
        "Florissant, USA",
        "Florence, USA",
        "Fairfax, USA",
        "Farmington, USA",
        "Fayetteville, USA",
        "Fort Kent, USA",
        "Forrest City, USA",
        "Freeport, USA",
        "Fort Benton, USA",
        "Fort Barbour, UK",
        "Fort Worth, USA",
        "Fort Lee, USA",
        "Florida, USA",
        "Flemington, Italy",
        "Frederick, USA",
        "Findlay, USA",
        "Fredericksburg, USA",
        "Fairfield, USA",
        "Fernandina Beach, USA",
        "Ferguson, USA",
        "Fallon, USA",
        "Fitzgerald, USA",
        "Franklin, USA",
        "Fort Valley, USA",
        "Fulton, USA",
    ]

    root = tk.Tk()

    autofill = EntryAuto(root, autofill=True, width=40)
    autofill.grid()
    autofill.focus_set()

    
    traverse = Entry(root)
    traverse.grid()

    autofill2 = EntryAuto(root, autofill=True, width=40)
    autofill2.grid()
    EntryAuto.create_lists(all_items)
    root.mainloop()






