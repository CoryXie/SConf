#!/usr/bin/env python

# Populate a tree of all items in the configuration

import os
import sys
from Tkinter import *
from ScrolledText import *
import ttk
import kconf

class App():
    def __init__(self, root, conf):
        self.conf = conf
        self.items = conf.get_top_level_items()
        self.tree = ttk.Treeview(root, selectmode="browse", columns=("name", "value", "type"), height=30)
        
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
        
        self.help = ScrolledText(root, width=130, height=10)
        self.msg = StringVar()
        self.info = Label(root, fg="green", font=("Helvetica", 16), anchor=W, justify=LEFT, textvariable=self.msg)
        
        self.msg.set("Please set configurations, then you can save it!")
        
        self.tree.grid(row=0, column=0)
        self.help.grid(row=1, column=0)
        self.info.grid(row=2, column=0)
        ysb.grid(row=0, column=1, sticky='ns')
        xsb.grid(row=1, column=0, sticky='ew')
        
        root.grid()
        
        self.root = root
        
        # create a toplevel menu
        menubar = Menu(root)
        menubar.add_command(label="Save Config!", command=self.OnSaveConfig)
        menubar.add_command(label="Quit Config!", command=self.OnQuitConfig)

        # display the menu
        root.config(menu=menubar)
    
        self.tree.bind("<Double-1>", self.OnDoubleClick)
        self.tree.bind("<<TreeviewSelect>>", self.OnSelection)
    
    def add_subr_items(self, parent, items):
        for item in items:
            if item.get_visibility() != "n":
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
            if item.get_visibility() != "n":
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
        values = self.tree.item(mitem, "values");
        if (values):
            symbol = self.conf.get_symbol(values[0])
            print("symbol ", symbol.get_name(), " value ", symbol.get_user_value())
            if (symbol):
                if (symbol.get_type() == kconf.BOOL):
                    if (symbol.get_user_value() == "y"):
                        symbol.set_user_value("n")
                        self.tree.item(mitem, values = [values[0], "n", values[2]])
                        print("symbol ", symbol.get_name(), " changed to ", symbol.get_user_value())
                    else:
                        symbol.set_user_value("y")
                        self.tree.item(mitem, values = [values[0], "y", values[2]])
                        print("symbol ", symbol.get_name(), " changed to ", symbol.get_user_value())
                    
    def OnSelection(self, event):
        mitem = self.tree.focus()
        values = self.tree.item(mitem,"values");
        if (values):
            symbol = self.conf.get_symbol(values[0])
            if (symbol):                
                self.msg.set("Please Double Click to update config option value!")
                self.help.delete(1.0, END)
                help = symbol.get_help()
                if (help):
                    self.help.insert(INSERT, help)
                    

    def OnSaveConfig(self):
        self.conf.write_config(".config")
        self.msg.set("Configurations Saved!")
 
    def OnQuitConfig(self):
        self.root.quit()
        
if __name__ == "__main__":
    
    if len(sys.argv) <= 1:
        cfgfile = os.path.abspath('.').replace('\\', '/') + "/" + "SConfigure"
    else:
        cfgfile = os.path.abspath('.').replace('\\', '/') + "/" + sys.argv[1]
    
    conf = kconf.Config(cfgfile)
        
    if os.path.exists(".config"):
        conf.load_config(".config")
    
    root = Tk()
    app = App(root, conf)
                
    root.title(cfgfile)
    root.mainloop()
