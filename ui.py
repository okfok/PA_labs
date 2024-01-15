import json
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename

from pydantic import ValidationError

import core

tree = core.BTree()

window = tk.Tk()
window.resizable(False, False)

label_key = tk.Label(window, text="Key")
label_value = tk.Label(window, text="Value")

entry_key = tk.Entry(window, width=10)
entry_value = tk.Entry(window, width=20)


def get_key():
    try:
        key = int(entry_key.get())
    except ValueError:
        messagebox.showerror("Value error", "Key should be number!")
        window.update()
        return
    return key


def add_event():
    key = get_key()

    if (res := tree.search(key)) is not None:
        node, index = res
        node.keys[index] = key, entry_value.get()
    else:
        tree.insert((key, entry_value.get()))

    # entry_key.delete(0, tk.END)
    entry_value.delete(0, tk.END)


def search_event():
    key = get_key()

    if (res := tree.search(key)) is not None:
        node, index = res
        entry_value.delete(0, tk.END)
        entry_value.insert(0, node.keys[index][1])
    else:
        messagebox.showerror("Value error", "Key has not found in tree!")
        window.update()
        return


def remove_event():
    key = get_key()

    if tree.search(key) is not None:
        tree.delete(key)
        entry_key.delete(0, tk.END)
        entry_value.delete(0, tk.END)
    else:
        messagebox.showerror("Value error", "Key has not found in tree!")
        window.update()
        return


def clear_event():
    global tree
    tree = core.BTree()


def open_from_file_event():
    filepath = askopenfilename(
        filetypes=[("B-tree files", "*.btree"), ("All files", "*.*")],
        initialdir='~/Desktop',
    )
    if not filepath:
        return
    with open(filepath, "r") as input_file:
        raw_data = input_file.read()
        try:
            data = json.loads(raw_data)
            global tree
            tree = core.BTree(**data)
        except ValidationError:
            messagebox.showerror("File error", "File is broken!")


def save_to_file_event():
    filepath = asksaveasfilename(
        defaultextension="*.btree",
        filetypes=[("B-tree files", "*.btree"), ("All files", "*.*")],
        initialdir='~/Desktop',
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        output_file.write(tree.model_dump_json())


button_add = tk.Button(window, text='Add/Edit', command=add_event)
button_search = tk.Button(window, text='Search', command=search_event)
button_remove = tk.Button(window, text='Remove', command=remove_event)
button_clear = tk.Button(window, text='Clear', command=clear_event)

menu = tk.Menu(window)
window.config(menu=menu)

menu_file = tk.Menu(menu, tearoff=0)
menu_file.add_command(label='Open', command=open_from_file_event)
menu_file.add_command(label='Save', command=save_to_file_event)

menu.add_cascade(label='File', menu=menu_file)

label_key.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
label_value.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

entry_key.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
entry_value.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

button_add.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
button_search.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
button_remove.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
button_clear.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

window.mainloop()
