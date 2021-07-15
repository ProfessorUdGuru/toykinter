# dev_user_docs.py

intro_head = '''
Good News: ttk is not the last word in configuring Tkinter widgets.
'''

intro_docs = '''
Toykinter widgets are simply-coded, fully-configurable replacements for:
    \u2022 ttk.Combobox
    \u2022 ttk.Notebook
    \u2022 ttk.Sizegrip
    \u2022 tk.Scrollbar
    \u2022 Windows title bar, window border, and window decorations
    \u2022 tk.Menu

Toykinter also provides:
    \u2022 a single means to reconfigure colors and fonts globally
    \u2022 a simple way for the user to create custom color schemes
    \u2022 autocomplete Entry widget
    \u2022 unobtrusive tooltips that appear in the status bar

You are invited to use this code and improve on it.

Toykinter's creator is doing other things right now.

Suggestions will be added to the do list.
        
'''

autofill_docs = '''

This simple autofill entry can use values from a Python list which could be hard-coded or populated by a database query, for example. To use it, you have to add three simple lines of code in the instance:

    \u2022 `autofill = True`
    \u2022 `instance.config(textvariable=instance.var)`
    \u2022 `instance.values = ['red', 'rust', 'black', 'blue', 'Bill', 'Bilbo', 'billboard']`

The purpose of the `autofill` boolean is so a whole table can be populated with the same widget class, then one or more columns can be set to `autofill=True`. For a large table, depending on the design you may want to use the `EntryAutofill` class which works exactly the same but looks like a label. Or to make it more obvious that the table cells are to be filled out, the `EntryAutofillHilited` class can be used as done on this tab.

This code makes the user type until a unique character is reached. For example, if 'Bill', 'Bilbo' and 'billboard' are all in the list, then 'Bill' would have to be typed out all the way; 'Bilbo' or 'billboard' won't fill in until the second 'b' is typed.

I wrote this code because none of the autofill entries I could find for Tkinter did what I wanted. Some of them didn't work very well. Others were too complex. When I finally got fed up and tried to make my own, I couldn't believe how easy it was. Maybe I just got lucky.

Recently I translated this code into HTML/JavaScript and extended it to create a much better autofill input. The new JS autofill could probably be translated back into Python. The widget fills in after typing one character, most of the time. Instead of using an alphabetical list, it arranges the value list in order that the values were last used. So if you tab out after entering "Bill", then next time you type a "b", "Bill" will autocomplete instead of "billboard" or "Bilbo", and generally you'd only have to type one character. This new code is the bee's knees, so if there's any interest I will try to translate it back into Python and add it to this tab.
'''

