import tkinter as tk
import sqlite3
from files import current_file
from query_strings import(
    select_opening_settings, select_all_color_schemes,
    select_all_color_schemes_plus)
from dev_tools import looky, seeline




MAX_WINDOW_HEIGHT = 0.95
MAX_WINDOW_WIDTH = 0.995
NEUTRAL_COLOR = '#878787'

'''
    widget.winfo_class() is a built-in Tkinter method that
    refers to Tkinter classes such as 'Label' or ttk classes
    such as 'TLabel'. widget.winfo_subclass() is a custom
    method that refers to subclasses such as 'Label' that 
    this app creates by inheriting from Tkinter. The purpose 
    of this module is to do with Tkinter widgets what they
    are saying can only be done with ttk widgets: configure
    widgets by class instead of one at a time. This is supposed
    to replace or make unnecessary ttk.Style and Windows themes,
    using methods that novice coders can understand easily while 
    getting predictable results, whereas ttk widgets fall short 
    in that regard.

    The worst thing about this method of reconfiguring values is that
    if you accidentally use a tkinter widget like this: "lab = tk.Label..."
    you'll get an error like this... so don't use any tk.widgets:
    Traceback (most recent call last):
      File "C:\treebard_gps\app\python\ccccc.py", line 33, in <module>
        ST.config_generic(root)
      File "C:\treebard_gps\app\python\styles.py", line 449, in config_generic
        widg.winfo_subclass() == 'LabelStay'):
    AttributeError: 'Label' object has no attribute 'winfo_subclass'

    To use this method of configuration by detecting subclasses, you have to
    remember to not use the parent tkinter classes, only the subclasses.
'''
'''
   Groups of widgets that take common formatting changes
   when user changes a style preference. If a subclass
   fits in one of these groups just add its class name
   to one of these tuples. Otherwise it has to be added
   to the switch in config_generic() and given a 
   subfunction there to configure it. Only options that
   can be changed by user need to be handled here, like
   fg, bg, and font. The intended result is no styling
   in the widget construction code since all styles are
   built into class names.
'''

# change background to formats['bg']:
bg_only_bg = (
    'Frame', 'DatePrefsWidgets', 'PersonsTab', 
    'NamesTab', 'Treebard', 'IconMenu', 'Main', 
    'StatusBarTooltips', 'Colorizer', 'Search', 
    'Notebook', 'Toplevel', 'LabelEntryPair', 
    'PersonAdd', 'EditablePairs', 'LabelGoTo',
    'CanvasScrolledBG1')

# change background to formats['table_head_bg']:
bg_only_table_head = ('FrameHilited2',)

# change background to formats['highlight_bg']:
bg_only_hilited = (
    'FrameHilited', 'FrameHilited1', 'FrameHilited4', 
    'LabelTitleBar', 'Sizer', 'KinTip', 'ToolTip',
    'ToplevelHilited', 'CanvasScrolledBG2')

# change background, foreground to standard:
bg_fg_only_standard = ('Label', 'LabelFrame', 'Sizer')

# change background, foreground to standard and font to input
bg_fg_standard_font_input = (
    'Table', 'FindingsTable', 'AttributesTable', 'LabelEntrylike')

# change background, foreground to standard,
#    font to output, and normally disabled:    
bg_fg_font_state_disabled = ('LabelStylable', 'MessageCopiable')

