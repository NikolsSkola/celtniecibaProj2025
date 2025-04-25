import tkinter as tk
from tkinter import messagebox

# Hardcoded credentials
USERNAME = "admin"
PASSWORD = "1234"

# Function to check login
def check_login():
    user = username_entry.get()
    pwd = password_entry.get()
    if user == USERNAME and pwd == PASSWORD:
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to open main window
def open_main_window():
    root = tk.Tk()
    root.title("Tk Example")
    root.configure(background="lightgray")
    root.minsize(500, 500)
    root.maxsize(1920, 1080)
    root.geometry("300x300+50+50")

    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (300 // 2)
    y = (screen_height // 2) - (300 // 2)
    root.geometry(f"300x300+{x}+{y}")

    root.mainloop()

# Create login window
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("500x500")

tk.Label(login_window, text="Username").pack(pady=(10, 0))
username_entry = tk.Entry(login_window)
username_entry.pack()

tk.Label(login_window, text="Password").pack(pady=(10, 0))
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

tk.Button(login_window, text="Login", command=check_login).pack(pady=20)

login_window.update_idletasks()
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()
x = (screen_width // 2) - (500 // 2)
y = (screen_height // 2) - (500 // 2)
login_window.geometry(f"500x500+{x}+{y}")

login_window.mainloop()