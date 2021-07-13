import tkinter as tk
from PIL import Image, ImageTk
import tkinter as tk
from files import project_path
from window_border import Border
from scrolling import MousewheelScrolling
from styles import config_generic
from main import Main
from widgets import Toplevel
from dev_tools import looky, seeline




class Toykinter():
    def __init__(self, view):
        self.view = view
        self.make_main_canvas_and_border()
        self.configure_mousewheel_scrolling()

        config_generic(self.view)

    def make_main_canvas_and_border(self):
        self.canvas = Border(
            self.view, 
            size=3, 
            menubar=True, 
            ribbon_menu=True)
        self.main = Main(self.canvas, self.view, self)
        self.canvas.create_window(0, 0, anchor='nw', window=self.main)

    def configure_mousewheel_scrolling(self):
        self.scroll_mouse = MousewheelScrolling(self.view, self.canvas)
        self.scroll_mouse.append_to_list([self.canvas, self.main])
        self.scroll_mouse.configure_mousewheel_scrolling(in_root=True)

def main():

    def withdraw_new_root(event): 
        view.withdraw()

    def show_new_root(event): 
        view.deiconify()

    def make_taskbar_flyout_image():
        width = 600
        height = 300
        flyout_pic_file = '{}images/old_typewriter.png'.format(
            project_path)
        pil_img = Image.open(flyout_pic_file)
        tk_img = ImageTk.PhotoImage(pil_img)
        flyout_canvas = tk.Canvas(icon, height=height, width=width)
        flyout_canvas.create_image(0, 0, anchor='nw', image=tk_img)
        flyout_canvas.grid()
        flyout_canvas.image = tk_img

    def configure_root():
        icon.title('TOYKINTER')
        # set size to size of image and move off screen
        icon.geometry('600x300+-2500+0')
        icon.focus_set() # so one click on taskbar icon gets result
        icon.attributes("-alpha", 0.0)
        icon.iconbitmap(default='{}favicon.ico'.format(project_path)) 
        icon.bind("<Unmap>", withdraw_new_root)
        icon.bind("<Map>", show_new_root)

    icon = tk.Tk()

    view = tk.Toplevel(icon, name='view')
    view.geometry('+100+50')
    view.overrideredirect(1)

    Toykinter(view)

    make_taskbar_flyout_image()
    configure_root()

    icon.mainloop()

if __name__ == '__main__':
    main()

