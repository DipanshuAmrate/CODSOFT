import tkinter as tk
import string
import random

# Function to generate the password
def generate_password():
    try:
        length = int(entry_length.get())  # Get length of password

        # List to hold the character set based on user selection
        characterList = ""

        # Collect user preferences for character set
        if var_digits.get():
            characterList += string.digits
        if var_letters.get():
            characterList += string.ascii_letters
        if var_special.get():
            characterList += string.punctuation
        
        if not characterList:  # If no character set is selected
            result_label.config(text="Please select at least one character set.")
            return

        # Generate the password by picking random characters from the selected sets
        password = ''.join(random.choice(characterList) for _ in range(length))
        
        # Display the generated password in the result label
        result_label.config(text="Generated Password: " + password)

    except ValueError:
        result_label.config(text="Please enter a valid number for password length.")

# Create the main window
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x350")
root.config(bg="#E1F5FE")  # Light background color

# Font style for the UI
font_style = ('Helvetica', 12)

# Label and input for password length
tk.Label(root, text="Enter Password Length:", bg="#E1F5FE", font=font_style).pack(pady=10)

entry_length = tk.Entry(root, font=font_style, width=10, justify="center")
entry_length.pack(pady=5)
entry_length.insert(0, "8")  # Default value

# Checkboxes for character set options
var_digits = tk.BooleanVar()
var_letters = tk.BooleanVar()
var_special = tk.BooleanVar()

# Character set options
tk.Checkbutton(root, text="Include Digits", variable=var_digits, bg="#E1F5FE", font=font_style).pack(pady=5)
tk.Checkbutton(root, text="Include Letters", variable=var_letters, bg="#E1F5FE", font=font_style).pack(pady=5)
tk.Checkbutton(root, text="Include Special Characters", variable=var_special, bg="#E1F5FE", font=font_style).pack(pady=5)

# Button to generate the password
generate_button = tk.Button(root, text="Generate Password", command=generate_password, bg="#4CAF50", fg="white", font=font_style, width=20, height=2)
generate_button.pack(pady=20)

# Label to display the generated password
result_label = tk.Label(root, text="Generated Password:", bg="#E1F5FE", font=font_style, wraplength=350)
result_label.pack(pady=10)

# Exit button to close the application
exit_button = tk.Button(root, text="Exit", command=root.quit, bg="#F44336", fg="white", font=font_style, width=20, height=2)
exit_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
