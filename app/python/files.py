# files.py

from sys import argv
from os import path
import tkinter as tk
import sqlite3
from query_strings import select_current_database
from dev_tools import looky, seeline



current_path = argv[0]
split_path = path.splitdrive(current_path)
current_drive = '{}\\'.format(split_path[0])
current_database = '{}toykinter/data/toykinter/toykinter.db'.format(current_drive)
project_path = '{}toykinter/app/python/'.format(current_drive)

def get_current_file():
    conn = sqlite3.connect(current_database)
    cur = conn.cursor()
    cur.execute(select_current_database)
    cur_tup = cur.fetchone()

    if cur_tup:
        cur_tup = cur_tup[0]
    else:
        cur_tup = ''

    if cur_tup == 'default_database.db':
        current_file = cur_tup
        current_dir = '{}toykinter/data/settings'.format(
            current_drive)

    elif len(cur_tup) > 0:
        current_dir = cur_tup.rstrip('.db')
        current_file = '{}toykinter/data/{}/{}'.format(
            current_drive, current_dir, cur_tup)
    else:
        current_file = ''
    cur.close()
    conn.close()
    file_ok = path.exists(current_file)
    if file_ok is False:
        valid_dummy = 'default_database.db'
        # last-used db was moved/deleted outside of Toykinter controls,
        #    so don't let sqlite make a blank db by that name
        set_current_file(valid_dummy)
        current_file = '{}toykinter/data/settings/{}'.format(
            current_drive, valid_dummy)
        current_dir = '{}toykinter/data/settings'.format(
            current_drive)
    return current_file, current_dir
current_file, current_dir = get_current_file()

def set_current_file(new_current_file):
    if new_current_file.strip() != '':
        current_file = new_current_file
        conn = sqlite3.connect(current_database)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_current_database, (current_file,))
        conn.commit()
        cur.close()
        conn.close()








