#!/usr/bin/env python

# Populate a tree of all items in the configuration

import os
import sys
from Tkinter import *
from ScrolledText import *
import ttk
import kconf

class PopupWindow(object):
    def __init__(self, root, config, value):
        self.top=top=Toplevel(root)
        self.l=Label(top, text=config)
        self.l.grid(row=0, column=0)
        self.e=Entry(top)
        self.e.delete(0, END)
        self.e.insert(0, value)
        self.e.grid(row=0, column=1)
        self.b=Button(top, text='Submit', command=self.Submit)
        self.b.grid(row=1, column=0)
        self.c=Button(top, text='Cancel', command=self.Cancel)
        self.c.grid(row=1, column=1)
        self.v=False
        self.Center()
        self.top.grid()
        self.top.wm_title("Set " + config)
        
    def Submit(self):
        self.value=self.e.get()
        self.v=True        
        self.top.destroy()
        
    def Cancel(self):
        self.v=False        
        self.top.destroy()
        
    def Center(self):
        self.top.update()
        w_req, h_req = self.top.winfo_width(), self.top.winfo_height()
        w_form = self.top.winfo_rootx() - self.top.winfo_x()
        w = w_req + w_form*2
        h = h_req + (self.top.winfo_rooty() - self.top.winfo_y()) + w_form
        x = (self.top.winfo_screenwidth() // 2) - (w // 2)
        y = (self.top.winfo_screenheight() // 2) - (h // 2)
        self.top.geometry('{0}x{1}+{2}+{3}'.format(w_req, h_req, x, y))    
        
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

    def search_for_item(self, name, item=None):
        children = self.tree.get_children(item)
        for child in children:
            nameval = self.tree.set(child, "name")
            if nameval == name:
                return child
            else:
                res = self.search_for_item(name, child)
                if res:
                    return res
        return None
                    
    def OnDoubleClick(self, event):
        mitem = self.tree.identify('item',event.x, event.y)
        nameval = self.tree.set(mitem, "name")
        symbol = self.conf.get_symbol(nameval)
        
        if symbol is None:
            return
        
        if (symbol.get_type() == kconf.BOOL or (symbol.get_type() == kconf.TRISTATE and not self.conf.is_tristate_enabled())):
            if (symbol.is_choice_symbol() and len(symbol.get_parent().get_items()) == 1):
                self.msg.set("A boolean choice, exactly one config option must be set to y, so no change here!")
                return
            if (symbol.get_value() == "y"):
                print("Setting " + symbol.get_name() + " to n")
                symbol.set_user_value("n")
                if (symbol.get_value() == "y"):
                    self.msg.set("A boolean choice that is the only 'y' in the choice group can not be set to 'n'")
                    symbol.set_user_value("y")
                    return
                self.tree.set(mitem, "value", symbol.get_value())
            else:
                print("Setting " + symbol.get_name() + " to y")
                symbol.set_user_value("y")   
                self.tree.set(mitem, "value", symbol.get_value())
            print("Dependents for " + symbol.get_name() + " {" + symbol.get_visibility() + "} " + " [" + symbol.get_value() + "]:")
            for sym in symbol.get_dependent_symbols():
                print(sym.get_name() + " {"+sym.get_visibility() + "} " + " [" + sym.get_value() + "] ")
                mitem = self.search_for_item(sym.get_name(), None)
                if (mitem):
                    self.tree.set(mitem, "value", sym.get_value())
            print("========================================")
        elif (symbol.get_type() == kconf.TRISTATE and self.conf.is_tristate_enabled()):
            nono = False
            if (symbol.is_choice_symbol() and len(symbol.get_parent().get_items()) == 1):
                self.msg.set("A single tristate choice in one choice group can not be set to 'n'")
                nono = True
            # 'y'->'m'->'n'->'y'->'m'->'n'->...
            if (symbol.get_value() == "y"):
                print("Setting " + symbol.get_name() + " to m")
                symbol.set_user_value("m")
                if (symbol.get_value() == "y"):
                    self.msg.set("A tristate choice that is the only 'y' in the choice group can not be set to 'n'")
                    symbol.set_user_value("y")
                    return
                self.tree.set(mitem, "value", symbol.get_value())
            elif (symbol.get_value() == "m"):
                print("Setting " + symbol.get_name() + " to n")
                symbol.set_user_value("n")
                if (symbol.get_value() == "m"):
                    self.msg.set("A tristate choice that is the only 'm' in the choice group can not be set to 'n'")
                    symbol.set_user_value("m")
                    return
                self.tree.set(mitem, "value", symbol.get_value())
            else:
                print("Setting " + symbol.get_name() + " to y")
                symbol.set_user_value("y")   
                self.tree.set(mitem, "value", symbol.get_value())
            print("Dependents for " + symbol.get_name() + " {" + symbol.get_visibility() + "} " + " [" + symbol.get_value() + "]:")
            for sym in symbol.get_dependent_symbols():
                print(sym.get_name() + " {"+sym.get_visibility() + "} " + " [" + sym.get_value() + "] ")
                mitem = self.search_for_item(sym.get_name(), None)
                if (mitem):
                    self.tree.set(mitem, "value", sym.get_value())
            print("========================================")            
        elif (symbol.get_type() == kconf.INT or symbol.get_type() == kconf.HEX or symbol.get_type() == kconf.STRING):
            self.pop = PopupWindow(self.root, symbol.get_name(), symbol.get_value())
            self.root.wait_window(self.pop.top)
            if (self.pop.v == True):
                print("Setting " + symbol.get_name() + " to " + self.pop.value)
                symbol.set_user_value(self.pop.value)
                print("Now " + symbol.get_name() + " is " + symbol.get_value())
                self.tree.set(mitem, "value", symbol.get_value())
            
        return
                    
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

        return

    def OnSaveConfig(self):
        self.conf.write_config(".config")
        self.msg.set("Configurations Saved!")
        return
 
    def OnQuitConfig(self):
        self.root.quit()
        return
        
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
