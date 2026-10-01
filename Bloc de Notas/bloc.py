#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, messagebox

class SimpleTextEditor:
    def __init__(self, root):
        self.root = root # internamente el objeto contiene la ventana
        self.text_area = tk.Text(self.root)
        self.text_area.pack(fill=tk.BOTH, expand=1) # en el eje Y no se consigue por los límites, por eso el expand=1
        self.current_open_file = ''

    def quit_confirm(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro de que deseas salir?") == True:
            self.root.destroy() # cierra el programa

    def open_file(self):
        filename = filedialog.askopenfilename()

        if filename: # si tiene contenido
            self.text_area.delete("1.0", tk.END) # para limpiar el contenido previo
            with open(filename, 'r') as file:
                self.text_area.insert("1.0", file.read())

            self.current_open_file = filename

    def new_file(self):
        self.text_area.delete("1.0", tk.END)
        self.current_open_file = ''

    def save_file(self):
        if not self.current_open_file:
            new_file_path = filedialog.asksaveasfilename()

            if new_file_path:
                self.current_open_file = new_file_path
            else:
                return

        with open(self.current_open_file, 'w') as file:
            file.write(self.text_area.get("1.0", tk.END))

root = tk.Tk()
root.geometry("700x500")

editor = SimpleTextEditor(root)

menu_bar = tk.Menu(root)
menu_options = tk.Menu(menu_bar, tearoff=0)

menu_options.add_command(label="Nuevo", command=editor.new_file)
menu_options.add_command(label="Abrir", command=editor.open_file)
menu_options.add_command(label="Guardar", command=editor.save_file)
menu_options.add_command(label="Salir", command=editor.quit_confirm)

root.config(menu=menu_bar)
menu_bar.add_cascade(label="Archivo", menu=menu_options)

root.mainloop()
