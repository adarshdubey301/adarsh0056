import tkinter as tk
from tkinter import ttk
import tkinter.font as font

class ResponsiveCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Responsive Calculator")
        self.root.geometry("400x500")
        self.root.minsize(300, 400)  # Set minimum window size
        
        # Color scheme
        self.colors = {
            "background": "#f0f0f0",
            "display_bg": "#e8f4f8",
            "display_border": "#b0d8e8",
            "number_bg": "#ffffff",
            "number_fg": "#333333",
            "operation_bg": "#4a86e8",
            "operation_fg": "#ffffff",
            "equal_bg": "#43a047",
            "equal_fg": "#ffffff",
            "clear_bg": "#ef5350",
            "clear_fg": "#ffffff",
            "special_bg": "#ff9800",
            "special_fg": "#ffffff",
            "result_fg": "#0d47a1",
            "calculation_fg": "#546e7a"
        }
        
        # Set background color
        self.root.configure(bg=self.colors["background"])
        
        # Calculator variables
        self.current_input = ""
        self.current_calculation = ""
        
        # Configure root to be responsive
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=5)
        
        # Create frames
        self.create_display_frame()
        self.create_buttons_frame()
        
        # Set up responsiveness
        self.root.bind("<Configure>", self.on_resize)
    
    def create_display_frame(self):
        self.display_frame = tk.Frame(
            self.root, 
            bg=self.colors["display_bg"],
            highlightbackground=self.colors["display_border"],
            highlightthickness=2
        )
        self.display_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.display_frame.grid_columnconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(0, weight=2)
        self.display_frame.grid_rowconfigure(1, weight=1)
        
        # Result label
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.result_label = tk.Label(
            self.display_frame, 
            textvariable=self.result_var, 
            font=("Arial", 24, "bold"),
            anchor="e",
            bg=self.colors["display_bg"],
            fg=self.colors["result_fg"],
            padx=10,
            pady=5
        )
        self.result_label.grid(row=0, column=0, sticky="nsew")
        
        # Calculation label (shows the expression)
        self.calculation_var = tk.StringVar()
        self.calculation_label = tk.Label(
            self.display_frame, 
            textvariable=self.calculation_var, 
            font=("Arial", 12),
            anchor="e",
            bg=self.colors["display_bg"],
            fg=self.colors["calculation_fg"],
            padx=10,
            pady=5
        )
        self.calculation_label.grid(row=1, column=0, sticky="nsew")
    
    def create_buttons_frame(self):
        self.buttons_frame = tk.Frame(self.root, bg=self.colors["background"])
        self.buttons_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Configure buttons grid - 5 rows, 4 columns
        for i in range(5):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Button layout with button types for color differentiation
        button_layout = [
            ("C", 0, 0, "clear"), ("()", 0, 1, "special"), ("%", 0, 2, "special"), ("/", 0, 3, "operation"),
            ("7", 1, 0, "number"), ("8", 1, 1, "number"), ("9", 1, 2, "number"), ("*", 1, 3, "operation"),
            ("4", 2, 0, "number"), ("5", 2, 1, "number"), ("6", 2, 2, "number"), ("-", 2, 3, "operation"),
            ("1", 3, 0, "number"), ("2", 3, 1, "number"), ("3", 3, 2, "number"), ("+", 3, 3, "operation"),
            ("±", 4, 0, "special"), ("0", 4, 1, "number"), (".", 4, 2, "number"), ("=", 4, 3, "equal")
        ]
        
        self.buttons = {}
        self.button_fonts = {}
        
        for (text, row, col, btn_type) in button_layout:
            # Set colors based on button type
            if btn_type == "number":
                bg_color = self.colors["number_bg"]
                fg_color = self.colors["number_fg"]
            elif btn_type == "operation":
                bg_color = self.colors["operation_bg"]
                fg_color = self.colors["operation_fg"]
            elif btn_type == "equal":
                bg_color = self.colors["equal_bg"]
                fg_color = self.colors["equal_fg"]
            elif btn_type == "clear":
                bg_color = self.colors["clear_bg"]
                fg_color = self.colors["clear_fg"]
            elif btn_type == "special":
                bg_color = self.colors["special_bg"]
                fg_color = self.colors["special_fg"]
            
            # Create button with custom styling
            button_font = font.Font(family="Arial", size=12, weight="bold")
            self.button_fonts[text] = button_font
            
            button = tk.Button(
                self.buttons_frame, 
                text=text,
                font=button_font,
                bg=bg_color,
                fg=fg_color,
                activebackground=self.darken_color(bg_color),
                activeforeground=fg_color,
                relief=tk.RAISED,
                borderwidth=2,
                command=lambda t=text: self.on_button_click(t)
            )
            button.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
            self.buttons[text] = button
    
    def darken_color(self, hex_color):
        # Function to darken a color for button press effect
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        # Darken by 15%
        factor = 0.85
        r = int(max(r * factor, 0))
        g = int(max(g * factor, 0))
        b = int(max(b * factor, 0))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def on_button_click(self, button_text):
        if button_text == "C":
            self.clear()
        elif button_text == "=":
            self.calculate()
        elif button_text == "±":
            self.negate()
        elif button_text == "()":
            self.add_parenthesis()
        else:
            self.add_to_calculation(button_text)
    
    def clear(self):
        self.current_calculation = ""
        self.current_input = ""
        self.calculation_var.set("")
        self.result_var.set("0")
    
    def calculate(self):
        try:
            # Replace % with /100 for calculation
            expr = self.current_calculation.replace("%", "/100")
            result = eval(expr)
            
            # Format result to avoid long decimals
            if isinstance(result, float):
                # Display up to 8 decimal places, remove trailing zeros
                result_str = f"{result:.8f}".rstrip('0').rstrip('.')
                if len(result_str) > 12:  # If still too long, use scientific notation
                    result_str = f"{result:.6e}"
            else:
                result_str = str(result)
            
            # Update display
            self.calculation_var.set(self.current_calculation + "=")
            self.result_var.set(result_str)
            
            # Reset for new calculation, but keep result
            self.current_calculation = result_str
            self.current_input = result_str
        except Exception as e:
            self.result_var.set("Error")
            self.current_calculation = ""
            self.current_input = ""
    
    def negate(self):
        if self.current_input and self.current_input not in "+-*/()%":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            
            # Update calculation
            if self.current_calculation:
                # Find the last number in the calculation and replace it
                operations = "+-*/()%"
                i = len(self.current_calculation) - 1
                while i >= 0 and self.current_calculation[i] not in operations:
                    i -= 1
                
                if i < 0:  # No operations found
                    self.current_calculation = self.current_input
                else:
                    self.current_calculation = self.current_calculation[:i+1] + self.current_input
            else:
                self.current_calculation = self.current_input
            
            self.calculation_var.set(self.current_calculation)
            self.result_var.set(self.current_input)
    
    def add_parenthesis(self):
        # Simple logic to add matching parentheses
        open_count = self.current_calculation.count("(")
        close_count = self.current_calculation.count(")")
        
        if open_count > close_count:
            self.add_to_calculation(")")
        else:
            self.add_to_calculation("(")
    
    def add_to_calculation(self, value):
        operations = "+-*/%"
        
        # Handle operations
        if value in operations:
            self.current_input = ""
            self.current_calculation += value
        # Handle numbers and decimal
        else:
            if value == "." and "." in self.current_input:
                return  # Prevent multiple decimal points
            
            if self.current_input == "0" and value == "0":
                return  # Prevent leading zeros
            
            if self.current_input == "0" and value != ".":
                self.current_input = value
            else:
                self.current_input += value
            
            # If the last character was an operation, start a new input
            if self.current_calculation and self.current_calculation[-1] in operations:
                self.current_calculation += value
            # If last character was a closing parenthesis, add multiplication
            elif self.current_calculation and self.current_calculation[-1] == ")":
                self.current_calculation += "*" + value
            else:
                self.current_calculation += value
        
        # Update the display
        self.calculation_var.set(self.current_calculation)
        if self.current_input:
            self.result_var.set(self.current_input)
    
    def on_resize(self, event):
        # Adjust font sizes based on window width
        width = self.root.winfo_width()
        
        # Adjust display font sizes
        if width < 350:
            self.result_label.configure(font=("Arial", 18, "bold"))
            self.calculation_label.configure(font=("Arial", 10))
            button_font_size = 10
        else:
            self.result_label.configure(font=("Arial", 24, "bold"))
            self.calculation_label.configure(font=("Arial", 12))
            button_font_size = 12
        
        # Adjust button font sizes
        for text, button_font in self.button_fonts.items():
            button_font.configure(size=button_font_size)

if __name__ == "__main__":
    root = tk.Tk()
    app = ResponsiveCalculator(root)
    root.mainloop()
