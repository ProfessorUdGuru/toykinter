import tkinter as tk
import sqlite3
from files import current_file
from query_strings import(
    select_opening_settings, select_all_color_schemes,
    select_all_color_schemes_plus)
from dev_tools import looky, seeline

'''
    When making a new subclass it has to have its own config_* sub-function
    added to config_generic, even if the class it's inheriting from is already
    a sub-class that already has its own config sub-function.

    Some of the more complex custom widgets have their own method w.colorize()
    which is called here in `config_generic()`.
'''


MAX_WINDOW_HEIGHT = 0.95
MAX_WINDOW_WIDTH = 0.995
NEUTRAL_COLOR = '#878787'

'''
    widget.winfo_class() is a built-in Tkinter method that refers to 
    Tkinter classes such as 'Label' or ttk classes such as 'TLabel'.
    widget.winfo_subclass() is a custom method that refers to subclasses 
    such as 'Label' that this app creates by inheriting from Tkinter. The 
    purpose of this module is to do with Tkinter widgets what they are 
    saying can only be done with ttk widgets: configure widgets by class 
    instead of one at a time. This is supposed to replace or make 
    unnecessary ttk.Style and Windows themes, using methods that novice 
    coders can understand easily while getting predictable results, 
    whereas ttk widgets fall short in that regard.

    The worst thing about this method of reconfiguring values is that
    if you accidentally use a tkinter widget like this: "lab = tk.Label..."
    you'll get an error like this... so don't use any tk.widgets:
    Traceback (most recent call last):
      File "C:\treebard_gps\app\python\ccccc.py", line 33, in <module>
        TS.config_generic(root)
      File "C:\treebard_gps\app\python\styles.py", line 449, in config_generic
        widg.winfo_subclass() == 'LabelStay'):
    AttributeError: 'Label' object has no attribute 'winfo_subclass'

    The other worst thing is (if I recall correctly), you have to do 
    winfo_class() before you can do winfo_subclass(). 

    To use this method of configuration by detecting subclasses, you have to
    remember to not use the parent tkinter classes, only the subclasses.
'''
'''
    These hard-coded tuples represent groups of widgets that take common 
    formatting changes when the user changes a style preference. 
    The tuples below can have new subclasses added to them manually, if the
    configuration needs of that subclass fit the corresponding subfunction. In
    case of a fit, then adding the name of the new subclass to a tuple is all
    you have to do. 
    Otherwise it has to be added to the switch in `config_generic()` and given
    a subfunction there to configure it. Only options that can be changed by 
    the user are handled here, usually fg, bg, and font. The intended result is 
    no styling in the widget construction code since all styles are built into 
    subclasses. The reason for going to all this trouble is so that all widgets
    can be instantly restyled by the user on the press of a button.

    Naming conventions for these tuples and the functions that refer to them:
    3 parts of camelCase: camel is bg/fg/font; Case is Std/Lite/Head for bg or 
    In/Out for font (short for standard/highlight/heading or Input/Output); 
    Example: `bgStd_fgStd_fontIn` for "use standard background color, standard 
    foreground color, and input font". The name for the corresponding function 
    is the same as the tuple with "config_" prepended, 
    e.g: `config_bgStd_fgStd_fontIn()`
    For font styles see `prefs_to_use[6]` in `make_formats_dict()`.
'''

bgStd = (
    'Frame', 'Toykinter', 'Main', 'Colorizer', 'Toplevel', 'FontPicker',
    'StatusbarTooltips')

bgHead = ('FrameHilited2',)

bgLite = (
    'FrameHilited', 'FrameHilited1', 'FrameHilited3', 'FrameHilited4', 
    'LabelTitleBar', 'Sizer', 'ToolTip', 'TabBook',
    'ToplevelHilited')

bgStd_fgStd = ('Sizer', )

bgStd_fgStd_fontOut = ('Label', 'LabelFrame')

bgStd_fgStd_fontIn = ('LabelButtonText',)

bgLite_fgStd_fontIn_insFg = ('Entry', 'Text')

bgStd_fgStd_fontIn_insFg = ('EntryAutofill', 'EntryUnhilited')

