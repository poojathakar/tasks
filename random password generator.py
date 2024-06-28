import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import string
import random
import pyperclip

def generate_password(length, use_uppercase, use_lowercase, use_digits, use_special):
    characters = ''
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    if not characters:
        messagebox.showerror("Error", "Please select at least one character type.")
        return None

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def handle_generate():
    try:
        length = int(length_entry.get())
        if length < 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid length (positive integer).")
        return

    use_uppercase = uppercase_var.get()
    use_lowercase = lowercase_var.get()
    use_digits = digits_var.get()
    use_special = special_var.get()

    password = generate_password(length, use_uppercase, use_lowercase, use_digits, use_special)
    if password:
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

def copy_to_clipboard():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showerror("Error", "No password to copy.")

root = tk.Tk()
root.title("Advanced Password Generator")

tk.Label(root, text="Password Length:").grid(row=0, column=0, padx=10, pady=10)
length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1, padx=10, pady=10)

uppercase_var = tk.BooleanVar()
lowercase_var = tk.BooleanVar()
digits_var = tk.BooleanVar()
special_var = tk.BooleanVar()

tk.Checkbutton(root, text="Include Uppercase Letters", variable=uppercase_var).grid(row=1, column=0, columnspan=2)
tk.Checkbutton(root, text="Include Lowercase Letters", variable=lowercase_var).grid(row=2, column=0, columnspan=2)
tk.Checkbutton(root, text="Include Digits", variable=digits_var).grid(row=3, column=0, columnspan=2)
tk.Checkbutton(root, text="Include Special Characters", variable=special_var).grid(row=4, column=0, columnspan=2)

generate_button = tk.Button(root, text="Generate Password", command=handle_generate)
generate_button.grid(row=5, column=0, columnspan=2, pady=10)

password_entry = tk.Entry(root, width=40)
password_entry.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=7, column=0, columnspan=2, pady=10)

root.mainloop()