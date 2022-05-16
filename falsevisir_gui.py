#!/usr/bin/env python3
import time
time0 = time.time()
import logging
import sys
from subprocess import run
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path, PurePath, WindowsPath, PosixPath
from pprint import pprint

import numpy as np
from PIL import Image, ImageTk
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
from imageio import imwrite

from falsevisir import process_pair
from find_files import get_files_dict



INDIRS  =  "/home/m/Y/SKENY/VIS/", "/home/m/Y/APOLLO/2021/"

CANVAS_SIZE = 200,150

BUTTONS = """
        Open file_open
        """

COMMANDS = {
        # "File":"""
# 
                # Quit q file_quit
                # """,
                    }





class MainWin:

    def __init__(self, master, commands=COMMANDS, buttons=BUTTONS, canvas_size=CANVAS_SIZE):

        # super().__init__(master)

        self.master = master
        
        self.itemid = None
        self._vis_dict = None
        self._irr_dict = None
        
        self.vi_path=(Path("."))
        self.ir_path=(Path("."))
        # self.screen_size = self.winfo_screenheight(), self.winfo_screenwidth()  # screensize - monitors combined
#        logging.info(self.screen_size)
        
        # self.commands = {k:self._text_to_2dlist(v) for k,v in commands.items()}
        # self.buttons = self._text_to_2dlist(buttons)  
        # self.hotkeys = self._hotkeys_dict(self.commands)
                
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
        # self.master.bind("<F4>", lambda x: self._widget_toggle("sidebar"))
        # self.master.bind("<F5>", lambda x: self._menubar_toggle())
        # self.master.bind("<F6>", lambda x: self._widget_toggle("statusbar"))
        
        s = ttk.Style(master)
        s.configure('TFrame', background='slategray')
        self.win = ttk.Frame(master) 

        
        # TOOLBAR
        BUTTON_WIDTH = 10
        self.toolbar = ttk.Frame(self.win)
        # self.toolbar = tk.Frame(self.win, bg="lightgreen")
        ttk.Button(self.toolbar, text='Open VIS', width=BUTTON_WIDTH, command=self.open_vis).pack(side="left")
        ttk.Button(self.toolbar, text='Open IRR', width=BUTTON_WIDTH, command=self.open_irr).pack(side="left")
        ttk.Button(self.toolbar, text='Find files', width=BUTTON_WIDTH, command=self.find_files).pack(side="left")
        ttk.Button(self.toolbar, text='RUN', width=BUTTON_WIDTH, command=self.run).pack(side="left")
        ttk.Button(self.toolbar, text='SAVE', width=BUTTON_WIDTH, command=self.save).pack(side="left")
        ttk.Button(self.toolbar, text='QUIT', width=BUTTON_WIDTH, command=self.quit).pack(side="left")
        self.toolbar.pack(fill="x",  side="top", expand=0,  anchor="nw")
        
        # CANVAS
        self.canvas = ttk.Frame(self.win)
        # self.canvas = tk.Frame(self.win, bg="lightblue")
        
        self.canvas.pack(fill="both", side="left", expand=1,  anchor="nw")
        
        self.canvas1 = tk.Canvas(self.canvas, bg="grey")
        self.canvas2 = tk.Canvas(self.canvas, bg="grey")
        self.canvas3 = tk.Canvas(self.canvas, bg="grey")
        self.canvas1.pack(fill="both",  side="left", expand=1, anchor="nw")
        self.canvas2.pack(fill="both",  side="left", expand=1,  anchor="nw")
        self.canvas3.pack(fill="both",  side="left", expand=1,  anchor="nw")
        self.win.pack(fill="both",  side="left", expand=1, anchor="nw")    

    @property
    def irr_dict(self):
        if not self.itemid:
            self.itemid = askstring("Najít soubory", "Zadej ID objektu (např. J2154)")
        if not self._irr_dict:
            self._irr_dict = get_files_dict(INDIRS[1], extensions=[".png"], id_pattern=r".*?_(\w{5})_.*")
        pprint(self._irr_dict)
        return self._irr_dict

    @property
    def vis_dict(self):
        if not self.itemid:
            self.itemid = askstring("Najít soubory", "Zadej ID objektu (např. J2154)")
        if not self._vis_dict:
            self._vis_dict = get_files_dict(INDIRS[0], extensions=[".tif"], id_pattern=r"(\w{5}).*", exclude=r".*(spod|zad|reverz|rub).*")  # exclude zadni strana
        pprint(self._vis_dict)
        return self._vis_dict

    def open_vis(self):
        print("open VIS")
        self.vi_path = Path(self.ask_image(initialdir=self.vi_path.parent))
        im = Image.open(self.vi_path)
        self.im1 = self.load_image(self.canvas1, im)
        
    def open_irr(self):
        print("open IRR")
        self.ir_path = Path(self.ask_image(initialdir=self.ir_path.parent))
        im = Image.open(self.ir_path)
        self.im2 = self.load_image(self.canvas2, im)
        
    def find_files(self):
        print("find files")
        
        self.itemid = askstring("Najít soubory", "Zadej ID objektu (J....)", initialvalue="J2159").lower()
        
        if self.itemid not in self.irr_dict: 
            showinfo("Najít soubor", f"IRR image not found: {self.itemid}")
            return
        
        elif self.itemid not in self.vis_dict:    
            showinfo("Najít soubor", f"VIS image not found: {self.itemid}")
            return

        self.ir_path = self.irr_dict[self.itemid]
        self.vi_path = self.vis_dict[self.itemid]
            
        im = Image.open(self.vi_path)
        self.im1 = self.load_image(self.canvas1, im)
        
        
        im = Image.open(self.ir_path)
        self.im2 = self.load_image(self.canvas2, im)

        
        # im = Image.open(self.ir_path)
        # self.im2 = self.load_image(self.canvas2, im)

        
        
        
        
    def run(self):
        print("RUN")
        # self.canvas3 = tk.Canvas(self.canvas, bg="grey")
        # self.canvas3.pack(fill="both",  side="left", expand=1,  anchor="nw")
        # self.canvas3.delete("all")
        # if hasattr(self, "im3"):
            # self.canvas3.delete(self.im3)
            
        _, _, _, self.irfc = process_pair(self.vi_path, self.ir_path, show=False, save=False)
        ir = np.array(255*self.irfc).astype(np.uint8)
        # print(ir)
        self.im3 = self.load_image(self.canvas3, Image.fromarray(ir))
        
    def save(self):
        print("SAVE")
        print(self.irfc.dtype, self.irfc.max())
        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        print(f, f.name)
        imwrite(f.name, self.irfc)
        
        
    def quit(self):
        logging.info("quit mainwin loop")
        self.master.quit()  # exit mainloop

    def view_fullscreen(self):
        self.attributes('-fullscreen', not self.attributes('-fullscreen'))

    def get_wid_size(self, widget):
        return  widget.winfo_width(), widget.winfo_height()

    def load_image(self, widget, im):
        size = widget.winfo_width(), widget.winfo_height()
        im = self.img_to_8bit(im)  
        print("PIL image loaded:", im.format, im.mode)                 
        im.thumbnail(size)
        im_photo = ImageTk.PhotoImage(im)
        widget.create_image(0, 0, image=im_photo, anchor="nw")
        return im_photo
   
    def img_to_8bit(self, im):
        if im.mode == "I":
            im = Image.fromarray(np.array(im)//256)
        return im
        
    def ask_image(self, *a, **kw):
        return filedialog.askopenfilename(
                           filetypes =(("Image", ".jpg .jpeg .png .tiff .tif .gif .bmp"),("All Files","*.*")),
                           title = "Choose a file", 
                           *a, **kw)
# FILE --------------------------------------------------------

    def file_open(self):
        logging.info("file_open")
        fpath = tk.filedialog.askopenfilename()
        if fpath:
            self.load_image(fpath)


#  ------------------------------------------
#  MAIN
#  ------------------------------------------

if __name__ == '__main__':

    logging.basicConfig(level=20,
        format='!%(levelno)s [%(module)10s%(lineno)4d]\t%(message)s')
    logging.info(f"imports done \t{time.time()-time0:.2f} s")

    #memory_limit(.8)  # use max 80% of ram

    root = tk.Tk()
    
    root.title("FalseVisir")
    
    root.geometry("1200x800")
    
    app = MainWin(root, buttons=BUTTONS, commands=COMMANDS)



    logging.info(f"mainloop started \t{time.time()-time0:.2f} s")

    root.mainloop()
    root.destroy() # destroy all windows

    logging.info("end")