# bgLite_fgStd_fontOut = ('LabelHilited', )
bgLite_fgStd_fontOut = ()

bgHead_fgStd_fontOut = ('LabelHilited2', )
    
bgStd_fgStd_fontOut_disAbl = ('LabelStylable', 'MessageCopiable')

'''
    The variable `formats` can't be global in this module because these are
    reconfiguration functions and the colors that were current when this 
    module first loaded are changed when the recolorizer runs. A global 
    variable would only run once when this module is imported so the config 
    subfunctions have been nested inside of the main config_generic() in order 
    to prevent connecting to the database once for each of the subfunctions.
'''

def get_all_descends (ancestor, deep_list):
    ''' 
        So all widgets can be configured at once, this lists every widget in 
        the app by running recursively.
    '''

    lst = ancestor.winfo_children()        
    for item in lst:
        deep_list.append(item)
        get_all_descends(item, deep_list)
    return deep_list

def config_generic(parent):
    ''' 
        Call this for every Toplevel window constructed to apply consistent 
        styling to tkinter widgets so widgets don't have to be styled 
        individually. This is also called in colorizer to change the color 
        of everything instantly. 
    '''

    def config_bgStd(widg):
        widg.config(bg=formats['bg'])

    def config_bgLite(widg):
        widg.config(bg=formats['highlight_bg'])
       
    def config_bgHead(widg):
        widg.config(bg=formats['table_head_bg'])

    def config_bgStd_fgStd(widg):
        widg.config(bg=formats['bg'], fg=formats['fg'])

    def config_bgStd_fgStd_fontOut(widg):
        widg.config(
            bg=formats['bg'],
            fg=formats['fg'],
            font=formats['output_font'])

    def config_bgLite_fgStd_fontOut(widg):
        widg.config(
            bg=formats['highlight_bg'], 
            fg=formats['fg'],
            font=formats['output_font']) 

    def config_bgHead_fgStd_fontOut(widg):
        widg.config(
            bg=formats['table_head_bg'], 
            fg=formats['fg'],
            font=formats['output_font'])  

    def config_bgStd_fgStd_fontIn(widg):
        widg.config(
            bg=formats['bg'],
            fg=formats['fg'],
            font=formats['input_font'])

    def config_bgLite_fgStd_fontIn_insFg(widg):
        widg.config( 
            bg=formats['highlight_bg'], 
            fg=formats['fg'],
            font=formats['input_font'],
            insertbackground=formats['fg'])

    def config_bgStd_fgStd_fontIn_insFg(widg):
        widg.config(
            bg=formats['bg'], 
            fg=formats['fg'], 
            font=formats['input_font'], 
            insertbackground=formats['fg'])

    def config_bgStd_fgStd_fontOut_disAbl(widg):
        widg.config(state='normal')
        widg.config(
            bg=formats['bg'],
            fg=formats['fg'],
            font=formats['output_font'])
        widg.config(state='disabled')     

    def config_labeltip(lab):
        lab.config(
            bg=formats['highlight_bg'],
            fg=formats['fg'],
            font=formats['status'])

    def config_labeltip2(lab):
        lab.config(
            bg=formats['table_head_bg'],
            fg=formats['fg'],
            font=formats['status'])

    def config_labeltipbold(lab):
        lab.config(
            bg=formats['highlight_bg'],
            fg=formats['fg'],
            font=formats['titlebar_1'])

    def config_labelitalic(lab):
        lab.config(
            bg=formats['bg'],
            fg=formats['fg'],
            font=formats['show_font'])

    def config_labelnegative(lab):
        lab.config(
            bg=formats['fg'], 
            fg=formats['bg'],
            font=formats['output_font'])

    def config_heading1(lab):
        lab.config(
            bg=formats['bg'], 
            fg=formats['fg'], 
            font=formats['heading1'])

    def config_heading2(lab):
        lab.config(
            bg=formats['bg'], 
            fg=formats['fg'], 
            font=formats['heading2'])

    def config_heading3(lab):
        lab.config(
            bg=formats['bg'], 
            fg=formats['fg'], 
            font=formats['heading3'])

    def config_heading4(lab):
        lab.config(
            bg=formats['bg'], 
            fg=formats['fg'], 
            font=formats['heading4'])
        
    def config_boilerplate(lab):
        lab.config(
            bg=formats['bg'], 
            fg=formats['fg'], 
            font=formats['boilerplate'])

    # ************* special event widgets ********************

    # widgets that have highlight/unhighlight events need some
    #    special treatment to keep up with changes of the
    #    color scheme. In the class definition do this:
    # self.formats = make_formats_dict()
    # And in the highlight/unhighlight methods do this:
    # bg=self.formats['blah'] ...instead of bg=formats['blah']
    # And give them their own config function here:

    def config_labelhilited(lab):
    # def config_comboboxarrow(lab):
        print("line", looky(seeline()).lineno, "running:")
        lab.formats = formats 
        lab.config(
            bg=formats['highlight_bg'],
            fg=formats['fg'],
            font=formats['output_font']) 

    def config_labeltab(lab):
        lab.formats = formats
        if lab.chosen is False:
            lab.config(
                bg=formats['highlight_bg'],
                fg=formats['fg'])
        else:
            lab.config(
                bg=formats['bg'],
                fg=formats['fg'])

    def config_labelmovable(lab):
        lab.formats = formats
        lab.config(
            bg=formats['highlight_bg'], 
            fg=formats['fg'],
            font=formats['output_font'])

    def config_entrydefaulttext(ent):
        ent.formats = formats
        ent.config(
            background=formats['highlight_bg'],
            font=formats['show_font'])

    # ***********************************

    def config_buttons(button):
        button.config(
            bg=formats['bg'],  
            fg=formats['fg'],
            font=(formats['output_font']),
            activebackground=formats['table_head_bg'])

    def config_buttons_plain(button):
        button.config(
            bg=formats['bg'],  
            fg=formats['fg'],
            font=(formats['input_font']),
            activebackground=formats['table_head_bg'])

    def config_buttonflathilited(button):
        button.config(
            bg=formats['highlight_bg'],
            fg=formats['fg'],
            activebackground=formats['fg'],
            activeforeground=formats['bg'])

    def config_radiobuttons(radio):
        radio.config(
            bg=formats['bg'],
            fg=formats['fg'], 
            activebackground=formats['highlight_bg'],
            selectcolor=formats['highlight_bg']) 

    def config_radiobuttonhilited(radio):
        radio.config(
            bg=formats['highlight_bg'],
            fg=formats['fg'], 
            activebackground=formats['bg'],
            selectcolor=formats['bg']) 

    def config_separator(sep):
        ''' 
            has 3 frames with 3 different colors
            so needs its own reconfigure method 
        '''
        sep.colorize() 

    def config_messages(widg):
        widg.config( 
            bg=formats['bg'], 
            fg=formats['fg'],
            font=formats['output_font'])

    def config_messageshilited(widg):
        widg.config( 
            bg=formats['highlight_bg'], 
            fg=formats['fg'],
            font=formats['output_font'])

    def config_labelcopiable(widg):
        widg.config(state='normal')
        widg.config(
            bg=formats['bg'], 
            fg=formats['fg'])
        widg.config(state='readonly')
        widg.config(readonlybackground=widg.cget('background'))

    def config_scale(widg):
        widg.config(
            bg=formats['bg'], 
            fg=formats['fg'], 
            font=formats['output_font'],
            troughcolor=formats['highlight_bg'],
            activebackground=formats['table_head_bg'])

    formats = make_formats_dict()

    ancestor_list = []
    all_widgets_in_root = get_all_descends(
        parent, ancestor_list)

    for widg in (all_widgets_in_root):
        if (widg.winfo_class() == 'Label' and 
            widg.winfo_subclass() == 'LabelStay'):
                pass

        elif widg.winfo_class() == 'Frame':
            if widg.winfo_subclass() == 'FrameStay':
                pass

            elif widg.winfo_subclass() in bgStd:
                config_bgStd(widg)

            elif widg.winfo_subclass() in bgHead:
                config_bgHead(widg)

            elif widg.winfo_subclass() in bgLite:
                config_bgLite(widg)

            elif widg.winfo_subclass() == 'Combobox':
                widg.colorize()

            elif widg.winfo_subclass() == 'Separator':
                config_separator(widg)

            elif widg.winfo_subclass() == 'EntryDefaultText':
                config_entrydefaulttext(widg)

        elif widg.winfo_class() == 'Label': 

            if widg.winfo_subclass() in bgHead:
                config_bgHead(widg) 
          
            elif widg.winfo_subclass() in bgStd_fgStd:
                config_bgStd_fgStd(widg)

            elif widg.winfo_subclass() in bgStd_fgStd_fontOut:
                config_bgStd_fgStd_fontOut(widg)

            elif widg.winfo_subclass() in bgLite_fgStd_fontOut:
                config_bgLite_fgStd_fontOut(widg)

            elif widg.winfo_subclass() in bgHead_fgStd_fontOut:
                config_bgHead_fgStd_fontOut(widg)

            elif widg.winfo_subclass() == 'LabelH2':
                config_heading2(widg)
            elif widg.winfo_subclass() == 'LabelH3':
                config_heading3(widg)
            elif widg.winfo_subclass() == 'LabelBoilerplate':
                config_boilerplate(widg)
            elif widg.winfo_subclass() == 'LabelItalic':
                config_labelitalic(widg)
            elif widg.winfo_subclass() == 'LabelHilited':
                config_labelhilited(widg)
            # elif widg.winfo_subclass() == 'ComboboxArrow':
                # config_comboboxarrow(widg)
            elif widg.winfo_subclass() == 'LabelTab':
                config_labeltab(widg)
            elif widg.winfo_subclass() == 'LabelTip':
                config_labeltip(widg)
            elif widg.winfo_subclass() == 'LabelTip2':
                config_labeltip2(widg)
            elif widg.winfo_subclass() == 'LabelTipBold':
                config_labeltipbold(widg)
            elif widg.winfo_subclass() == 'LabelNegative':
                config_labelnegative(widg)
            elif widg.winfo_subclass() == ('TitleBarButtonSolidBG'):
                config_bgLite(widg)
            elif widg.winfo_subclass() == 'LabelMovable':
                config_labelmovable(widg)

        elif widg.winfo_class() == 'Entry':

            if widg.winfo_subclass() in bgLite_fgStd_fontIn_insFg:
                config_bgLite_fgStd_fontIn_insFg(widg)

            elif widg.winfo_subclass() == 'LabelCopiable':
                config_labelcopiable(widg)

            # elif widg.winfo_subclass() in ('EntryUnhilited', 'EntryAutofill'):
                # config_unhilited_entry(widg)

            elif widg.winfo_subclass() in bgStd_fgStd_fontIn_insFg:
                config_bgStd_fgStd_fontIn_insFg(widg)

        elif widg.winfo_class() == 'Text':

            if widg.winfo_subclass() in bgLite_fgStd_fontIn_insFg:
                config_bgLite_fgStd_fontIn_insFg(widg)

            elif widg.winfo_subclass() in bgStd_fgStd_fontOut_disAbl:
                config_bgStd_fgStd_fontOut_disAbl(widg)

        elif widg.winfo_class() == 'Button':

            if widg.winfo_subclass() in ('Button', 'ButtonQuiet'):
                config_buttons(widg)

            elif widg.winfo_subclass() == 'ButtonPlain':
                config_buttons_plain(widg)

            elif widg.winfo_subclass() == 'ButtonFlatHilited':
                config_buttonflathilited(widg)

        elif widg.winfo_class() == 'Message':

            if widg.winfo_subclass() == 'Message':
                config_messages(widg)

            elif widg.winfo_subclass() == 'MessageHilited':
                config_messageshilited(widg)

        elif widg.winfo_class() in ('Radiobutton', 'Checkbutton'):

            if widg.winfo_subclass() == 'RadiobuttonHilited':
                config_radiobuttonhilited(widg)

            elif widg.winfo_subclass() in ('Radiobutton', 'Checkbutton'):
                config_radiobuttons(widg)

        elif widg.winfo_class() == 'Scale':
            config_scale(widg)

        elif widg.winfo_class() == 'Canvas':

            if widg.winfo_subclass() == 'Canvas':
                config_bgStd(widg)

            elif widg.winfo_subclass() == 'CanvasHilited':
                config_bgLite(widg)

            elif widg.winfo_subclass() == 'Border':
                widg.config(bg=formats['bg'])

            elif widg.winfo_subclass() == 'Scrollbar':
                # to figure out where all the scrollbars are:
                # print("line", looky(seeline()).lineno, "widg:", widg)
                # this is called in `styles.config_generic()`:
                widg.colorize()

    config_bgStd(parent)

