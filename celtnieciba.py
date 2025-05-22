import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
from PIL import Image, ImageTk
import io

# Create and setup SQLite database

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

def check_login():
    user = username_entry.get()
    pwd = password_entry.get()

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Check if the user exists in the database
    cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (user, pwd))
    result = cursor.fetchone()
    conn.close()

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
    
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    if cursor.fetchone():
        messagebox.showerror("Registration Failed", "Username already exists!")
    elif username == "":
        messagebox.showerror("Registration Failed", "Blank username!")
    else:
        # Insert the new user into the database
        cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        reg_window.destroy()
    conn.close()

class RoomPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Room Planner")
        self.root.geometry("1000x800")
        self.root.configure(bg="#e6f2ff")

        self.max_furniture = 3
        self.furniture_items = []

        self.room_length = 4.0
        self.room_width = 3.0
        self.scale = 100  # pixels per meter

        self._drag_data = {}

        # Top control panel
        top_frame = tk.Frame(root, bg="#99ccff")
        top_frame.pack(fill=tk.X, side=tk.TOP, anchor="ne")

        tk.Button(top_frame, text="Reset", bg="#ff6666", fg="white", command=self.reset).pack(side=tk.RIGHT, padx=10, pady=5)
        tk.Button(top_frame, text="Close", bg="#666666", fg="white", command=root.quit).pack(side=tk.RIGHT, padx=10, pady=5)

        # Room size controls
        controls = tk.Frame(root, bg="#cce6ff", bd=2, relief=tk.RIDGE)
        controls.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(controls, text="Room Length (m):", bg="#cce6ff").pack(side=tk.LEFT, padx=5)
        self.length_entry = tk.Entry(controls, width=6)
        self.length_entry.pack(side=tk.LEFT)
        self.length_entry.insert(0, str(self.room_length))

        tk.Label(controls, text="Room Width (m):", bg="#cce6ff").pack(side=tk.LEFT, padx=5)
        self.width_entry = tk.Entry(controls, width=6)
        self.width_entry.pack(side=tk.LEFT)
        self.width_entry.insert(0, str(self.room_width))

        tk.Button(controls, text="Update Room", command=self.set_room_size).pack(side=tk.LEFT, padx=15)

        # Furniture controls
        furniture_frame = tk.Frame(root, bg="#d9f0ff", bd=2, relief=tk.RIDGE)
        furniture_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(furniture_frame, text="Furniture Name:", bg="#d9f0ff").grid(row=0, column=0, padx=5, pady=5)
        self.f_name = tk.Entry(furniture_frame, width=12)
        self.f_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(furniture_frame, text="Length (m):", bg="#d9f0ff").grid(row=0, column=2, padx=5, pady=5)
        self.f_length = tk.Entry(furniture_frame, width=6)
        self.f_length.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(furniture_frame, text="Width (m):", bg="#d9f0ff").grid(row=0, column=4, padx=5, pady=5)
        self.f_width = tk.Entry(furniture_frame, width=6)
        self.f_width.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(furniture_frame, text="Color:", bg="#d9f0ff").grid(row=0, column=6, padx=5, pady=5)
        self.color_btn = tk.Button(furniture_frame, text="Choose", command=self.pick_color, bg="#87ceeb")
        self.color_btn.grid(row=0, column=7, padx=5, pady=5)
        self.selected_color = "#87ceeb"

        tk.Button(furniture_frame, text="Add Furniture", bg="#4CAF50", fg="white", command=self.add_furniture).grid(row=0, column=8, padx=10, pady=5)

        # Canvas for drawing room and furniture
        self.canvas = tk.Canvas(root, bg="#ffffff", bd=4, relief=tk.RIDGE)
        self.canvas.pack(padx=10, pady=10)

        self.update_canvas_size()

        # Rating system
        self.rating_frame = tk.Frame(root, bg="#fff0cc")
        self.rating_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        tk.Label(self.rating_frame, text="Rate your experience: ", bg="#fff0cc", font=("Arial", 12)).pack(side=tk.LEFT)
        self.stars = []
        self.rating_value = 0
        for i in range(5):
            star = tk.Label(self.rating_frame, text="☆", font=("Arial", 16), bg="#fff0cc", fg="#FFD700", cursor="hand2")
            star.pack(side=tk.LEFT)
            star.bind("<Button-1>", lambda e, idx=i: self.set_rating(idx + 1))
            self.stars.append(star)

    def set_rating(self, rating):
      self.rating_value = rating
      for i, star in enumerate(self.stars):
        star.config(text="★" if i < rating else "☆", fg="#FFD700")
      self.rating_frame.destroy()  # Hide the whole rating frame after rating

    def update_canvas_size(self):
        w_px = int(self.room_width * self.scale)
        h_px = int(self.room_length * self.scale)
        self.canvas.config(width=w_px, height=h_px)
        self.canvas.delete("room_border")
        self.canvas.create_rectangle(0, 0, w_px, h_px, outline="#003366", width=5, tags="room_border")
        self.canvas.delete("dim_text")
        self.canvas.create_text(w_px / 2, h_px + 15, text=f"Length: {self.room_length} m", tags="dim_text", font=("Arial", 10, "bold"), fill="#003366")
        self.canvas.create_text(-30, h_px / 2, text=f"Width: {self.room_width} m", tags="dim_text", font=("Arial", 10, "bold"), fill="#003366", angle=90)

    def set_room_size(self):
        try:
            length = float(self.length_entry.get())
            width = float(self.width_entry.get())
            if length <= 0 or width <= 0:
                raise ValueError("Dimensions must be positive")
            self.room_length = length
            self.room_width = width
            self.update_canvas_size()
        except Exception as e:
            messagebox.showerror("Invalid input", f"Error: {e}")

    def pick_color(self):
        color = colorchooser.askcolor(title="Pick Furniture Color", initialcolor=self.selected_color)
        if color[1]:
            self.selected_color = color[1]
            self.color_btn.config(bg=self.selected_color)

    def add_furniture(self):
        if len(self.furniture_items) >= self.max_furniture:
            messagebox.showinfo("Limit reached", f"Maximum {self.max_furniture} furniture pieces allowed.")
            return
        try:
            name = self.f_name.get().strip()
            length = float(self.f_length.get())
            width = float(self.f_width.get())
            color = self.selected_color

            if not name:
                raise ValueError("Furniture name cannot be empty")
            if length <= 0 or width <= 0:
                raise ValueError("Furniture dimensions must be positive")

            w_px = int(width * self.scale)
            h_px = int(length * self.scale)
            x = 10 + len(self.furniture_items) * 40
            y = 10 + len(self.furniture_items) * 40

            rect = self.canvas.create_rectangle(x, y, x + w_px, y + h_px, fill=color, outline="#333333", width=2, tags="furniture")
            label = f"{name}\n{length:.1f}m x {width:.1f}m"
            text = self.canvas.create_text(x + w_px / 2, y + h_px / 2, text=label, fill="black", font=("Arial", 10), tags="furniture")

            self.furniture_items.append((rect, text))
            self.make_draggable(rect, text)

            self.canvas.tag_bind(rect, "<Button-3>", lambda e, r=rect, t=text: self.remove_furniture(r, t))
            self.canvas.tag_bind(text, "<Button-3>", lambda e, r=rect, t=text: self.remove_furniture(r, t))

            self.f_name.delete(0, tk.END)
            self.f_length.delete(0, tk.END)
            self.f_width.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error adding furniture", f"{e}")

    def make_draggable(self, rect, text):
        def start_drag(event):
            self._drag_data = {"x": event.x, "y": event.y}
            self.canvas.tag_raise(rect)
            self.canvas.tag_raise(text)

        def drag(event):
            dx = event.x - self._drag_data["x"]
            dy = event.y - self._drag_data["y"]

            x1, y1, x2, y2 = self.canvas.coords(rect)
            new_x1, new_y1 = x1 + dx, y1 + dy
            new_x2, new_y2 = x2 + dx, y2 + dy
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            if new_x1 < 0:
                dx -= new_x1
            if new_y1 < 0:
                dy -= new_y1
            if new_x2 > canvas_width:
                dx -= (new_x2 - canvas_width)
            if new_y2 > canvas_height:
                dy -= (new_y2 - canvas_height)

            self.canvas.move(rect, dx, dy)
            self.canvas.move(text, dx, dy)
            self._drag_data = {"x": event.x, "y": event.y}

        self.canvas.tag_bind(rect, "<ButtonPress-1>", start_drag)
        self.canvas.tag_bind(rect, "<B1-Motion>", drag)
        self.canvas.tag_bind(text, "<ButtonPress-1>", start_drag)
        self.canvas.tag_bind(text, "<B1-Motion>", drag)

    def remove_furniture(self, rect, text):
        self.canvas.delete(rect)
        self.canvas.delete(text)
        self.furniture_items = [(r, t) for r, t in self.furniture_items if r != rect and t != text]

    def reset(self):
        self.canvas.delete("all")
        self.furniture_items.clear()
        self.update_canvas_size()
        self.length_entry.delete(0, tk.END)
        self.length_entry.insert(0, "4.0")
        self.width_entry.delete(0, tk.END)
        self.width_entry.insert(0, "3.0")
        self.selected_color = "#87ceeb"
        self.color_btn.config(bg=self.selected_color)
        self.f_name.delete(0, tk.END)
        self.f_length.delete(0, tk.END)
        self.f_width.delete(0, tk.END)
        self.set_rating(0)

def open_room_edit():
    root = tk.Tk()
    root.title("Tk Example")
    root.configure(background="lightgray")
    root.minsize(200, 200)
    root.maxsize(1920, 1080)
    root.geometry("300x300")  # Set initial size

    # Center the window on the screen
    root.title("Room Planner")
    root.configure(background="#dbe9f4")
    root.geometry("1000x800")
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (300 // 2)
    y = (screen_height // 2) - (300 // 2)
    root.geometry(f"300x300+{x}+{y}")

    # Sample content for the logged-in user
    tk.Label(root, text="Welcome to the main window!").pack(pady=20)
    x = (screen_width // 2) - (1000 // 2)
    y = (screen_height // 2) - (800 // 2)
    root.geometry(f"1000x800+{x}+{y}")
    app = RoomPlannerApp(root)
    root.mainloop()

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

    tk.Button(root, text="Open room planner", command=open_room_edit).pack(pady=10)
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

if __name__ == "__main__":
    setup_database()
    create_login_window()
