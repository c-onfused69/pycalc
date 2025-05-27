# gui.py
import tkinter as tk
import re
from .calculator import Calculator

class RoundedButton(tk.Canvas):
    def __init__(self, parent, width=80, height=80, cornerradius=15, padding=5, 
                 bg="#333333", fg="white", text="", font=None, command=None):
        tk.Canvas.__init__(self, parent, width=width, height=height, 
                          highlightthickness=0, bg=parent['bg'])
        self.command = command
        self.cornerradius = cornerradius
        self.padding = padding
        self.bg = bg
        self.fg = fg
        self.text = text
        self.font = font or ('Segoe UI', 18, 'bold')
        self.width = width
        self.height = height
        self.is_pressed = False

        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

        self.draw_button(bg)

    def draw_button(self, color):
        self.delete("all")
        radius = self.cornerradius
        padding = self.padding
        w = self.width
        h = self.height
        
        # Draw rounded rectangle
        self.create_arc(padding, padding, padding+2*radius, padding+2*radius, 
                       start=90, extent=90, fill=color, outline=color)
        self.create_arc(w-padding-2*radius, padding, w-padding, padding+2*radius, 
                       start=0, extent=90, fill=color, outline=color)
        self.create_arc(padding, h-padding-2*radius, padding+2*radius, h-padding, 
                       start=180, extent=90, fill=color, outline=color)
        self.create_arc(w-padding-2*radius, h-padding-2*radius, w-padding, h-padding, 
                       start=270, extent=90, fill=color, outline=color)
        self.create_rectangle(padding+radius, padding, w-padding-radius, h-padding, 
                            fill=color, outline=color)
        self.create_rectangle(padding, padding+radius, w-padding, h-padding-radius, 
                            fill=color, outline=color)
        # Draw text
        self.create_text(w//2, h//2, text=self.text, fill=self.fg, font=self.font)

    def _on_press(self, event):
        self.is_pressed = True
        self.draw_button(self._lighten_color(self.bg, factor=0.3))

    def _on_release(self, event):
        if self.is_pressed:
            self.is_pressed = False
            self.draw_button(self.bg)
            if self.command:
                self.command()

    def _on_enter(self, event):
        if not self.is_pressed:
            self.draw_button(self._lighten_color(self.bg, factor=0.2))

    def _on_leave(self, event):
        if not self.is_pressed:
            self.draw_button(self.bg)

    def _lighten_color(self, hex_color, factor=0.2):
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        lighter = tuple(min(255, int(c + (255 - c) * factor)) for c in rgb)
        return f'#{lighter[0]:02x}{lighter[1]:02x}{lighter[2]:02x}'

class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self._configure_window()
        self._create_main_frame()
        self._create_display()
        self._create_buttons()
        self._configure_grid()
        self.error_displayed = False
        self.current_number = ""

    def _configure_window(self):
        self.root.title("PyCalc - Calculator")
        self.root.geometry("400x800")
        self.root.configure(bg="#0a0a0a")
        self.root.resizable(False, False)

    def _create_main_frame(self):
        self.main_frame = tk.Frame(self.root, bg="#121212")
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)

    def _create_display(self):
        self.display_frame = tk.Frame(self.main_frame, bg="#121212")
        self.display_frame.pack(fill="x", padx=10, pady=10)

        self.expression_var = tk.StringVar()
        self.result_var = tk.StringVar(value="0")

        self.expression_label = tk.Label(
            self.display_frame,
            textvariable=self.expression_var,
            font=('Segoe UI', 14),
            fg="#888888",
            bg="#121212",
            anchor="e"
        )
        self.expression_label.pack(fill="x")

        self.result_label = tk.Label(
            self.display_frame,
            textvariable=self.result_var,
            font=('Segoe UI', 36, 'bold'),
            fg="white",
            bg="#121212",
            anchor="e"
        )
        self.result_label.pack(fill="x")

    def _create_buttons(self):
        self.buttons_frame = tk.Frame(self.main_frame, bg="#121212")
        self.buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)

        buttons = [
            ['e', 'μ', 'sin', 'deg'],
            ['Ac', '()', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '⌫', '=']
        ]

        for row_idx, row in enumerate(buttons):
            for col_idx, text in enumerate(row):
                self._create_button(text, row_idx, col_idx)

    def _create_button(self, text, row, col):
        color_scheme = {
            'operator': {'bg': "#0a5edb", 'fg': "white"},
            'special': {'bg': "#2a2a2a", 'fg': "#888888"},
            'number': {'bg': "#1e1e1e", 'fg': "white"},
            'equals': {'bg': "#1e90ff", 'fg': "white"}
        }

        if text in {'÷', '×', '-', '+', '%'}:
            btn_type = 'operator'
        elif text in {'Ac', '()', 'deg', '⌫'}:
            btn_type = 'special'
        elif text == '=':
            btn_type = 'equals'
        else:
            btn_type = 'number'

        btn = RoundedButton(
            self.buttons_frame,
            width=80,
            height=80,
            cornerradius=15,
            padding=5,
            bg=color_scheme[btn_type]['bg'],
            fg=color_scheme[btn_type]['fg'],
            text=text,
            font=('Segoe UI', 18, 'bold'),
            command=None
        )

        if text == 'Ac':
            btn.command = self._clear_display
        elif text == '⌫':
            btn.command = self._backspace
        elif text == '=':
            btn.command = self._evaluate
        elif text == '()':
            btn.command = self._insert_parentheses
        else:
            operator_map = {'÷': '/', '×': '*'}
            btn.command = lambda t=text: self._add_to_display(operator_map.get(t, t))

        btn.grid(
            row=row,
            column=col,
            padx=2,
            pady=2,
            sticky="nsew"
        )

    def _configure_grid(self):
        for i in range(4):
            self.buttons_frame.grid_columnconfigure(i, weight=1, uniform="cols", minsize=80)
        for i in range(6):
            self.buttons_frame.grid_rowconfigure(i, weight=1, uniform="rows", minsize=80)

    def _add_to_display(self, value):
        current_expr = self.expression_var.get()
        
        # Track current number state
        if value in '0123456789.':
            self.current_number += value
        else:
            self.current_number = ""

        # Handle decimal point
        if value == '.':
            # Prevent multiple decimals in current number
            if '.' in self.current_number[:-1]:
                return
            # Add leading zero if needed
            if not current_expr or current_expr[-1] in '+-*/÷×':
                value = '0.'

        new_expr = current_expr + value
        self.expression_var.set(new_expr)
        self.result_var.set(new_expr or "0")

    def _insert_parentheses(self):
        current = self.expression_var.get()
        open_count = current.count('(') - current.count(')')
        self._add_to_display('(' if open_count <= 0 else ')')

    def _clear_display(self):
        self.expression_var.set("")
        self.result_var.set("0")
        self.current_number = ""
        self.error_displayed = False

    def _backspace(self):
        current = self.expression_var.get()
        if current:
            # Update current number state
            if current[-1] in '0123456789.':
                self.current_number = self.current_number[:-1]
            else:
                self.current_number = ""
            
            new_expr = current[:-1]
            self.expression_var.set(new_expr)
            self.result_var.set(new_expr or "0")

    def _evaluate(self):
        try:
            expression = self.expression_var.get()
            expression = expression.replace('÷', '/').replace('×', '*')
            
            # Handle trailing decimal
            if expression.endswith('.'):
                expression += '0'
                
            result = Calculator.evaluate(expression)
            formatted_result = f"{result:,}"
            self.result_var.set(formatted_result)
            self.expression_var.set("")
            self.current_number = ""
        except Exception:
            self.result_var.set("Error")
            self.expression_var.set("")
            self.current_number = ""
            self.error_displayed = True
            self.root.after(1000, self._clear_display)