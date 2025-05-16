import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

# ---------- Database Setup ----------
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.close()

# ---------- Login Functions ----------
def check_login():
    user = username_entry.get()
    pwd = password_entry.get()

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, pwd))
    result = cursor.fetchone()

    if result:
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

    conn.close()

# ---------- Registration Functions ----------
def register_user():
    username = reg_username_entry.get()
    password = reg_password_entry.get()

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    
    if cursor.fetchone():
        messagebox.showerror("Registration Failed", "Username already exists!")
    else:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        reg_window.destroy()

    conn.close()

# ---------- Main App Window ----------
def open_main_window():
    root = tk.Tk()
    root.title("Main Window")
    root.configure(background="#f0f0f0")
    root.geometry("400x300")
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() - 400) // 2
    y = (root.winfo_screenheight() - 300) // 2
    root.geometry(f"400x300+{x}+{y}")

    tk.Label(root, text="Welcome!", font=("Arial", 18), bg="#f0f0f0").pack(pady=30)
    tk.Label(root, text="You have successfully logged in.", bg="#f0f0f0").pack()

    tk.Button(root, text="Exit", command=root.quit, bg="#d9534f", fg="white", width=10).pack(pady=30)

    root.mainloop()

# ---------- Registration Window ----------
def create_registration_window():
    global reg_username_entry, reg_password_entry, reg_window
    reg_window = tk.Toplevel()
    reg_window.title("Register")
    reg_window.geometry("350x250")
    
    x = (reg_window.winfo_screenwidth() - 350) // 2
    y = (reg_window.winfo_screenheight() - 250) // 2
    reg_window.geometry(f"350x250+{x}+{y}")
    reg_window.configure(bg="white")

    tk.Label(reg_window, text="Register New Account", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

    tk.Label(reg_window, text="Username:", bg="white").pack()
    reg_username_entry = tk.Entry(reg_window)
    reg_username_entry.pack()

    tk.Label(reg_window, text="Password:", bg="white").pack(pady=(10, 0))
    reg_password_entry = tk.Entry(reg_window, show="*")
    reg_password_entry.pack()

    tk.Button(reg_window, text="Register", command=register_user, bg="#0275d8", fg="white", width=15).pack(pady=20)

# ---------- Login Window ----------
def create_login_window():
    global username_entry, password_entry, login_window

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("500x500")
    login_window.resizable(False, False)

    # Center window
    x = (login_window.winfo_screenwidth() - 500) // 2
    y = (login_window.winfo_screenheight() - 500) // 2
    login_window.geometry(f"500x500+{x}+{y}")

    # Load background
    try:
        bg_image = Image.open("remonts_login.jpg").resize((500, 500), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(login_window, image=bg_photo)
        bg_label.image = bg_photo  # keep reference
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Background image error:", e)

    # Overlay Frame
    frame = tk.Frame(login_window, bg="white", bd=2, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=250)

    tk.Label(frame, text="Login", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    tk.Label(frame, text="Username:", bg="white").pack(anchor="w", padx=20)
    username_entry = tk.Entry(frame)
    username_entry.pack(padx=20)

    tk.Label(frame, text="Password:", bg="white").pack(anchor="w", padx=20, pady=(10, 0))
    password_entry = tk.Entry(frame, show="*")
    password_entry.pack(padx=20)

    tk.Button(frame, text="Login", command=check_login, bg="#5cb85c", fg="white", width=20).pack(pady=(20, 5))
    tk.Button(frame, text="Register", command=create_registration_window, width=20).pack()

    login_window.mainloop()

# ---------- Start App ----------
if __name__ == "__main__":
    setup_database()
    create_login_window()
