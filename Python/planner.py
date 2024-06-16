import tkinter as tk
from tkinter import font
import customtkinter as ctk
import json
import os

SAVE_FILE = "sticky_notes.json"

class StickyNote:
    def __init__(self, root, x, y, width=200, height=300, text=""):
        self.root = root
        self.width = width
        self.height = height
        self.custom_font = font.Font(family="Roboto", size=10, weight="normal")

        # Main outer frame for each sticky note
        self.frame = tk.Frame(root, bg='#e0e0e0', bd=0, relief='solid')
        self.frame.place(x=x, y=y, width=self.width, height=self.height)

        # Title bar for each note. Used for repositioning note
        self.title_bar = tk.Frame(self.frame, bg='#00171F', height=100, relief='raised', bd=1)
        self.title_bar.pack(fill='x')
        self.title_label = tk.Label(self.title_bar, text="Sticky Note", bg='#00171F', fg='white', font=self.custom_font)
        self.title_label.pack(side='left', padx=5)

        # Delete button
        self.delete_button = ctk.CTkButton(self.title_bar, text="X", fg_color='red', text_color='white', command=self.delete_note, width=20, height=20, corner_radius=10)
        self.delete_button.pack(side='right', padx=5, pady=0)

        # Note content (using text widget)
        self.text = tk.Text(self.frame, bg='#e0e0e0', wrap='word', bd=0, padx=5, pady=5, font=self.custom_font)
        self.text.pack(expand=True, fill='both')
        self.text.insert(tk.END, text)

        # Functionality for repositoning notes (see functions below)
        self.frame.bind('<Button-1>', self.start_move)
        self.frame.bind('<B1-Motion>', self.do_move)
        self.title_bar.bind('<Button-1>', self.start_move)
        self.title_bar.bind('<B1-Motion>', self.do_move)
        self.title_label.bind('<Button-1>', self.start_move)
        self.title_label.bind('<B1-Motion>', self.do_move)
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
        sticky_notes.remove(self)

    def get_state(self):
        return {
            "x": self.frame.winfo_x(),
            "y": self.frame.winfo_y(),
            "width": self.frame.winfo_width(),
            "height": self.frame.winfo_height(),
            "text": self.text.get("1.0", tk.END).strip()
        }

def save_notes():
    notes_state = [note.get_state() for note in sticky_notes]
    with open(SAVE_FILE, "w") as f:
        json.dump(notes_state, f)

def load_notes():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            notes_state = json.load(f)
            for note_state in notes_state:
                note = StickyNote(
                    root,
                    note_state["x"],
                    note_state["y"],
                    note_state["width"],
                    note_state["height"],
                    note_state["text"]
                )
                sticky_notes.append(note)

def new_note():
    x, y = 100, 100
    note = StickyNote(root, x, y)
    sticky_notes.append(note)

def on_close():
    save_notes()
    root.destroy()

def main():
    global root, sticky_notes
    sticky_notes = []

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Sticky Notes")
    root.geometry("1280x720")

    load_notes()

    # Button to create new sticky notes
    new_note_button = ctk.CTkButton(root, text="New Note", command=new_note)
    new_note_button.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    main()
