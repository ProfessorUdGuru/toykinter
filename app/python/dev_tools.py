# dev_tools

import inspect as iii
import tkinter as tk    

looky = iii.getframeinfo
seeline = iii.currentframe
# to use:
# print(looky(seeline()).lineno)
# to get the real line no. do this if you want the value of x:
# x = 66
# print("line", looky(seeline()).lineno, "is", x)
# so I made a macro that types 
#     print("line", look(see()).lineno, "is", 
#     at the insertion cursor; just type the variable e.g. `x` and run the macro
# (Notepad Plus Plus might be the only free code editor that has a macro recorder.)