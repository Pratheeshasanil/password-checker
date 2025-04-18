import tkinter as tk
from tkinter import messagebox
import re
import random
import string
import datetime
import csv

def check_password_strength(password):
    strength = 0
    suggestions = []

    if len(password) >= 8:
        strength += 1
    else:
        suggestions.append("Make it at least 8 characters long.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        strength += 1
    else:
        suggestions.append("Use both uppercase and lowercase letters.")

    if re.search(r"\d", password):
        strength += 1
    else:
        suggestions.append("Add at least one number.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        strength += 1
    else:
        suggestions.append("Include special characters like @, #, $ etc.")

    if strength == 4:
        remarks = "Strong"
    elif strength == 3:
        remarks = "Moderate"
    elif strength == 2:
        remarks = "Weak"
    else:
        remarks = "Very Weak"

    return remarks, suggestions

def on_check_click():
    password = password_entry.get()
    result, suggestions = check_password_strength(password)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if suggestions:
        suggestions_text = "\n".join(suggestions)
        messagebox.showinfo("Password Strength", f"Strength: {result}\n\nSuggestions:\n{suggestions_text}")
        with open("password_report.txt", "a") as file:
            file.write(f"Time: {timestamp}\nPassword: {password}\nStrength: {result}\nSuggestions:\n{suggestions_text}\n\n")
        save_to_csv(timestamp, password, result, suggestions)
    else:
        messagebox.showinfo("Password Strength", f"Strength: {result}")
        with open("password_report.txt", "a") as file:
            file.write(f"Time: {timestamp}\nPassword: {password}\nStrength: {result}\n\n")
        save_to_csv(timestamp, password, result, [])

def clear_entry():
    password_entry.delete(0, tk.END)

def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(12))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

def toggle_password():
    if show_password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

def show_history():
    try:
        with open("password_report.txt", "r") as file:
            history = file.read()
    except FileNotFoundError:
        history = "No history found."

    history_window = tk.Toplevel(root)
    history_window.title("Password History")
    history_window.geometry("500x400")

    text_widget = tk.Text(history_window, wrap="word")
    text_widget.insert("1.0", history)
    text_widget.config(state="disabled")
    text_widget.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(text_widget)
    scrollbar.pack(side="right", fill="y")
    text_widget.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text_widget.yview)

def save_to_csv(timestamp, password, result, suggestions):
    with open("password_report.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        suggestions_text = ", ".join(suggestions) if suggestions else ""
        writer.writerow([timestamp, password, result, suggestions_text])

# GUI Setup
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("400x400")

label = tk.Label(root, text="Enter Password:", font=("Arial", 14))
label.pack(pady=10)

password_entry = tk.Entry(root, show="*", font=("Arial", 12))
password_entry.pack(pady=10)

check_button = tk.Button(root, text="Check Strength", font=("Arial", 12), command=on_check_click)
check_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear", font=("Arial", 12), bg="#003366", fg="white", command=clear_entry)
clear_button.pack(pady=5)

generate_button = tk.Button(root, text="Generate Password", font=("Arial", 12), bg="#228B22", fg="white", command=generate_password)
generate_button.pack(pady=5)

history_button = tk.Button(root, text="View History", command=show_history, bg="#007acc", fg="white", font=("Arial", 12, "bold"))
history_button.pack(pady=5)

show_password_var = tk.BooleanVar()
show_password_check = tk.Checkbutton(root, text="Show Password", variable=show_password_var, command=toggle_password)
show_password_check.pack()

root.mainloop()
