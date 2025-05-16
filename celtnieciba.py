import tkinter as tk
from tkinter import messagebox, colorchooser

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

if __name__ == "__main__":
    root = tk.Tk()
    app = RoomPlannerApp(root)
    root.mainloop()