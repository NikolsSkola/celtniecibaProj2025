import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create and setup SQLite database (only if it doesn't exist)
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create the users table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL)''')
    
    # Add a default user if the table is empty (you can remove this for real app)
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', '1234'))
        conn.commit()
    
    conn.close()

# Function to check login against database
def check_login():
    user = username_entry.get()
    pwd = password_entry.get()
    
    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Check if the user exists in the database
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, pwd))
    result = cursor.fetchone()
    
    if result:
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")
    
    conn.close()

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

setup_database()

login_window.mainloop()