dev_docs = '''

Toykinter is not a package or a library. There's nothing to install. It's just plain Python and Tkinter code, written for novices by a novice. Just copy the code and use the widgets just about like any other Tkinter widgets. There's not a drop of ttk here, as the main purpose of Toykinter is to replace ttk widgets with widgets that are fully configurable in the same way that non-ttk Tkinter widgets are configured. This collection of custom widgets also provides a configurable scrollbar and a configurable window border so that your design can be your design without any intrusion from Windows themes or whatever was considered modern GUI design when ttk was added to the Tkinter widget toolkit. There's also an (unfinished) replacement for the Tkinter dropdown menu. Unlike the Tkinter menu, it's configurable like any Tkinter widget. The reason it's unfinished is that I tried to make it work with both keyboard and mouse and I burned out before
the project was finished. It could be simplified to work with only the mouse, instead of being finished, or it could be used as a model for starting over.

Other ttk widgets that are replaced by Toykinter include the Combobox, Sizegrip and Notebook. The Toykinter versions are fully configurable like any non-ttk Tkinter widget. 

The Notebook's tabs can be placed on any of the four corners of the tabbed area. You could do this with the ttk Notebook but since you can't control the shape of the tabs, the rounded top edges will still be on the top of the tab, and there's no way to turn them upside-down if you put them on the bottom of the tabbed area.

The Scrollbar is optionally hideable, so it will not appear until it's needed. A `scridth` feature is included which is a spacer the same width as the scrollbar which provides extra padding on the N and W edges of the window so that when the scrollbar appears, it will not unbalance the page. The dev-user has to set scridth to the same value as the scrollbar width. Like any scrollbar, the dev-user will have to pay attention to where everything has to be gridded for everything to look right and work right. Some extra widgets are in the mix due to the custom title bar and borders, and the scridth elements, so before trying to implement the Toykinter scrollbar or title bar, come to an understanding of what everything is and why, so that grid and its methods are used on the right columns and rows.

The Border class is a Tkinter canvas which provides a complete replacement for the Windows title bar. All four borders are resizers, and a gripper is provided in the SE corner for resizing width and height at simultaneously. The Border comes in four sizes. the smallest is meant to look about the same as the Windows title bar. Right now this setting is hard-coded, which my successors to this project can easily improve. Since I've gone back to writing interfaces in HTML and CSS, its hard to deal with the limitations of Pillow, or maybe its just that I haven't learned very much about how Pillow works.

Speaking of Pillow, it pip installs automatically with Python 3.8 and 3.9, so if you're having trouble figuring out how to install Pillow, just update your Python version and pip install will take care of Pillow for you.

Along with some configurable widgets to keep ttk and Windows themes from altering your design intentions, this demo repo includes a system for reconfiguring the app's fonts and colors globally and instantly with the push of a button. The system detects subclasses instead of your having to type "class=foo" or "style=blah" every time you instantiate a widget. To use this system, all widgets are inherited from Tkinter widgets. If you try to use tkinter.Label, for example, you'll get an error because it doesn't have a subclass detection system built into it for the reconfiguration. Most of the inherited widgets are in widgets.py. There you will see that a method widget.winfo_subclass() is built into every widget subclass with names like Toykinter's Labelx, Framex, etc. The configuration system is inheriting from Labelx to create the widgets that will actually work with the system. When making a new subclass it has to have its own config_* sub-function added to config_generic, even if the class it's inheriting from is already a sub-class that already has its own config sub-function. The code is in styles.py.

This demo provides a color-scheme generator which allows the user to make any 4-color scheme desired. It could be extended for more complex color schemes. The color schemes and other settings are stored in a simple SQLite database.

Each toplevel dialog needs to have config_generic(dialog) called on it after its widgets are made, so that the dialog will reconfigure instantly along with the main window. The config_generic() method is imported from styles.py along with the dictionary of user preferences which is created on load by reading from the database.

The main window in this demo is not the root, because removing the Windows border removed the desirable functionality of having a flyout on the taskbar that identifies the app before you click on the taskbar icon. The root window has been named `icon` and it has only an image on it which is for the flyout. The icon on the taskbar will just be a Python icon, but when you mouse over it, the flyout will be whatever image you provide, in this case an old typewriter.

Then a separate toplevel window is used for the main window, instead of the root. All toplevels work the same, and I've had no problems with this system, though it is a recent addition to the family. The new main window is called `view` in this demo instead of `root`.

The Border class also includes a statusbar and a non-intrusive style of tooltips which appear at the right side of the statusbar instead of covering content.

The scrolling.py module includes an attempted tutorial on how to instantiate scrollbars in Tkinter. One reason the Toykinter scrollbar works is that it's made using the Tkinter API with some of the code suggested by StackOverflow's Tkinter guru Bryan Oakley. I couldn't have done this without his posts, which is not to suggest that either my scrollbar or my tutorial is perfect.

One of the best features of the scrolling.py module is a MousewheelScrolling class which makes the mouse scroll the right window. This wasn't easy, since working with scrolling in Tkinter to begin with isn't easy, but I got it done for the most part.

Which of course Toykinter has two varieties of. The simple version doesn't fill anything till you type the first unique character. For example, if "Bill" and "Bilbo" are both in the autofill list, nothing will autofill until you type the second "l" or "b". The other simple version fills in the most recent value you used that starts with the letter you type. If what fills in is not what you wanted, just keep typing. This one usually gets the right answer after typing the first character.

Speaking of Bilbo, there's already an unfinished Bilbobox in this collection, which is a combobox that drops down on hover instead of click. It worked at one time and the instructions for bringing it back to life are in the module.

The Toykinter Combobox, on the other hand, is a serious piece of work. Not to say that it's perfect, but as far as I know it does what it's supposed to do, and more:

    Replaces ttk.Combobox with an easily configurable widget.

    Configuration is done tkinter style, instead of pitting ttk.Style
    and Windows themes against each other to see which one wins, as is
    the norm when trying to configure ttk widgets.

    Unlike ttk.Combobox...
        ...dropdown items are selected with mouse, Return key, or 
            spacebar
        ...colors including Entry background are easily configured
        ...clicking either Entry or Arrow opens then closes dropdown on 
            alternate clicks
        ...FocusOut event can be bound to the dropdown items
        ...arrow traversal thru dropdown loops to top or bottom when 
            bottom or top is reached
        ...dropdown opens with either Up or Down arrow key, with either 
            top or bottom item highlighted
        ...a long dropdown auto-scrolls while traversing with arrow keys
        ...a dropdown item with text longer than the window displays a 
            tooltip that shows the whole text
        ...the arrow button changes color when the Entry is in focus.

A listbox widget is included. I've been using this widget successfully for some time. I created it because I couldn't get the tk.Listbox and the tk.Text to work right together. It seems the Text widget doesn't like the Listbox widget for some reason. So I wrote some naive code and it works fine. The scrollbar section needs to be done over, even I don't know how I got that to work, especially after reading my notes on it. Now that there's a Toykinter scrollbar, it should be added to this class in lieu of the tk.Scrollbar that's used in it now.

Odd cases of the word "tree" will appear in some variables because most of this code has been written while I work on a GUI for family tree databases.

Nothing in this collection of widget classes is completely finished or perfect. It's not my main focus right now. But I will be starting a do list for the project now that I've got it organized into a discrete demo app. So here begins a list of Toykinter's deficits, defects, shortcomings, and unfinished/neglected/forgotten/broken features as well as ways to improve and reformat this demo app. Most of the problems are newer than the code, i.e. some things weren't being updated "till later", and now "later" has rolled around and these things all need to be fixed at once. Instead of delaying the initial commit to this repo any longer, I'm creating a do list:

DO LIST (easy stuff at top; scary stuff toward bottom unless urgent)

\u2022 make fonts tab smaller so it's not bigger than colors tab
\u2022 delete_sample() not working in colorizer.py (it worked once but I don't know what I did different).
\u2022 title bar is not recolorizing
\u2022 merge colors branch; add another tab called widgets to display a Text, Separator, and other misc. widgets
\u2022 add a status message to some of the widgets
\u2022 The statusbar tooltips on colorizer.py don't work, probably still using the old version. On title bar they work but seem to be too big and not flush w/ bottom of status bar.
\u2022 Make sure separator.colorize() is working.
\u2022 The active title bar color should be right with somewhat less encouragement.
\u2022 Need a way to refer to tabs similar to ttk.Notebook's `notebook.index('current')`.
\u2022 The logo is yuck.
\u2022 The font on the TabBook tabs could be smaller.
\u2022 Every module should have a separate demo i.e. `if __name__ == "__main__"` at bottom.
\u2022 Changing font size should change title bar size.
\u2022 Mousewheel scrolling needs to be activated on the Docs tab.
\u2022 Add a scrollbar to each tab where there's a lot of text which can be reconfigured to a larger font size thus overflowing the fixed size of the tab.
\u2022 Unused classes and styles need to be weeded out of widgets.py and styles.py. Also in treebard project separate widgets.py into toykinter_widgets.py and treebard_widgets.py so changes in toykinter widgets can be copied easily to the other project.
\u2022 Combobox is bogging down with a large list of values. In any case where there is a long list of values that has to be accessed frequently and/or needs good response, just use an autofill entry instead of a Combobox. For changing fonts in this little app, it's OK that the Combobox is slow (it's Python), but possibly a refactoring is in order even though the current design is the third or fourth start-over and works well with small lists of values.
\u2022 Combobox recolorizing is a compromise right now. The dropdown buttons respond to so many events that it might be a sort of minor miracle to make them colorize instantly. For now it's enough that they do colorize on reload. They are not on top, they're only seen on dropdown. It's not top priority compared to other things on this list.
\u2022 colorizer preview area: The buttons and header background in the preview area are right as shown in preview_scheme() but then on APPLY they don't actually use that color. There are three background colors and they actually use one of the others on APPLY. Before changing this, figure out a place in the preview area to show all three background colors and then fix it so when APPLY is pressed, these chosen colors remain as shown in the preview.
\u2022 Scrollbar.colorize is running nine times on load and 7 more times when changing the color scheme. I only count 6 scrollbars including the comboboxes. Look at what's printing in scrollbar.colorize() to see what all the scrollbars are.
\u2022 change "table_head_bg" to "head_bg" also in db
\u2022 There are 2 ways of detecting subclass in styles.py. The old way is a long switch statement in config_generic. The new way is a set of hard-coded global tuples at top of styles.py. Change as much as possible to the new way.
\u2022 The dropdown menu isn't being used right now because it was never finished. It could be simplified to work with the mouse only instead of trying to make it work with the mouse and the keyboard.
\u2022 The combobox scrollbar slider seems to be dropping the grab sometimes, or am I just losing my grip?
\u2022 TabBook tabs don't take focus (not important, use the mouse)

'''