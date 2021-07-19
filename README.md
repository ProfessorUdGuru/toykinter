# toykinter
Custom Tkinter widgets made by inheriting from other Tkinter widgets.

The ttk widgets are harder to configure than the original Tkinter widgets which are easy to configure by class. The purpose of the Toykinter project is to provide easily configurable widgets such as tabbed pages, combobox, optionally auto-hiding scrollbar, title bar, window border/sizer, autofill entries, sizegrip, tooltips, and more. Modules for instantly reconfiguring colors and fonts for every widget in the application are also provided.

This repo is a demo app comprising working models for most of the Toykinter widget and code for other widgets that needs to be finished, fixed, or refactored. A do list is at the bottom of the Docs tab in the demo app. To suggest improvements, do list items, etc., send me a message. I'm busy with other things but I will be making additions to the do list.

I'm using Python 3.9 with Pillow installed. `pip install Pillow` worked for me on 3.8 and 3.9 in spite of the scary words on the docs if you look into Pillow's dependencies. I didn't have to do anything about Pillow's dependencies.

I found out the hard way that tracking a database on github is not worth the trouble or not possible, I'm not sure which. I'm using SQLite, but these schemas should work for any SQL database. Below the schema for the tables I'll also give the table contents that are current for the code in the repo.

## Database (toykinter/data/toykinter/toykinter.db)

```
sqlite> .tables
closing_state  color_scheme   format
sqlite> .schema closing_state
CREATE TABLE closing_state (closing_state_id INTEGER PRIMARY KEY AUTOINCREMENT, current_database TEXT DEFAULT null);
sqlite> .schema format
CREATE TABLE format (format_id INTEGER PRIMARY KEY AUTOINCREMENT, bg TEXT, highlight_bg TEXT, head_bg TEXT, fg TEXT, output_font TEXT, input_font TEXT, font_size INTEGER, default_bg TEXT NOT NULL DEFAULT '#393932', default_highlight_bg TEXT NOT NULL DEFAULT '#4d4545', default_head_bg TEXT NOT NULL DEFAULT '#8d6262', default_fg TEXT NOT NULL DEFAULT '#f1c5c5', default_output_font TEXT NOT NULL DEFAULT 'courier', default_input_font TEXT NOT NULL DEFAULT 'tahoma', default_font_size INTEGER NOT NULL DEFAULT 12);
sqlite> .schema color_scheme
CREATE TABLE IF NOT EXISTS "color_scheme" (color_scheme_id INTEGER PRIMARY KEY AUTOINCREMENT, bg TEXT NOT NULL, highlight_bg TEXT NOT NULL, head_bg TEXT NOT NULL, fg TEXT NOT NULL, built_in BOOLEAN NOT NULL DEFAULT 01, hidden BOOLEAN NOT NULL DEFAULT 0);
sqlite>

sqlite> select * from closing_state;
closing_state_id|current_database
1|toykinter.db
sqlite> select * from format;
format_id|bg|highlight_bg|head_bg|fg|output_font|input_font|font_size|default_bg|default_highlight_bg|default_head_bg|default_fg|default_output_font|default_input_font|default_font_size
1|#232931|#393e46|#2E5447|#eeeeee|courier|tahoma|13|#232931|#393e46|#2e5447|#eeeeee|courier|tahoma|12
sqlite> select * from color_scheme;
color_scheme_id|bg|highlight_bg|head_bg|fg|built_in|hidden
1|#232931|#393e46|#2E5447|#eeeeee|1|0
2|#393932|#4d4545|#8d6262|#f1c5c5|1|0
3|#212121|#323232|#0d7377|#7efee1|1|0
4|#423030|#605656|gray|lightgray|1|0
203|#51605f|#3f4948|#2e3433|#a9b4b1|1|0
205|#35483a|#647d73|#7e6373|#c8b9c1|1|0
206|#35483a|#647d73|#4d444b|#c8b9c1|1|0
207|#a2b48d|#87baac|#ddac64|#151580|1|0
208|#34615f|#4a8a87|#486a8c|#b9ddd9|1|0
213|#a2b48d|#87baac|#c5997c|#151580|1|0
214|#b5fdfd|#57fbfb|#fbbbfd|black|1|0
216|#344140|#5a7270|#977d77|#ffffff|1|0
217|#1e1e1e|#484848|#43523f|#d7d7d7|1|0
218|#b8a089|#cbbaa9|#ded3c9|#2d241c|1|0
220|#0C1021|#55606c|#808c9b|white|1|0
221|#524d7d|#7a75aa|#83989c|white|1|0
222|#283133|#899ea3|#86a68b|white|1|0
223|#2F343F|#424242|#212121|#AFB9C6|1|0
225|#38555f|#507987|#4d598a|#b0b7d2|1|0
226|#151a26|#3d4b6d|#6c8093|#bac4cd|1|0
228|#152028|#232b32|#202945|#9da3b7|1|0
230|#121212|#606782|#5a7a87|#99b0bb|1|0
231|#121212|#403250|#506985|#94a8be|1|0
233|#dbdde8|#b4b8cf|#8087ae|#424766|1|0
234|#bcd0d3|#97b7bb|#639196|#2c3f41|1|0
235|#2b3237|#48535b|#677783|#d3d9dc|1|0
236|#061D3F|#284b80|#267d82|#71cfd5|1|0
sqlite>
```
