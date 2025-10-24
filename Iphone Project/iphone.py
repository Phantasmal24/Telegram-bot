import tkinter as tk
from tkinter import font
import calendar
import datetime

# --- Main Application ---
class iPhoneSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # --- Configure the main window (the "phone") ---
        self.title("Python iPhone")
        self.geometry("375x812")  # Typical iPhone X/11 dimensions
        self.resizable(False, False)
        self.configure(bg="#111") # Phone body color

        # --- Create the "screen" ---
        # This is a container where all app content will go
        self.screen_frame = tk.Frame(self, width=360, height=790, bg="white", highlightthickness=0)
        self.screen_frame.pack(pady=10, padx=8)
        self.screen_frame.pack_propagate(False) # Prevents frame from shrinking to fit content

        # --- Container for all app frames ---
        # We'll stack all app frames in this container and raise the one we want to see
        self.app_container = tk.Frame(self.screen_frame, bg="white")
        self.app_container.pack(fill="both", expand=True)
        self.app_container.grid_rowconfigure(0, weight=1)
        self.app_container.grid_columnconfigure(0, weight=1)

        # --- Dictionary to store app frames ---
        self.app_frames = {}

        # --- Create and store each app frame ---
        for AppClass in (HomeScreen, CalculatorApp, CalendarApp, MapsApp):
            frame_name = AppClass.__name__
            frame = AppClass(parent=self.app_container, controller=self)
            self.app_frames[frame_name] = frame
            # Place each frame in the same grid cell
            frame.grid(row=0, column=0, sticky="nsew")

        # --- Show the Home Screen first ---
        self.show_frame("HomeScreen")

    def show_frame(self, frame_name):
        """Raises the specified frame to the top."""
        frame = self.app_frames[frame_name]
        frame.tkraise()

    def show_home(self):
        """A dedicated method to return to the home screen."""
        self.show_frame("HomeScreen")

# --- Base App Frame ---
class AppFrame(tk.Frame):
    """Base class for all 'app' screens."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        
        # Default app font
        self.app_font = font.Font(family="Helvetica", size=16)
        self.title_font = font.Font(family="Helvetica", size=20, weight="bold")

    def create_home_bar(self):
        """Creates a 'home bar' to return to the home screen."""
        home_bar_frame = tk.Frame(self, bg="#f0f0f0", height=40)
        home_bar_frame.pack(side="bottom", fill="x")
        
        home_button = tk.Button(
            home_bar_frame, 
            text="—", 
            font=font.Font(family="Helvetica", size=20, weight="bold"),
            command=self.controller.show_home,
            bg="#f0f0f0", 
            fg="black", 
            bd=0, 
            activebackground="#d0d0d0"
        )
        home_button.pack(pady=5)

# --- Home Screen App ---
class HomeScreen(tk.Frame):
    """The main home screen with app icons."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Set a background color (simulating wallpaper)
        self.configure(bg="#87CEEB") # Sky blue

        icon_font = font.Font(family="Helvetica", size=10)
        
        # --- App Icons Grid ---
        icon_frame = tk.Frame(self, bg="#87CEEB")
        icon_frame.pack(expand=True, pady=40, padx=20)

        # Calculator Icon
        calc_btn = self.create_app_icon(icon_frame, "🧮", "Calculator", lambda: controller.show_frame("CalculatorApp"))
        calc_btn.grid(row=0, column=0, padx=20, pady=20)

        # Calendar Icon
        cal_btn = self.create_app_icon(icon_frame, "📅", "Calendar", lambda: controller.show_frame("CalendarApp"))
        cal_btn.grid(row=0, column=1, padx=20, pady=20)
        
        # Maps Icon
        maps_btn = self.create_app_icon(icon_frame, "🗺️", "Maps", lambda: controller.show_frame("MapsApp"))
        maps_btn.grid(row=0, column=2, padx=20, pady=20)

    def create_app_icon(self, parent, icon_text, label_text, command):
        """Helper to create an app icon button."""
        frame = tk.Frame(parent, bg="#87CEEB")
        
        icon_btn = tk.Button(
            frame, 
            text=icon_text, 
            font=font.Font(family="Helvetica", size=36),
            bg="white", 
            bd=1,
            relief="raised",
            width=3, 
            height=1,
            command=command
        )
        icon_btn.pack(pady=(0, 5))
        
        label = tk.Label(frame, text=label_text, bg="#87CEEB", fg="white", font=font.Font(family="Helvetica", size=12))
        label.pack()
        
        return frame

