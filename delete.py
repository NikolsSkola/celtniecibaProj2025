import tkinter as tk
import sqlite3
from PIL import Image, ImageTk
import io

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

def main_menu():
    """Create the main menu with a button to open the gallery."""
    root = tk.Tk()
    root.title("Galvenā izvēlne")
    tk.Button(root, text="Atvērt attēlu galeriju", command=open_gallery).pack(pady=20, padx=50)
    center_window(root, 300, 150)
    root.mainloop()

# Run the main menu
main_menu()
