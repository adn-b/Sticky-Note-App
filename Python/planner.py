import tkinter as tk
from tkinter import font

class StickyNote:
    def __init__(self, root, x, y, width=200, height=100):
        self.root = root
        self.width = width
        self.height = height

        # Main outer frame for each sticky note
        self.frame = tk.Frame(root, bg='#e0e0e0', bd=0, relief='solid')
        self.frame.place(x=x, y=y, width=self.width, height=self.height)

        # Title bar for each note. Used for repositioning note
        self.title_bar = tk.Frame(self.frame, bg='#00171F', height=20, relief='raised', bd=1)
        self.title_bar.pack(fill='x')
        self.title_label = tk.Label(self.title_bar, text="Sticky Note", bg='#00171F', fg='white')
        self.title_label.pack(side='left', padx=5)

        # Delete button
        self.delete_button = tk.Button(self.title_bar, text="X", bg='red', fg='white', command=self.delete_note)
        self.delete_button.pack(side='right', padx=10)

        # Note content (using text widget)
        self.custom_font = font.Font(family="Roboto", size=11, weight="normal")
        self.text = tk.Text(self.frame, bg='#e0e0e0', wrap='word', bd=0, padx=5, pady=5, font=self.custom_font)
        self.text.pack(expand=True, fill='both')

        # Functionality for repositoning notes (see functions below)
        self.frame.bind('<Button-1>', self.start_move)
        self.frame.bind('<B1-Motion>', self.do_move)
        self.title_bar.bind('<Button-1>', self.start_move)
        self.title_bar.bind('<B1-Motion>', self.do_move)

        # Resize handle
        self.resize_handle = tk.Frame(self.frame, bg='black', cursor='sizing', bd=0, width=10, height=10)
        self.resize_handle.place(relx=1.0, rely=1.0, anchor='se')
        self.resize_handle.bind('<Button-1>', self.start_resize)
        self.resize_handle.bind('<B1-Motion>', self.do_resize)

    def start_move(self, event):
        self.startX = event.x
        self.startY = event.y

    def do_move(self, event):
        x = self.frame.winfo_x() + event.x - self.startX
        y = self.frame.winfo_y() + event.y - self.startY
        self.frame.place(x=x, y=y)

    def start_resize(self, event):
        self.startX = event.x
        self.startY = event.y
        self.startWidth = self.frame.winfo_width()
        self.startHeight = self.frame.winfo_height()

    def do_resize(self, event):
        new_width = self.startWidth + (event.x - self.startX)
        new_height = self.startHeight + (event.y - self.startY)
        if new_width > 25 and new_height > 25:
            self.frame.place(width=new_width, height=new_height)
            self.resize_handle.place(relx=1.0, rely=1.0, anchor='se')

    def delete_note(self):
        self.frame.destroy()

def new_note():
    x, y = 100, 100
    StickyNote(root, x, y)

def main():
    global root
    root = tk.Tk()
    root.title("Sticky Notes")
    root.geometry("800x600")

    # notes = [
    #     (50, 50),
    #     (200, 150),
    #     (350, 250)
    # ]

    # for x, y in notes:
    #     StickyNote(root, x, y)

    # Button to create new sticky notes
    new_note_button = tk.Button(root, text="New Note", command=new_note)
    new_note_button.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)


    root.mainloop()

if __name__ == "__main__":
    main()