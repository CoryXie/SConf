#!/usr/bin/env python

# Populate a tree of all items in the configuration

import os
import sys
from Tkinter import *
from ScrolledText import *
import ttk
import kconf

class App():
    def __init__(self, master, conf):
        self.conf = conf
        self.items = conf.get_top_level_items()
        self.tree = ttk.Treeview(master, selectmode="browse", columns=("name", "value", "type"), height=30)
        
        ysb = ttk.Scrollbar(orient=VERTICAL, command= self.tree.yview)
        xsb = ttk.Scrollbar(orient=HORIZONTAL, command= self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        
        self.tree.heading('#0', text='Configuration Tree', anchor='w')
        self.tree.column("#0", minwidth=0, width=300, stretch=True)

        self.tree.heading("name", text="Conguration Name")   
        self.tree.column("name", minwidth=0, width=200, stretch=True)
        
        self.tree.heading("value", text="Conguration Value")   
        self.tree.column("value", minwidth=0, width=200, stretch=True)
        
        self.tree.heading("type", text="Conguration Type")   
        self.tree.column("type", minwidth=0, width=200, stretch=True)

        self.add_root_items(self.items)
        
        self.helptext = ScrolledText(master, width=130, height=10)
        
        self.tree.grid(row=0, column=0)
        self.helptext.grid(row=1, column=0)
        ysb.grid(row=0, column=1, sticky='ns')
        xsb.grid(row=1, column=0, sticky='ew')

        master.grid()
        
        self.tree.bind("<Double-1>", self.OnDoubleClick)
        self.tree.bind("<<TreeviewSelect>>", self.OnSelection)
    
    def add_subr_items(self, parent, items):
        for item in items:
            if item.is_symbol():
                str = 'config {0}'.format(item.get_name())
                self.tree.insert(parent, "end", text=str, values=[item.get_name(), item.get_value(), kconf.TYPENAME[item.get_type()]])
            elif item.is_menu():
                str = 'menu "{0}"'.format(item.get_title())
                parent = self.tree.insert(parent, "end", text=str)
                self.add_subr_items(parent, item.get_items())
            elif item.is_choice():
                str = 'choice "{0}"'.format(item.get_prompts()[0])
                parent = self.tree.insert(parent, "end", text=str)
                self.add_subr_items(parent, item.get_items())
            elif item.is_comment():
                str = 'comment "{0}"'.format(item.get_text())
                self.tree.insert(parent, "end", text=str)
                
    def add_root_items(self, items):
        for item in items:
            if item.is_symbol():
                str = 'config {0}'.format(item.get_name())
                self.tree.insert("", "end", text=str, values=[item.get_name(), item.get_value(), kconf.TYPENAME[item.get_type()]])
            elif item.is_menu():
                str = 'menu "{0}"'.format(item.get_title())
                parent = self.tree.insert("", "end", text=str)
                self.add_subr_items(parent, item.get_items())
            elif item.is_choice():
                str = 'choice "{0}"'.format(item.get_prompts()[0])
                parent = self.tree.insert("", "end", text=str)
                self.add_subr_items(parent, item.get_items())
            elif item.is_comment():
                str = 'comment "{0}"'.format(item.get_text())
                self.tree.insert("", "end", text=str)             
        
    def OnDoubleClick(self, event):
        mitem = self.tree.identify('item',event.x, event.y)
        print("you clicked on", self.tree.item(mitem,"text"))
        
    def OnSelection(self, event):
        mitem = self.tree.focus()
        values = self.tree.item(mitem,"values");
        if (values):
            symbal = self.conf.get_symbol(values[0])
            if (symbal):
                self.helptext.delete(1.0, END)
                help = symbal.get_help()
                if (help):
                    self.helptext.insert(INSERT, help)
        
if __name__ == "__main__":

    conf = kconf.Config(sys.argv[1])
    if os.path.exists(".config"):
        conf.load_config(".config")
    
    root = Tk()
    app = App(root, conf)
    root.title(os.path.abspath('.').replace('\\', '/') + "/" + sys.argv[1])
    root.mainloop()