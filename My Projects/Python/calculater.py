import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#2C3E50')
        
        # Variables
        self.expression = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Display Frame
        display_frame = tk.Frame(self.root, bg='#34495E', height=150)
        display_frame.pack(expand=True, fill='both')
        
        # Expression Label
        self.expression_label = tk.Label(
            display_frame,
            text="",
            font=('Arial', 14),
            bg='#34495E',
            fg='#ECF0F1',
            anchor='e'
        )
        self.expression_label.pack(expand=True, fill='both', padx=10, pady=(20, 5))
        
        # Result Display
        result_label = tk.Label(
            display_frame,
            textvariable=self.result_var,
            font=('Arial', 32, 'bold'),
            bg='#34495E',
            fg='white',
            anchor='e'
        )
        result_label.pack(expand=True, fill='both', padx=10, pady=(5, 20))
        
        # Buttons Frame
        buttons_frame = tk.Frame(self.root, bg='#2C3E50')
        buttons_frame.pack(expand=True, fill='both')
        
        # Button configuration
        buttons = [
            ['C', '⌫', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '=']
        ]
        
        # Create buttons
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text == '=':
                    btn = self.create_button(
                        buttons_frame,
                        text,
                        self.calculate,
                        bg='#E67E22',
                        fg='white'
                    )
                elif text == 'C':
                    btn = self.create_button(
                        buttons_frame,
                        text,
                        self.clear,
                        bg='#E74C3C',
                        fg='white'
                    )
                elif text == '⌫':
                    btn = self.create_button(
                        buttons_frame,
                        text,
                        self.backspace,
                        bg='#95A5A6',
                        fg='white'
                    )
                elif text in ['/', '*', '-', '+', '%']:
                    btn = self.create_button(
                        buttons_frame,
                        text,
                        self.add_to_expression,
                        bg='#3498DB',
                        fg='white'
                    )
                elif text == '±':
                    btn = self.create_button(
                        buttons_frame,
                        text,
                        self.toggle_sign,
                        bg='#95A5A6',
                        fg='white'
                    )
                else:
                    btn = self.create_button(
                        buttons_frame,
                        text,
                        self.add_to_expression,
                        bg='#ECF0F1',
                        fg='#2C3E50'
                    )
                
                btn.grid(row=i, column=j, padx=2, pady=2, sticky='nsew')
        
        # Configure grid weights
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.grid_columnconfigure(j, weight=1)
    
    def create_button(self, parent, text, command, bg='#ECF0F1', fg='#2C3E50'):
        return tk.Button(
            parent,
            text=text,
            font=('Arial', 18, 'bold'),
            bg=bg,
            fg=fg,
            bd=0,
            command=lambda: command(text) if command else None,
            activebackground=self.darken_color(bg),
            activeforeground=fg
        )
    
    def darken_color(self, color):
        """Darken a color for button hover effect"""
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            r = max(0, r - 30)
            g = max(0, g - 30)
            b = max(0, b - 30)
            
            return f'#{r:02x}{g:02x}{b:02x}'
        return color
    
    def add_to_expression(self, value):
        """Add value to expression"""
        if self.result_var.get() == "Error":
            self.clear()
        
        current = self.result_var.get()
        
        # Handle decimal points
        if value == '.' and '.' in current.split()[-1]:
            return
        
        # Handle operators
        if value in ['+', '-', '*', '/', '%']:
            if current and current[-1] in ['+', '-', '*', '/', '%']:
                return
        
        if current == "0":
            self.result_var.set(value)
        else:
            self.result_var.set(current + value)
    
    def calculate(self, *args):
        """Calculate the expression"""
        try:
            expression = self.result_var.get()
            
            # Replace symbols for eval
            expression = expression.replace('×', '*').replace('÷', '/')
            
            # Handle percentage
            if '%' in expression:
                expression = expression.replace('%', '/100')
            
            result = eval(expression)
            
            # Handle division by zero
            if result == float('inf') or result == -float('inf'):
                self.result_var.set("Error")
                return
            
            # Format result
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 10)
            
            self.result_var.set(str(result))
            
        except ZeroDivisionError:
            self.result_var.set("Error")
        except Exception:
            self.result_var.set("Error")
    
    def clear(self, *args):
        """Clear all"""
        self.result_var.set("0")
    
    def backspace(self, *args):
        """Remove last character"""
        current = self.result_var.get()
        if len(current) > 1:
            self.result_var.set(current[:-1])
        else:
            self.result_var.set("0")
    
    def toggle_sign(self, *args):
        """Toggle positive/negative sign"""
        try:
            current = float(self.result_var.get())
            current = -current
            if current.is_integer():
                current = int(current)
            self.result_var.set(str(current))
        except:
            pass

def main():
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()