import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import sqlite3

def init_db():
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bmi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            weight REAL,
            height REAL,
            bmi REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def calculate_bmi(weight, height):
    try:
        bmi = weight / (height / 100) ** 2
        return round(bmi, 2)
    except ZeroDivisionError:
        return None

def add_to_db(name, weight, height, bmi):
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bmi (name, weight, height, bmi)
        VALUES (?, ?, ?, ?)
    ''', (name, weight, height, bmi))
    conn.commit()
    conn.close()

def fetch_all_data():
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bmi')
    rows = cursor.fetchall()
    conn.close()
    return rows

def display_data():
    data_listbox.delete(0, tk.END)
    for row in fetch_all_data():
        data_listbox.insert(tk.END, row)

def handle_calculate():
    name = name_entry.get()
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers for weight and height.")
        return

    bmi = calculate_bmi(weight, height)
    if bmi:
        bmi_label.config(text=f"Your BMI: {bmi}")
        if bmi < 18.5:
            bmi_message = "You are underweight."
        elif 18.5 <= bmi < 25:
            bmi_message = "You have a normal weight."
        elif 25 <= bmi < 30:
            bmi_message = "You are overweight."
        else:
            bmi_message = "You are obese."
        
        bmi_label.config(text=f"Your BMI: {bmi} - {bmi_message}")
        add_to_db(name, weight, height, bmi)
        display_data()
    else:
        messagebox.showerror("Calculation error", "Height cannot be zero.")

def visualize_trends():
    data = fetch_all_data()
    names = [row[1] for row in data]
    bmis = [row[4] for row in data]

    plt.figure(figsize=(10, 5))
    plt.plot(names, bmis, marker='o')
    plt.title("BMI Trends")
    plt.xlabel("User")
    plt.ylabel("BMI")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

init_db()

root = tk.Tk()
root.title("BMI Calculator")

tk.Label(root, text="Name:").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Weight (kg):").grid(row=1, column=0)
weight_entry = tk.Entry(root)
weight_entry.grid(row=1, column=1)

tk.Label(root, text="Height (cm):").grid(row=2, column=0)
height_entry = tk.Entry(root)
height_entry.grid(row=2, column=1)

calc_button = tk.Button(root, text="Calculate BMI", command=handle_calculate)
calc_button.grid(row=3, column=0, columnspan=2)

bmi_label = tk.Label(root, text="Your BMI: ")
bmi_label.grid(row=4, column=0, columnspan=2)

data_listbox = tk.Listbox(root, width=50)
data_listbox.grid(row=5, column=0, columnspan=2)

visualize_button = tk.Button(root, text="Visualize BMI Trends", command=visualize_trends)
visualize_button.grid(row=6, column=0, columnspan=2)

display_data()

root.mainloop()