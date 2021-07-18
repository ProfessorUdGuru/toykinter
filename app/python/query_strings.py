# query_strings.py


'''
	Since Sqlite queries are inserted as string in Python code,
	the queries can be stored here to save space in the modules
	where they are used.
'''

delete_color_scheme = '''
    DELETE FROM color_scheme 
    WHERE color_scheme_id = ?
'''

insert_color_scheme = '''
    INSERT INTO color_scheme 
    VALUES (null, ?, ?, ?, ?, 0, 0)
'''

select_all_color_schemes = '''
    SELECT bg, highlight_bg, head_bg, fg 
    FROM color_scheme
'''

select_all_color_schemes_plus = '''
    SELECT bg, highlight_bg, head_bg, fg, built_in, color_scheme_id 
    FROM color_scheme
'''

select_color_scheme_current = '''
    SELECT bg, highlight_bg, head_bg, fg 
    FROM format 
    WHERE format_id = 1
'''

select_current_database = '''
    SELECT current_database 
    FROM closing_state 
    WHERE closing_state_id = 1
'''

select_font_scheme = '''
    SELECT font_size, output_font, input_font
    FROM format
    WHERE format_id = 1
'''

select_opening_settings = '''
    SELECT 
        bg,
        highlight_bg,
        head_bg, 
        fg,
        output_font,
        input_font, 
        font_size,
        default_bg,
        default_highlight_bg,
        default_head_bg, 
        default_fg,
        default_output_font,
        default_input_font, 
        default_font_size            
    FROM format
    WHERE format_id = 1
'''

update_color_scheme_null = '''
    UPDATE format 
    SET (bg, highlight_bg, head_bg, fg) = 
        (null, null, null, null) 
                WHERE format_id = 1
'''

update_current_database = '''
    UPDATE closing_state 
    SET current_database = ? 
    WHERE closing_state_id = 1
'''

update_format_color_scheme = '''
    UPDATE format 
    SET (bg, highlight_bg, head_bg, fg) = (?, ?, ?, ?) 
    WHERE format_id = 1 
'''

update_format_fonts = '''
    UPDATE format 
    SET (font_size, output_font, input_font) = (?, ?, ?) 
    WHERE format_id = 1
'''







