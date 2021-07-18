# dev_user_docs.py

intro_head = '''
Good News: ttk is not the last word in configuring Tkinter widgets.
'''

intro_docs = '''
Toykinter widgets are simply-coded, fully-configurable replacements for:
    \u2022 ttk.Combobox
    \u2022 ttk.Notebook
    \u2022 ttk.Sizegrip
    \u2022 ttk.Separator
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

Recently I translated this code into HTML/JavaScript and extended it to create a much better autofill input. The new JS autofill could probably be translated back into Python. The widget fills in after typing one character, most of the time. Instead of using an alphabetical list, it arranges the value list in order that the values were last used. So if you tab out after entering "Bill", then next time you type a "b", "Bill" will autocomplete instead of "billboard" or "Bilbo", and generally you'd only have to type one character. This new code works wonders in cases where the user would generally be using the same value several times in a row. It was created for filling in long nested place names such as "Denver, Arapahoe County, Colorado, United States of America" by typing a "d". If there's any interest I will try to translate it back into Python and add it to this tab.
'''

morewidg_docs = '''
Unlike the ttk.Separator, the Toykinter Separator can be sized and its colors are configured like any Tkinter widget: en masse to match a simple user-defined color scheme. This Separator is horizontal but the code could be extended to make a vertical Separator. Everything below the Separators is a Toykinter widget that works identically to the Tkinter class that it inherits from, except that its colors and fonts can be instantly reconfigured.
'''

italics = '''
There's not much you can't do with Tkinter,
and with Toykinter features added instead of ttk, 
the user has control of their own color schemes too.
See the settings tab for examples of font and color controls
as well as a tabbed widget with the tabs on the bottom instead of on the top.
'''