class ThemeStyles:
    def __init__(self, app=None):

        self.root = app

    def create_custom_theme(self):
        ''' 
            Customize all widgets with the push of a button
            without using any ttk widgets or ttk.Style. See 
            ttk_notebook_vs_button_theme_showcase.py
            for voluminous notes and demo re: theme choices,
            a study which was necessitated by the inconsistencies
            of something called ttk which was created to court
            Windows themes when in fact Tkinter worked fine
            before that move was made.
        '''

        formats = make_formats_dict() # this replaces a whole bunch of ttk nonsense

    '''
        The variable formats can't be global in this module because
        these are reconfiguration functions and the
        colors that are current when this module first loads
        are now wrong when the recolorizer runs. A global variable
        would only run once when this module is imported so the
        little config functions have been nested inside of the 
        main config_generic() in order to prevent connecting to the db
        once for each of the little functions.
    '''

    def get_all_descends (self, ancestor, deep_list):
        ''' 
            So all widgets can be configured at once,
            this lists every widget in the app by running
            recursively.
        '''

        lst = ancestor.winfo_children()        
        for item in lst:
            deep_list.append(item)
            self.get_all_descends(item, deep_list)
        return deep_list

    def config_generic(self, parent):
        ''' 
            Call this for every Toplevel window constructed 
            to apply consistent styling to tkinter widgets
            so widgets don't have to be styled individually.
            Instantiate this class in each module where widgets
            are made: TS = ThemeStyles() When all widgets have 
            been constructed add this line: TS.config_generic(parent).
            This is also called in colorizer to change the color of 
            everything instantly. '''

        def config_labelhilited(lab):
            lab.config(
                bg=formats['highlight_bg'],
                fg=formats['fg'])

        def config_labelhilited2(lab):
                bg=formats['table_head_bg']
                fg=formats['fg']

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
                fg=formats['bg'])

        def config_labelstay2(lab):
            lab.config(fg=formats['fg'])

        def config_heading1(lab):
            lab.config(bg=formats['bg'], 
            fg=formats['fg'], 
            font=formats['heading1'])

        def config_heading2(lab):
            lab.config(bg=formats['bg'], 
            fg=formats['fg'], 
            font=formats['heading2'])

        def config_heading3(lab):
            lab.config(bg=formats['bg'], 
            fg=formats['fg'], 
            font=formats['heading3'])

        def config_heading4(lab):
            lab.config(bg=formats['bg'], 
            fg=formats['fg'], 
            font=formats['heading4'])
            
        def config_boilerplate(lab):
            lab.config(
                bg=formats['bg'], 
                fg=formats['fg'], 
                font=formats['boilerplate'])

        def config_labelcolumn(lab):
            lab.config(
                bg=formats['bg'], 
                fg=formats['fg'], 
                font=formats['heading3'],
                anchor='w')

        def config_labelcolumnctr(lab):
            lab.config(
                bg=formats['table_head_bg'], 
                fg=formats['fg'], 
                font=formats['heading3'],
                anchor='center') 

        # ************* special event widgets ********************

        # widgets that have highlight/unhighlight events need some
        #    special treatment to keep up with changes of the
        #    color scheme. In the class definition do this:
        # self.formats = make_formats_dict()
        # And in the highlight/unhighlight methods do this:
        # bg=self.formats['blah'] ...instead of bg=formats['blah']
        # And give them their very own config function here:

        def config_notebook_tabs(lab):
            lab.formats = formats # bec. of color change on click
            lab.config(
                bg=formats['highlight_bg'],
                fg=formats['fg'])

        def config_labelsearch(lab):
            lab.formats = formats
            lab.config(
                bg=formats['bg'], 
                fg=formats['fg'])

        def config_labeldots(lab):
            lab.formats = formats # bec. of Enter/Leave...
            lab.config(
                bg=formats['bg'],
                fg=formats['fg'])

        def config_labelmovable(lab):
            lab.formats = formats # bec. of FocusIn/FocusOut...
            lab.config(
                bg=formats['highlight_bg'],
                font=formats['output_font'], 
                fg=formats['fg'])

        def config_entrydefaulttext(ent):
            ent.formats = formats # bec. of FocusIn/FocusOut...
            ent.config(
                background=formats['highlight_bg'],
                font=formats['show_font'])

        # ***********************************

        def config_buttons(button):
            button.config(
                font=(formats['output_font']),
                activebackground=formats['table_head_bg'],
                bg=formats['bg'],  
                fg=formats['fg'])

        def config_buttons_plain(button):
            button.config(
                font=(formats['input_font']),
                activebackground=formats['table_head_bg'],
                bg=formats['bg'],  
                fg=formats['fg'])

        def config_buttonflathilited(button):
            button.config(
                bg=formats['highlight_bg'],
                fg=formats['fg'],
                activebackground=formats['fg'],
                activeforeground=formats['bg'])

        def config_radiobuttons(radio):
            radio.config(
                bg=formats['bg'], 
                activebackground=formats['highlight_bg'],
                fg=formats['fg'],
                selectcolor=formats['highlight_bg']) 

        def config_radiobuttonhilited(radio):
            radio.config(
                bg=formats['highlight_bg'], 
                activebackground=formats['bg'],
                fg=formats['fg'],
                selectcolor=formats['bg']) 

        def config_fg_standard(widg):
            widg.config(fg=formats['fg'])

        def config_bg_only_bg(widg):
            widg.config(bg=formats['bg'])

        def config_bg_only_hilited(widg):
            widg.config(bg=formats['highlight_bg'])
           
        def config_bg_only_table_head(widg):
            widg.config(bg=formats['table_head_bg'])

        def config_bg_fg_only_standard(widg):
            widg.config(bg=formats['bg'], fg=formats['fg'])

        def config_separator(sep):
            ''' 
                has 3 frames with 3 different colors
                so needs its own reconfigure method 
            '''
            sep.colorize() 
        
        # this and more was needed for ttk.Combobox, just replace this
        def config_combos(ent):
            ent.config(font=formats['input_font']) 

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

        def config_buttonlabel(widg):
            widg.config(
                bg=formats['bg'],
                fg=formats['fg'],
                font=formats['input_font'])

        def config_labeldots(widg):
            widg.config(
                bg=formats['bg'],
                fg=formats['fg'],
                font=formats['heading3'])

        def config_labelcopiable(widg):
            widg.config(state='normal')
            widg.config(
                bg=formats['bg'], 
                fg=formats['fg'])
            widg.config(state='readonly')
            widg.config(readonlybackground=widg.cget('background'))

        def config_entry(widg):
            widg.config(
                bg=formats['highlight_bg'],
                fg=formats['fg'],
                font=formats['input_font'],
                insertbackground=formats['fg'],
                disabledbackground=formats['highlight_bg'],
                disabledforeground=formats['fg'])

        def config_scale(widg):
            widg.config(
                bg=formats['bg'], 
                fg=formats['fg'], 
                font=formats['output_font'],
                troughcolor=formats['highlight_bg'],
                activebackground=formats['table_head_bg'])

        def config_unhilited_entry(widg):
            widg.config(
                bd=0,
                bg=formats['bg'], 
                fg=formats['fg'], 
                font=formats['input_font'], 
                insertbackground=formats['fg'],
                disabledbackground=formats['bg'],
                disabledforeground=formats['fg'])

        def config_bg_fg_standard_font_input(widg):
            widg.config(
                bg=formats['bg'],
                fg=formats['fg'],
                font=formats['input_font'],
                insertbackground=formats['fg'],
                disabledbackground=formats['highlight_bg'],
                disabledforeground=formats['fg'])

        def config_bg_fg_font_state_disabled(widg):
            widg.config(state='normal')
            widg.config(
                bg=formats['bg'],
                fg=formats['fg'],
                font=formats['output_font'])
            widg.config(state='disabled')

        def config_text(widg):
            widg.config(
                bg=formats['bg'],
                fg=formats['fg'],
                insertbackground=formats['fg'])

        formats = make_formats_dict()

        ancestor_list = []
        all_widgets_in_root = self.get_all_descends(
            parent, ancestor_list)

        for widg in (all_widgets_in_root):
            if (widg.winfo_class() == 'Label' and 
                widg.winfo_subclass() == 'LabelStay'):
                    pass

            elif widg.winfo_class() == 'Frame':
                if widg.winfo_subclass() == 'FrameStay':
                    pass

                elif widg.winfo_subclass() in bg_only_bg:
                    config_bg_only_bg(widg)

                elif widg.winfo_subclass() in bg_only_table_head:
                    config_bg_only_table_head(widg)

                elif widg.winfo_subclass() in bg_only_hilited:
                    config_bg_only_hilited(widg)

                elif widg.winfo_subclass() == 'TabBook':
                    config_bg_only_hilited(widg)

                elif widg.winfo_subclass() == 'Separator':
                    config_separator(widg)

                elif widg.winfo_subclass() == 'EntryDefaultText':
                    config_entrydefaulttext(widg)
            
            # tk.Label is class
            elif widg.winfo_class() == 'Label':
                # widgets.Label is subclass
                if widg.winfo_subclass() in bg_fg_only_standard: # new way
                    config_bg_fg_only_standard(widg)
                elif widg.winfo_subclass() == 'LabelStay2':
                    config_labelstay2(widg)
                elif widg.winfo_subclass() == 'LabelH2': # old way
                    config_heading2(widg)
                elif widg.winfo_subclass() == 'LabelH3':
                    config_heading3(widg)
                elif widg.winfo_subclass() == 'LabelColumnCenter':
                    config_labelcolumnctr(widg)
                elif widg.winfo_subclass() == 'LabelColumn':
                    config_labelcolumn(widg)
                elif widg.winfo_subclass() == 'LabelBoilerplate':
                    config_boilerplate(widg)
                elif widg.winfo_subclass() == 'LabelItalic':
                    config_labelitalic(widg)
                elif widg.winfo_subclass() == 'LabelButtonText':
                    config_buttonlabel(widg)
                elif widg.winfo_subclass() == 'LabelHilited':
                    config_labelhilited(widg)
                elif widg.winfo_subclass() == 'LabelHilited2':
                    config_labelhilited2(widg)
                elif widg.winfo_subclass() == 'LabelHilited3':
                    config_notebook_tabs(widg)
                elif widg.winfo_subclass() == 'LabelTip':
                    config_labeltip(widg)
                elif widg.winfo_subclass() == 'LabelTip2':
                    config_labeltip2(widg)
                elif widg.winfo_subclass() == 'LabelTipBold':
                    config_labeltipbold(widg)
                elif widg.winfo_subclass() == 'LabelNegative':
                    config_labelnegative(widg)
                elif widg.winfo_subclass() == 'LabelSearch':
                    config_labelsearch(widg)
                elif widg.winfo_subclass() == 'LabelDots':
                    config_labeldots(widg)
                elif widg.winfo_subclass() == ('TitleBarButtonSolidBG'):
                    config_bg_only_hilited(widg)
                elif widg.winfo_subclass() == 'LabelMovable':
                    config_labelmovable(widg)
                elif widg.winfo_subclass() in bg_only_table_head:
                    config_bg_only_table_head(widg)

            elif widg.winfo_class() == 'Entry':
                if widg.winfo_subclass() in bg_fg_standard_font_input:
                    config_bg_fg_standard_font_input(widg)
                elif widg.winfo_subclass() == 'LabelCopiable':
                    config_labelcopiable(widg)
                elif widg.winfo_subclass() in ('Entry', 'EntryAutofillHilited'):
                    config_entry(widg)
                elif widg.winfo_subclass() in ('EntryUnhilited', 'EntryAutofill'):
                    config_unhilited_entry(widg)

            elif widg.winfo_class() == 'TCombobox':
                config_combos(widg)

            elif widg.winfo_class() == 'Text':
                if widg.winfo_subclass() in bg_fg_standard_font_input:
                    config_text(widg)
                elif widg.winfo_subclass() in bg_fg_font_state_disabled:
                    config_bg_fg_font_state_disabled(widg)

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
                    config_bg_only_bg(widg)
                elif widg.winfo_subclass() == 'CanvasHilited':
                    config_bg_only_hilited(widg)
                elif widg.winfo_subclass() == 'PedigreeChart':
                    widg.config(bg=formats['bg'])
                    for obj in widg.find_all():
                        widg.itemconfigure(obj, fill=formats['fg'])                 
                        if widg.itemcget(obj, 'tags') == 'current_person':
                            widg.itemconfigure(obj, fill=formats['table_head_bg'])
                elif widg.winfo_subclass() == 'Scrollbar':
                    widg.colorize()
            elif widg.winfo_class() in ('Frame', 'Toplevel', 'Canvas'):
                config_bg_only_bg(widg)

        config_bg_only_bg(parent) # important

    def set_window_max_size(self, parent):

        if parent.winfo_class() == 'Toplevel':
            parent.maxsize(
                width=int(
                    parent.winfo_screenwidth()*MAX_WINDOW_WIDTH), 
                height=int(
                    parent.winfo_screenheight()*MAX_WINDOW_HEIGHT))

