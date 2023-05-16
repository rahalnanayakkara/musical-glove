import tkinter as tk
from tkinter import  messagebox, filedialog
from sys import exit

class MyGUI:

    def __init__(self):
        
        self.root = tk.Tk()
        self.root.geometry("800x400")

        self.xml_path = ""
        self.wav_path = ""

        # Create Menu
        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Close', command=self.on_closing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Force Close', command=exit)

        self.menubar.add_cascade(menu=self.filemenu, label="File")

        self.root.config(menu=self.menubar)

        # Create Label
        self.xml_label = tk.Label(self.root, text='Music XML File', font=('Arial',18))
        self.xml_label.pack(padx=10, pady=10)

        # Create textbox to enter text
        self.xml_textbox = tk.Text(self.root, height=1, font=('Arial', 16))
        self.xml_textbox.pack(padx=10)

        # Create button
        self.xml_button = tk.Button(self.root, text='Select Music XML File', font=('Arial', 16), command=self.select_xml_file)
        self.xml_button.pack(padx=10, pady=10)

        # Create Label
        self.wav_label = tk.Label(self.root, text='Wav File', font=('Arial',18))
        self.wav_label.pack(padx=10, pady=10)

        # Create textbox to enter text
        self.wav_textbox = tk.Text(self.root, height=1, font=('Arial', 16))
        self.wav_textbox.pack(padx=10)

        # Create button
        self.wav_button = tk.Button(self.root, text='Select Wav File', font=('Arial', 16), command=self.select_wav_file)
        self.wav_button.pack(padx=10, pady=10)

        self.next_button = tk.Button(self.root, text='Connect to Glove', font=('Arial', 16), command=self.connect_glove)
        self.next_button.pack(padx=10, pady=20)

        # Add a closing protocol (called when 'X' is clicked)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


    def select_xml_file(self):
        self.xml_path = filedialog.askopenfile()
        self.xml_textbox.insert(tk.INSERT, self.xml_path.name)


    def select_wav_file(self):
        self.wav_path = filedialog.askopenfile()
        self.wav_textbox.insert(tk.INSERT, self.wav_path.name)


    def connect_glove(self):
        messagebox.showerror(title="Error", message="No Glove Detected!!!")

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            self.root.destroy()


MyGUI()