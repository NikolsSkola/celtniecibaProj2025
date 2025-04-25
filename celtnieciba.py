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

# Function to register a new user
def register_user():
    username = reg_username_entry.get()
    password = reg_password_entry.get()
    
    # Check if the username already exists
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        messagebox.showerror("Registration Failed", "Username already exists!")
    else:
        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Registration Successful", "Account created successfully!")
        reg_window.destroy()
    
    conn.close()

# Function to open main window after login
def open_main_window():
    root = tk.Tk()
    root.title("Tk Example")
    root.configure(background="lightgray")
    root.minsize(200, 200)
    root.maxsize(1920, 1080)
    root.geometry("300x300")  # Set initial size

    # Center the window on the screen
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (300 // 2)
    y = (screen_height // 2) - (300 // 2)
    root.geometry(f"300x300+{x}+{y}")

    # Sample content for the logged-in user
    tk.Label(root, text="Welcome to the main window!").pack(pady=20)
    root.mainloop()

# Create and setup the login window
def create_login_window():
    global username_entry, password_entry, login_window
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("500x500")  # Set size

    # Center the window on the screen
    login_window.update_idletasks()
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    x = (screen_width // 2) - (500 // 2)
    y = (screen_height // 2) - (500 // 2)
    login_window.geometry(f"500x500+{x}+{y}")

    # Add login fields
    tk.Label(login_window, text="Username").pack(pady=(10, 0))
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password").pack(pady=(10, 0))
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    # Add Login button
    tk.Button(login_window, text="Login", command=check_login).pack(pady=20)

    # Add Register button underneath the Login button
    tk.Button(login_window, text="Register", command=create_registration_window).pack(pady=10)

    login_window.mainloop()

# Create and setup the registration window
def create_registration_window():
    global reg_username_entry, reg_password_entry, reg_window
    reg_window = tk.Toplevel()  # Create a new window
    reg_window.title("Register")
    reg_window.geometry("400x300")

    # Center the window on the screen
    reg_window.update_idletasks()
    screen_width = reg_window.winfo_screenwidth()
    screen_height = reg_window.winfo_screenheight()
    x = (screen_width // 2) - (400 // 2)
    y = (screen_height // 2) - (300 // 2)
    reg_window.geometry(f"400x300+{x}+{y}")

    # Add registration fields
    tk.Label(reg_window, text="Username").pack(pady=(10, 0))
    reg_username_entry = tk.Entry(reg_window)
    reg_username_entry.pack()

    tk.Label(reg_window, text="Password").pack(pady=(10, 0))
    reg_password_entry = tk.Entry(reg_window, show="*")
    reg_password_entry.pack()

    tk.Button(reg_window, text="Register", command=register_user).pack(pady=20)

# Setup the database when the script runs
setup_database()

# Start the login window
create_login_window()
