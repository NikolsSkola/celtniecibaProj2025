import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
import io

# Create and setup SQLite database (only if it doesn't exist)
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create the users table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        idUser INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Images (
                        idImage INTEGER PRIMARY KEY AUTOINCREMENT,
                        blobImage BLOB,
                        nameImage TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Savieno (
                        idSavieno INTEGER PRIMARY KEY AUTOINCREMENT,
                        idUser INTEGER,
                        idImage INTEGER)''')
    
    conn.close()

# Function to check login against database
def check_login():
    user = username_entry.get()
    pwd = password_entry.get()
    
    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Check if the user exists in the database
    cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (user, pwd))
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
    
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    if cursor.fetchone():
        messagebox.showerror("Registration Failed", "Username already exists!")
    else:
        # Insert the new user into the database
        cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
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


    tk.Button(root, text="nikols logs", command=open_nikola_big_log).pack(pady=10)
    
    tk.Button(root, text="Atvērt attēlu galeriju", command=open_gallery).pack(pady=20, padx=50)

    root.mainloop()
DB_NAME = "users.db"
TABLE_NAME = "Images"
MAX_WIDTH = 300

def fetch_image(image_id):
    """Retrieve and resize image from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"SELECT blobImage FROM {TABLE_NAME} WHERE idImage = ?", (image_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        image = Image.open(io.BytesIO(bytes(result[0])))
        if image.width > MAX_WIDTH:
            image.thumbnail((MAX_WIDTH, MAX_WIDTH))
        return ImageTk.PhotoImage(image)
    return None

def show_vote_result(image_id):
    """Display the voted image in a new window."""
    vote_window = tk.Toplevel()
    vote_window.title("Jūsu izvēle")
    image_display = fetch_image(image_id)

    if image_display:
        tk.Label(vote_window, image=image_display).pack(pady=10)
        tk.Label(vote_window, text=f"Jūs izvēlējāties mājokli {chr(64 + image_id)}", font=("Arial", 14, "bold")).pack(pady=10)
        vote_window.image = image_display  # Prevent garbage collection
    center_window(vote_window, MAX_WIDTH + 40, MAX_WIDTH + 100)

def open_gallery():
    """Create a centered window displaying images and voting options."""
    gallery = tk.Toplevel()
    gallery.title("Izvēlies visskaistāko mājokli")
    frame = tk.Frame(gallery)
    frame.pack(padx=10, pady=10)

    tk.Label(frame, text="izvēlies visskaistāko mājokli", font=("Arial", 16, "bold")).grid(row=0, columnspan=3, pady=10)
    selected_image = tk.IntVar(value=0)
    
    for i in range(1, 4):  # Only images A, B, C
        image_display = fetch_image(i)
        if image_display:
            tk.Label(frame, image=image_display).grid(row=1, column=i-1, padx=10, pady=10)
            radio_btn = tk.Radiobutton(frame, variable=selected_image, value=i, width=5, height=2, indicatoron=False, relief="sunken", text=chr(64 + i))
            radio_btn.grid(row=2, column=i-1, padx=10, pady=5)
            radio_btn.image = image_display  # Prevent garbage collection

    tk.Button(frame, text="iesniegt", command=lambda: [gallery.destroy(), show_vote_result(selected_image.get())]).grid(row=3, columnspan=3, pady=10)
    center_window(gallery, MAX_WIDTH * 3 + 40, MAX_WIDTH + 180)

def center_window(root, width, height):
    """Center a window on the screen."""
    root.update_idletasks()
    x = (root.winfo_screenwidth() - width) // 2
    y = (root.winfo_screenheight() - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

def open_nikola_big_log():
    window=tk.Tk()
    window.title("ZOINKS")
    # Center the window on the screen
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (1000 // 2)
    y = (screen_height // 2) - (1000 // 2)
    window.geometry(f"1000x1000+{x}+{y}")




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