def get_opening_settings():
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_opening_settings)
    user_formats = cur.fetchall()[0]
    cur.close()
    conn.close()
    return user_formats

def get_formats():
    results = get_opening_settings()
    use_results = []
    x = 0
    for setting in results[0:7]:
        if setting is None or setting == '':
            use_results.append(results[x + 7]) # get default if no user setting
        else:
            use_results.append(results[x])
        x += 1
    return use_results

def make_formats_dict():
    ''' 
        To add a style, add a string to the end of keys list
        and a line below values.append... 
    '''

    use_results = get_formats()

# use_results: ['#232931', '#393e46', '#2E5447', '#eeeeee', 'courier', 'tahoma', 14]

    keys = [
        'bg', 'highlight_bg', 'table_head_bg', 
        'fg', 'output_font', 'input_font', 
        'heading1', 'heading2', 'heading3', 'heading4', 
        'status', 'boilerplate', 'show_font', 'titlebar_0',
        'titlebar_1', 'titlebar_2', 'titlebar_3',
        'titlebar_hilited_0', 'titlebar_hilited_1', 
        'titlebar_hilited_2', 'titlebar_hilited_3', 'unshow_font'
    ]
    values = []

    values.append(use_results[0])
    values.append(use_results[1])
    values.append(use_results[2])
    values.append(use_results[3])
    values.append((use_results[4], use_results[6]))
    values.append((use_results[5], use_results[6]))
    values.append((use_results[4], use_results[6]*2, 'bold'))
    values.append((use_results[4], int(use_results[6]*1.5), 'bold'))
    values.append((use_results[4], int(use_results[6]*1.08), 'bold'))
    values.append((use_results[4], int(use_results[6]*0.83), 'bold'))
    values.append((use_results[5], int(use_results[6]*0.83)))
    values.append((use_results[5], int(use_results[6]*0.66)))
    values.append((use_results[5], use_results[6], 'italic'))
    values.append((use_results[5], int(use_results[6]*0.66), 'bold'))
    values.append((use_results[5], int(use_results[6]*0.88), 'bold'))
    values.append((use_results[5], int(use_results[6]*1.00), 'bold'))
    values.append((use_results[5], int(use_results[6]*1.25), 'bold'))
    values.append((use_results[5], int(use_results[6]*0.66)))
    values.append((use_results[5], int(use_results[6]*0.88)))
    values.append((use_results[5], int(use_results[6]*1.00)))
    values.append((use_results[5], int(use_results[6]*1.25)))
    values.append((use_results[5], int(use_results[6]*.88), 'italic'))

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
