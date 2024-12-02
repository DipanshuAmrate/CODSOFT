import tkinter as tk

# Function to update the expression in the entry box
def button_click(value):
    current_text = entry.get()
    entry.delete(0, tk.END)  # Clear current text in the entry
    entry.insert(tk.END, current_text + str(value))

# Function to clear the entry box
def button_clear():
    entry.delete(0, tk.END)

# Function to evaluate the expression
def button_equal():
    try:
        result = eval(entry.get())  # Evaluate the arithmetic expression
        entry.delete(0, tk.END)
        entry.insert(tk.END, result)  # Show result in entry box
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

# Function to toggle between light and dark mode
def toggle_theme():
    current_bg = window.cget('bg')
    if current_bg == "#F0F8FF":  # Light Blue (soft theme)
        window.config(bg="#2F4F4F")  # Dark Gray background (dark mode)
        entry.config(bg="#2F4F4F", fg="white")
        for button in window.winfo_children():
            if isinstance(button, tk.Button):
                button.config(bg="#4F5D75", fg="white", activebackground="#5B6E81")
    else:
        window.config(bg="#F0F8FF")  # Light Blue background (light mode)
        entry.config(bg="white", fg="black")
        for button in window.winfo_children():
            if isinstance(button, tk.Button):
                button.config(bg="#B0C4DE", fg="black", activebackground="#A9B9CC")

# Function to block alphabetical keys (A-Z)
def block_alphabets(event):
    if event.char.isalpha():  # If an alphabet key is pressed
        return "break"  # Prevent the event (blocking the key)
    return None  # Allow other keys

# Create the main window
window = tk.Tk()
window.title("Simple Calculator")
window.geometry("400x600")  # Adjusted window size
window.config(bg="#F0F8FF")  # Initial light theme (soft blue)

# Entry widget to display the numbers and results
entry = tk.Entry(window, font=("Arial", 24, "bold"), width=15, borderwidth=5, relief="solid", justify="right")
entry.grid(row=0, column=0, columnspan=4, pady=20)

# Button definitions
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
    ('C', 5, 0), ('(', 5, 1), (')', 5, 2), ('^', 5, 3)
]

# Add buttons to the grid layout
for (text, row, col) in buttons:
    if text == '=':
        button = tk.Button(window, text=text, width=5, height=2, font=("Arial", 18, "bold"), command=button_equal, bg="#A9B9CC", fg="black")
    elif text == 'C':
        button = tk.Button(window, text=text, width=5, height=2, font=("Arial", 18, "bold"), command=button_clear, bg="#A9B9CC", fg="black")
    else:
        button = tk.Button(window, text=text, width=5, height=2, font=("Arial", 18, "bold"), command=lambda value=text: button_click(value), bg="#B0C4DE", fg="black")
    
    button.grid(row=row, column=col, padx=10, pady=10)

# Add the theme toggle button to the layout
theme_button = tk.Button(window, text="Toggle Theme", width=15, height=2, font=("Arial", 14, "bold"), command=toggle_theme, bg="#A9B9CC", fg="black")
theme_button.grid(row=6, column=0, columnspan=4, pady=20)

# Bind the keyboard event to block alphabetical keys
window.bind("<Key>", block_alphabets)

# Start the main event loop
window.mainloop()
