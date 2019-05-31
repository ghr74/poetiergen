import tkinter as tk
from tkinter import ttk
# import excache
import datetime

root = tk.Tk()

class ListFrame(ttk.Frame):

    def __init__(self, master, **kwargs):

        ttk.Frame.__init__(self, master, **kwargs)

        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0)
                                  

    def pack(self, **kwargs):

        self.canvas.pack(side=tk.LEFT, 
                                                fill=tk.BOTH, expand=tk.TRUE)

        ttk.Frame.pack(self, **kwargs)

    def get_frame(self):

        return self.canvas

class EditPopup():

    def validateString(self):
        try:
            first, second = self.l.get().split(' - ', 1)
            return len(first) > 0 and len(second) > 0
        except:
            return False

    def OnEnter(self, event):
        if self.validateString():
            # Pull Cache Data, 
            # excache.extract_content(self.target_index)
            #artist, title = self.l.get().split(' - ', 1)
            # webm_to_opus.convert(artist + ' - ' + title)
            exit(0)
        elif self.l.get() == "":
            pass

    def OnEscape(self, event):
        self.win.destroy()

    def popup_bonus(self, index):
        self.win = tk.Toplevel()
        self.win.transient(root)
        self.win.wm_title("Artist - Title")
        self.win.resizable(0, 0)
        self.target_index = index
        self.l = tk.Entry(self.win, width=100, font=('Arial', 16, 'bold'), justify='center')
        self.l.pack()
        center(self.win)
        self.l.focus()
        self.l.bind("<Return>", self.OnEnter)
        self.l.bind("<Escape>", self.OnEscape)

def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

# test_list = excache.getIndexcache()
test_list = [
    ["Key", datetime.datetime(2018, 5, 9, 16, 20, 44, 57673), 37]
]

list_length = max(len(test_list), 20)
root.title("Chrome Cache to webm")
rwidth = 230
rheight = 150
root.minsize(width=rwidth, height=rheight)
root.maxsize(width=rwidth, height=rheight)
root.resizable(0, 0)
center(root)
frame = ListFrame(root)

subframe = ttk.Frame( frame.get_frame() ) 
tree = ttk.Treeview(frame.get_frame(), show="", height=list_length, columns=("Date", "Count"))

edit = EditPopup()
tree.pack(anchor = 'center', fill = tk.BOTH, expand = tk.Y)
subframe.pack(padx  = 15, pady   = 15, fill = tk.BOTH, expand = tk.TRUE)
frame.pack(expand = True, fill = tk.BOTH)

def OnDoubleClick(event):
        item = tree.identify('item',event.x,event.y)
        edit.popup_bonus(tree.index(item))
        # excache.extract_content(tree.index(item))

for entry in test_list:
    tree.insert("", "end", values=[str(entry[1]).rsplit('.',1)[0],str(entry[2])])
tree.bind("<Double-1>", OnDoubleClick)

def OnEnterRoot(event):
    exit(0)

root.bind("<Escape>", OnEnterRoot)

# Launch
root.mainloop()