def get_opening_settings():
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_opening_settings)
    user_formats = cur.fetchall()[0]
    cur.close()
    conn.close()
    return user_formats

def get_formats():
    '''
        Get user and default preferences. For any item, if there's no 
        user-preference, use the default.
    '''
    all_prefs = get_opening_settings()
    prefs_to_use = []
    x = 0
    for setting in all_prefs[0:7]:
        if setting is None or setting == '':
            prefs_to_use.append(all_prefs[x + 7])
        else:
            prefs_to_use.append(all_prefs[x])
        x += 1
    return prefs_to_use

def make_formats_dict():
    ''' 
        To add a style, add a string to the end of keys list
        and a line below values.append...
    '''

    prefs_to_use = get_formats()

# prefs_to_use e.g.: ['#232931', '#393e46', '#2E5447', '#eeeeee', 'courier', 'tahoma', 14]

    keys = [
        # background, foreground
        'bg', 'highlight_bg', 'table_head_bg', 'fg', 
        # standard fonts
        'output_font', 'input_font',
        # heading fonts
        'heading1', 'heading2', 'heading3', 'heading4', 
        # other fonts
        'status', 'boilerplate', 'show_font', 'titlebar_0',
        'titlebar_1', 'titlebar_2', 'titlebar_3',
        'titlebar_hilited_0', 'titlebar_hilited_1', 
        'titlebar_hilited_2', 'titlebar_hilited_3', 
        'unshow_font'
    ]

    values = []

    values.append(prefs_to_use[0])
    values.append(prefs_to_use[1])
    values.append(prefs_to_use[2])
    values.append(prefs_to_use[3])
    values.append((prefs_to_use[4], prefs_to_use[6]))
    values.append((prefs_to_use[5], prefs_to_use[6]))
    values.append((prefs_to_use[4], prefs_to_use[6]*2, 'bold'))
    values.append((prefs_to_use[4], int(prefs_to_use[6]*1.5), 'bold'))
    values.append((prefs_to_use[4], int(prefs_to_use[6]*1.08), 'bold'))
    values.append((prefs_to_use[4], int(prefs_to_use[6]*0.83), 'bold'))
    values.append((prefs_to_use[5], int(prefs_to_use[6]*0.83)))
    values.append((prefs_to_use[5], int(prefs_to_use[6]*0.66)))
    values.append((prefs_to_use[5], prefs_to_use[6], 'italic'))
    values.append((prefs_to_use[5], int(prefs_to_use[6]*0.66), 'bold'))
    values.append((prefs_to_use[5], int(prefs_to_use[6]*0.88), 'bold'))
    values.append((prefs_to_use[5], int(prefs_to_use[6]*1.00), 'bold'))
    values.append((prefs_to_use[5], int(prefs_to_use[6]*1.25), 'bold'))
    values.append((prefs_to_use[5], int(prefs_to_use[6]*0.66)))
    values.append((prefs_to_use[5], int(prefs_to_use[6]*0.88)))
    values.append((prefs_to_use[5], int(prefs_to_use[6]*1.00)))
    values.append((prefs_to_use[5], int(prefs_to_use[6]*1.25)))
    values.append((prefs_to_use[5], int(prefs_to_use[6]*.88), 'italic'))

    formats = dict(zip(keys, values))
    return formats

formats = make_formats_dict()

def get_color_schemes():
    conn = sqlite3.connect(current_file)
    cur=conn.cursor()
    cur.execute(select_all_color_schemes)
    schemes = cur.fetchall()
    cur.close()
    conn.close()
    return schemes

def get_color_schemes_plus():
    conn = sqlite3.connect(current_file)
    cur=conn.cursor()
    cur.execute(select_all_color_schemes_plus)
    schemes = cur.fetchall()
    cur.close()
    conn.close()
    return schemes