# --- Calculator App ---
class CalculatorApp(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.configure(bg="#333") # Calculator background
        
        self.expression = ""

        # --- Display Screen ---
        self.display_var = tk.StringVar(value="0")
        display_font = font.Font(family="Helvetica", size=48)
        display = tk.Entry(
            self, 
            textvariable=self.display_var, 
            font=display_font, 
            bg="#333", 
            fg="white", 
            bd=0, 
            relief="flat", 
            justify="right", 
            state="readonly"
        )
        display.pack(fill="x", pady=20, padx=10, ipady=10)

        # --- Button Grid ---
        button_frame = tk.Frame(self, bg="#333")
        button_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        buttons = [
            ('C', 1, 0, '#aaa', 'black'), ('+/-', 1, 1, '#aaa', 'black'), ('%', 1, 2, '#aaa', 'black'), ('/', 1, 3, '#f69906', 'white'),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3, '#f69906', 'white'),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3, '#f69906', 'white'),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3, '#f69906', 'white'),
            ('0', 5, 0, None, None, 2), ('.', 5, 2), ('=', 5, 3, '#f69906', 'white'),
        ]
        
        btn_font = font.Font(family="Helvetica", size=24)
        
        for i in range(6):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)

        for btn in buttons:
            text = btn[0]
            row = btn[1]
            col = btn[2]
            bg_color = btn[3] if len(btn) > 3 else '#555'
            fg_color = btn[4] if len(btn) > 4 else 'white'
            col_span = btn[5] if len(btn) > 5 else 1
            
            self.create_calc_button(
                button_frame, text, row, col, bg_color, fg_color, btn_font, col_span
            )
            
        self.create_home_bar()

    def create_calc_button(self, parent, text, row, col, bg, fg, font, cspan=1):
        btn = tk.Button(
            parent, 
            text=text, 
            font=font, 
            bg=bg, 
            fg=fg, 
            bd=0, 
            relief="flat",
            command=lambda t=text: self.on_calc_click(t)
        )
        btn.grid(row=row, column=col, columnspan=cspan, sticky="nsew", padx=2, pady=2)
        return btn

    def on_calc_click(self, char):
        if char == 'C':
            self.expression = ""
            self.display_var.set("0")
        elif char == '=':
            try:
                # Using eval is generally unsafe, but fine for this simple, controlled app
                result = str(eval(self.expression))
                self.display_var.set(result)
                self.expression = result
            except Exception:
                self.display_var.set("Error")
                self.expression = ""
        elif char == '+/-':
            if self.expression and self.expression[0] == '-':
                self.expression = self.expression[1:]
            else:
                self.expression = '-' + self.expression
            self.display_var.set(self.expression)
        else:
            if self.expression == "0" or self.expression == "Error":
                self.expression = ""
            
            self.expression += str(char)
            self.display_var.set(self.expression)

# --- Calendar App ---
class CalendarApp(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.today = datetime.date.today()
        self.current_year = self.today.year
        self.current_month = self.today.month
        
        # --- Header ---
        header_frame = tk.Frame(self, bg="white")
        header_frame.pack(fill="x", pady=10)
        
        self.month_year_label = tk.Label(header_frame, text="", font=self.title_font, bg="white")
        self.month_year_label.pack(side="top", pady=10)
        
        btn_frame = tk.Frame(header_frame, bg="white")
        btn_frame.pack()
        
        prev_btn = tk.Button(btn_frame, text="< Prev", font=self.app_font, command=self.prev_month, bg="#eee", bd=0, relief="flat")
        prev_btn.pack(side="left", padx=10)
        
        next_btn = tk.Button(btn_frame, text="Next >", font=self.app_font, command=self.next_month, bg="#eee", bd=0, relief="flat")
        next_btn.pack(side="left", padx=10)

        # --- Calendar Display ---
        self.calendar_label = tk.Label(
            self, 
            font=font.Font(family="Courier", size=18), 
            justify="left", 
            bg="white", 
            anchor="n"
        )
        self.calendar_label.pack(fill="both", expand=True, padx=10)
        
        self.update_calendar()
        self.create_home_bar()

    def update_calendar(self):
        # Get calendar string
        cal_str = calendar.month(self.current_year, self.current_month)
        
        # Update labels
        month_name = datetime.date(self.current_year, self.current_month, 1).strftime('%B')
        self.month_year_label.config(text=f"{month_name} {self.current_year}")
        self.calendar_label.config(text=cal_str)

    def prev_month(self):
        self.current_month -= 1
        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1
        self.update_calendar()

    def next_month(self):
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
        self.update_calendar()

# --- Maps App ---
class MapsApp(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # --- Search Bar ---
        search_frame = tk.Frame(self, bg="white", pady=10, padx=10)
        search_frame.pack(fill="x")
        
        self.search_entry = tk.Entry(search_frame, font=self.app_font, bg="#f0f0f0", bd=0, relief="flat")
        self.search_entry.pack(side="left", fill="x", expand=True, ipady=5)
        
        search_btn = tk.Button(search_frame, text="Search", font=self.app_font, command=self.search_location, bg="#007AFF", fg="white", bd=0)
        search_btn.pack(side="left", padx=(5,0))

        # --- Map Canvas ---
        self.map_canvas = tk.Canvas(self, bg="#AADAFF") # Light blue for "water"
        self.map_canvas.pack(fill="both", expand=True)

        # --- Simple "Database" of locations ---
        self.locations = {
            "paris": (180, 150, "Paris, France"),
            "london": (160, 130, "London, UK"),
            "new york": (90, 180, "New York, USA"),
            "tokyo": (280, 200, "Tokyo, Japan"),
            "sydney": (300, 350, "Sydney, Australia"),
            "diphu": (250, 240, "Diphu, India")
        }
        
        # Draw a default "world"
        self.map_canvas.create_rectangle(50, 50, 310, 400, fill="#D2B48C", outline="") # Brown for "land"
        self.map_canvas.create_text(180, 30, text="Simplified World Map", font=self.app_font, fill="#333")

        self.create_home_bar()

    def search_location(self):
        # Clear previous searches
        self.map_canvas.delete("location_pin")
        self.map_canvas.delete("location_label")
        
        query = self.search_entry.get().lower()
        
        if query in self.locations:
            x, y, full_name = self.locations[query]
            
            # Create a pin
            self.map_canvas.create_oval(x-5, y-15, x+5, y, fill="red", outline="white", width=2, tags="location_pin")
            self.map_canvas.create_polygon(x, y, x-5, y-15, x+5, y-15, fill="red", outline="white", width=2, tags="location_pin")
            
            # Create a label
            self.map_canvas.create_text(x, y+10, text=full_name, font=self.app_font, fill="black", tags="location_label")
        else:
            # Show "Not Found"
            self.map_canvas.create_text(
                180, 250, 
                text="Location not found.", 
                font=self.title_font, 
                fill="red", 
                tags="location_label"
            )


# --- Run the application ---
if __name__ == "__main__":
    app = iPhoneSimulator()
    app.mainloop()