dev_docs = '''

Toykinter is not a package or a library. There's nothing to install. It's just plain Python and Tkinter code, written for novices by a novice. Just copy the code and use the widgets just about like any other Tkinter widgets. There's not a drop of ttk or Windows theme manipulation here. The main purpose of Toykinter is to replace ttk widgets with widgets that are fully configurable in the same way that non-ttk Tkinter widgets are configured, so that one magic button isn't hiding two incompatible systems. 

This collection of custom widgets also provides a configurable scrollbar and a configurable window border so that your design can be your design without any intrusion from Windows themes or whatever was considered modern GUI design when ttk was added to the Tkinter widget toolkit. There's also an (unfinished) replacement for the Tkinter dropdown menu. Unlike the Tkinter menu, it's configurable like any Tkinter widget. The reason it's unfinished is that I tried to make it work with both keyboard and mouse and I burned out before the project was finished. It could be simplified to work with only the mouse, instead of being finished, or it could be used as a model for starting over.

Other ttk widgets that are replaced by Toykinter include the Combobox, Sizegrip, Separator, and Notebook (i.e. Toykinter TabBook). The Toykinter versions are fully configurable like any non-ttk Tkinter widget. 

The TabBook's tabs can be placed on any of the four corners of the tabbed area. You could do this with the ttk Notebook but since you can't control the shape of the tabs, the rounded top edges will still be on the top of the tab, and there's no way to turn them upside-down if you put them on the bottom of the tabbed area. My experience with ttk.Notebook is limited to saying bad words about its being linked at the hip to Windows themes.

The Scrollbar is optionally hideable, so it will not appear until it's needed. A `scridth` feature is included which is a spacer the same width as the scrollbar which provides extra padding on the N and W edges of the window so that when the scrollbar appears, it will not unbalance the page. The dev-user has to set scridth to the same value as the scrollbar width. Like any scrollbar, the dev-user will have to pay attention to where everything has to be gridded for everything to look right and work right. Some extra widgets are in the mix due to the custom title bar and borders, and the scridth elements, so before trying to implement the Toykinter scrollbar or title bar, come to an understanding of what everything is and why, so that grid and its methods are used on the right columns and rows. It's pretty simple, as I am pretty simple-minded.

The Border class is a Tkinter canvas which provides a complete replacement for the Windows title bar. All four borders are resizers, and a gripper (the Toykinter Sizer) is provided in the SE corner for changing the window's width and height simultaneously. The Border comes in four sizes: 3, 4, 7 & 11. These numbers once meant something. The smallest is meant to look about the same as the Windows title bar. Right now this setting is hard-coded, which my successors to this project can easily improve. Since I've gone back to writing interfaces in HTML and CSS, its hard to deal with the limitations of Pillow, or maybe its just that I haven't learned very much about how Pillow works. I did finally manage to get a logo that was not too bad by making it an SVG in Inkscape and exporting it as four sizes of .png.

Speaking of Pillow, it pip installs automatically with Python 3.8 and 3.9, so if you're having trouble figuring out how to install Pillow, just update your Python version and pip install will take care of Pillow for you.

Along with some configurable widgets to keep ttk and Windows themes from altering your design intentions, this demo app includes a system for reconfiguring the app's fonts and colors globally and instantly with the push of a button. The system detects subclasses instead of your having to type "class=foo" or "style=blah" every time you instantiate a widget. To use this system, all widgets are inherited from Tkinter widgets. If you try to use tkinter.Label, for example, you'll get an error because it doesn't have a subclass detection system built into it for the reconfiguration. Most of the inherited widgets are in widgets.py. There you will see that a method widget.winfo_subclass() is built into every widget subclass with names like Toykinter's Labelx, Framex, etc. The configuration system is inheriting from Labelx to create the widgets that will actually work with the system. When making a new subclass it has to have its own sub-function added to config_generic(). The code is in styles.py.

This demo provides a color-scheme generator which allows the user to make any 4-color scheme desired. It could be extended for more complex color schemes. The color schemes and other settings are stored in a simple SQLite database.

Each toplevel dialog needs to have config_generic(dialog) called on it after its widgets are made, so that the dialog will reconfigure instantly along with the main window. The config_generic() method is imported from styles.py along with the dictionary of user preferences which is created on load by reading from the database.

The main window in this demo is not the root, because removing the Windows border removed the desirable functionality of having a flyout on the taskbar that identifies the app before you click on the taskbar icon. The root window has been named `icon` and it has only an image on it which is for the flyout. The icon on the taskbar will just be a Python icon, but when you mouse over it, the flyout will be whatever image you provide, in this case an old typewriter.

Then a separate toplevel window is used for the main window, instead of the root. All toplevels work the same, and I've had no problems with this system, though it is a recent addition to the family. The new main window is called `view` in this demo instead of `root`. (EDIT: I'm planning to roll this back, it's cute but useless.)

The Border class also includes a statusbar and a non-intrusive style of tooltips which appear at the right side of the statusbar instead of covering content. The statusbar can display a message at the left of the bar when a widget comes into focus.

The scrolling.py module includes an attempted tutorial on how to instantiate scrollbars in Tkinter. One reason the Toykinter scrollbar works is that it's made using the Tkinter API with some of the code suggested by StackOverflow's Tkinter guru Bryan Oakley. I couldn't have done this without his posts, which is not to suggest that either my scrollbar or my tutorial is up to his standards. But the Toykinter Scrollbar seems to work well, and it's configurable, unlike the Tkinter class which uses system colors.

One of the best features of the scrolling.py module is a MousewheelScrolling class which makes the mouse scroll the right window. This wasn't easy, since working with scrolling in Tkinter to begin with isn't effortless, but I got it done for the most part.

Toykinter has an autofill Entry. The simple version doesn't fill anything till you type the first unique character. For example, if "Bill" and "Bilbo" are both in the autofill list, nothing will autofill until you type the second "l" or "b". The other simple version (which I've only written in JavaScript, so it needs to be translated to Python) fills in the most recent value you used that starts with the letter you type. If what fills in is not what you wanted, just keep typing. This one usually gets the right answer after typing the first character.

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
        ...a dropdown item whose text is longer than the dropdown's width displays a 
            tooltip that shows the whole text
        ...the arrow button changes color when the Entry is in focus.
        ...a very long list of values bogs the Combobox down but it works fine with normal-sized values lists.

A listbox widget is included in the repo but not the demo. I've been using this widget successfully for some time. I created it because I couldn't get the tk.Listbox and the tk.Text to work right together. It seems the Text widget doesn't like the Listbox widget for some reason. So I wrote some naive code and it works fine. The scrollbar section needs to be done over. I don't know how I got that to work, especially after reading my notes on it. Now that there's a Toykinter scrollbar, it should be added to this class in lieu of the tk.Scrollbar that's used in it now.

Odd cases of the word "tree" will appear in some variables because most of this code has been written while I work on a GUI for family tree databases.

Nothing in this collection of widget classes is completely finished or perfect. It's not my main focus right now. But I will be starting a do list for the project now that I've got it organized into a discrete demo app. So here begins a list of Toykinter's deficits, defects, shortcomings, and unfinished/neglected/forgotten/broken features as well as ways to improve and reformat this demo app. Most of the problems are newer than the code, i.e. some things weren't being updated "till later", and now "later" has rolled around and these things all need to be fixed at once. Instead of delaying the initial commit to this repo any longer, I'm creating a do list:

DO LIST (easy stuff at top; scary stuff toward bottom unless urgent)

\u2022 Some of the tabs need a scrollbar since you'd have to set the font to 13 or less to see everything.
\u2022 Need a way to refer to tabs similar to ttk.Notebook's `notebook.index('current')`.
\u2022 Every module should have a separate demo i.e. `if __name__ == "__main__"` at bottom.
\u2022 Changing font size should change title bar size. Currently this has to be done manually by changing the hard-coded size setting where Border is instantiated in toykinter_demo.py. Maybe a method will be needed in the Border class which can be called in the font_picker.py module.
\u2022 Add right-click context help menu, the code for this already exists in treebard_gps repo.
\u2022 Combobox is bogging down with a large list of values. In any case where there is a long list of values that has to be accessed frequently and/or needs good response, just use an autofill entry instead of a Combobox. For changing fonts in this little app, it's OK that the Combobox is slow (it's Python). But possibly a refactoring is in order even though the current design is the third or fourth start-over and works well with small lists of values.
\u2022 Combobox recolorizing is a compromise right now. The dropdown buttons respond to so many events that it might be a sort of minor miracle to make them colorize instantly. For now it's enough that they do colorize on reload. They are not on top, they're only seen on dropdown. It's not top priority compared to other things on this list.
\u2022 colorizer preview area: The buttons and header background in the preview area are right as shown in preview_scheme() but then on APPLY not all of them actually use the color shown. There are three background colors and they actually use one of the others on APPLY. Before changing this, figure out a place in the preview area to show all three background colors and then fix it so when APPLY is pressed, these chosen colors remain as shown in the preview.
\u2022 Scrollbar.colorize is running many times on load and several more times when changing the color scheme. I don't see that many scrollbars including the comboboxes. Look at what's printing in scrollbar.colorize() to see where all the scrollbars are.
\u2022 There are 2 ways of detecting subclass in styles.py. The old way is a long switch statement (lots of if/elif) in config_generic(). The new way is a set of hard-coded global tuples at top of styles.py. Change as much as possible to the new way.
\u2022 The dropdown menu isn't being used right now because it was never finished. It could be simplified to work with mouse-only instead of trying to make it work with both the mouse and the keyboard. Or maybe it was OK and I was just being too picky, I don't remember exactly when or why I set it aside. I just remember being annoyed that Tkinter tried to make me use system colors after I worked so hard to make everything configurable on the press of one button.
\u2022 The combobox scrollbar slider seems to be dropping the grab sometimes, or am I just losing my grip on long scrolls?
\u2022 TabBook tabs don't take focus (not important, you can use the mouse or the accelerator keys e.g. Alt+F).
\u2022 Look into making the scrollbars and the app and the tabs work like a modern browser: there should be a hideable vertical scrollbar on the whole window, no horizontal scrollbar on anything, and no separate scrollbars on the tabs. The app should be responsive when manually resizing, especially as regards width since there should be no horizontal scrollbars. I've never looked into doing this for Tkinter since my main app uses a huge table that can't change its layout to be responsive. So I tend to use too many scrollbars by habit. Contents should expand to fill window if main window is manually resized. This demo could certainly be fixed to behave better but I have other things to do right now.
\u2022 Color schemes have a database column `built_in` which prevents the color scheme from being deleted by user if it's set to 1. All are set to 1 right now but can be deleted in the GUI by first manually setting the column to 0 for that color scheme. The purpose of the `hidden` column is to allow user to hide color scheme that he can't delete since it's built-in. I have to go through the color schemes and decide which can be set to 0 in the built_in column. Then code can be written so that if the user tries to delete a built_in color scheme, the `hidden` column can instead be set to 1. Further coding would get the color scheme removed from the GUI but set to 1 and 1 in the db for `built_in` and `hidden` respectively. This would be overkill for this demo app but would be useful in a real app where certain color schemes are provided out of the box and user can add others. The ones he adds himself would be `built_in = 0` by default. Right now user can delete his own color schemes but the rest are undeletable without updating the database manually, including some ugly or useless color schemes.
\u2022 Using the root to just hold a taskbar icon was an interesting experiment but should probably be rolled back. I think the complications outweigh the advantages. For example, if you minimize the app, there are now two flyouts when hovering over the Python icon on the Windows taskbar. One is the old typewriter which is displayed on the root window. The other is the favicon. Better to accept the limitations of Tkinter and the fact (I assume) that until an app is packaged as an .exe, it's going to show on the taskbar with a generic Python icon. In short, get rid of "icon" and "view" and combine them into "root" as Tkinter is normally used. See toykinter_demo.py.

'''