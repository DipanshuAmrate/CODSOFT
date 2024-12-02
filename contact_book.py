import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import font

# Create SQLite database connection
conn = sqlite3.connect('contacts.db')
cursor = conn.cursor()

# Create the contacts table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    phone_number TEXT NOT NULL,
                    email TEXT NOT NULL,
                    address TEXT);''')
conn.commit()

# Function to add a new contact
def add_contact():
    def save_contact():
        name = entry_name.get()
        phone_number = entry_phone.get()
        email = entry_email.get()
        address = entry_address.get()
        
        if not (name and phone_number and email):
            messagebox.showwarning("Input Error", "All fields except Address are required!")
            return
        
        cursor.execute('''INSERT INTO contacts (name, phone_number, email, address) 
                          VALUES (?, ?, ?, ?)''', (name, phone_number, email, address))
        conn.commit()
        messagebox.showinfo("Success", "Contact added successfully!")
        add_window.destroy()
        refresh_contacts()

    add_window = tk.Toplevel(root)
    add_window.title("Add Contact")
    add_window.config(bg="#F5F5F5")  # Light gray background
    
    # Add Labels and Entry Fields with modern design
    tk.Label(add_window, text="Name:", bg="#F5F5F5", font=('Roboto', 12)).grid(row=0, column=0, pady=10)
    entry_name = tk.Entry(add_window, width=30, font=('Roboto', 12), bd=2, relief="solid", borderwidth=1)
    entry_name.grid(row=0, column=1, pady=10)
    
    tk.Label(add_window, text="Phone Number:", bg="#F5F5F5", font=('Roboto', 12)).grid(row=1, column=0, pady=10)
    entry_phone = tk.Entry(add_window, width=30, font=('Roboto', 12), bd=2, relief="solid", borderwidth=1)
    entry_phone.grid(row=1, column=1, pady=10)
    
    tk.Label(add_window, text="Email:", bg="#F5F5F5", font=('Roboto', 12)).grid(row=2, column=0, pady=10)
    entry_email = tk.Entry(add_window, width=30, font=('Roboto', 12), bd=2, relief="solid", borderwidth=1)
    entry_email.grid(row=2, column=1, pady=10)
    
    tk.Label(add_window, text="Address:", bg="#F5F5F5", font=('Roboto', 12)).grid(row=3, column=0, pady=10)
    entry_address = tk.Entry(add_window, width=30, font=('Roboto', 12), bd=2, relief="solid", borderwidth=1)
    entry_address.grid(row=3, column=1, pady=10)
    
    # Rounded "Save" Button with custom design
    tk.Button(add_window, text="Save", command=save_contact, bg="#2196F3", fg="white", font=('Roboto', 12), 
              relief="flat", width=15, height=2).grid(row=4, column=0, columnspan=2, pady=20)

# Function to display all contacts
def view_contacts():
    contacts_window = tk.Toplevel(root)
    contacts_window.title("View Contacts")
    contacts_window.config(bg="#F5F5F5")
    
    # Query database for all contacts
    cursor.execute("SELECT id, name, phone_number FROM contacts")
    rows = cursor.fetchall()

    # Display in Listbox
    listbox = tk.Listbox(contacts_window, height=15, width=50, font=('Roboto', 12), bg="#F5F5F5", bd=2, 
                         selectmode=tk.SINGLE, activestyle="none")
    listbox.grid(row=0, column=0, padx=20, pady=10)

    for row in rows:
        listbox.insert(tk.END, f"{row[1]} - {row[2]}")  # Show name and phone number
    
    def on_select(event):
        selected = listbox.curselection()
        if selected:
            contact_id = rows[selected[0]][0]
            edit_contact(contact_id)

    listbox.bind('<<ListboxSelect>>', on_select)

# Function to update a contact's details
def edit_contact(contact_id):
    cursor.execute("SELECT * FROM contacts WHERE id=?", (contact_id,))
    contact = cursor.fetchone()

    def update_contact():
        name = entry_name.get()
        phone_number = entry_phone.get()
        email = entry_email.get()
        address = entry_address.get()
        
        if not (name and phone_number and email):
            messagebox.showwarning("Input Error", "All fields except Address are required!")
            return
        
        cursor.execute('''UPDATE contacts SET name=?, phone_number=?, email=?, address=? 
                          WHERE id=?''', (name, phone_number, email, address, contact_id))
        conn.commit()
        messagebox.showinfo("Success", "Contact updated successfully!")
        edit_window.destroy()
        refresh_contacts()

    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Contact")
    edit_window.config(bg="#F5F5F5")
    
    tk.Label(edit_window, text="Name:", bg="#F5F5F5", font=('Roboto', 12)).grid(row=0, column=0, pady=10)
    entry_name = tk.Entry(edit_window, width=30, font=('Roboto', 12), bd=2, relief="solid", borderwidth=1)
    entry_name.grid(row=0, column=1, pady=10)
    entry_name.insert(0, contact[1])
    
    tk.Label(edit_window, text="Phone Number:", bg="#F5F5F5", font=('Roboto', 12)).grid(row=1, column=0, pady=10)
    entry_phone = tk.Entry(edit_window, width=30, font=('Roboto', 12), bd=2, relief="solid", borderwidth=1)
    entry_phone.grid(row=1, column=1, pady=10)
    entry_phone.insert(0, contact[2])
    
    tk.Label(edit_window, text="Email:", bg="#F5F5F5", font=('Roboto', 12)).grid(row=2, column=0, pady=10)
    entry_email = tk.Entry(edit_window, width=30, font=('Roboto', 12), bd=2, relief="solid", borderwidth=1)
    entry_email.grid(row=2, column=1, pady=10)
    entry_email.insert(0, contact[3])
    
    tk.Label(edit_window, text="Address:", bg="#F5F5F5", font=('Roboto', 12)).grid(row=3, column=0, pady=10)
    entry_address = tk.Entry(edit_window, width=30, font=('Roboto', 12), bd=2, relief="solid", borderwidth=1)
    entry_address.grid(row=3, column=1, pady=10)
    entry_address.insert(0, contact[4])
    
    tk.Button(edit_window, text="Save", command=update_contact, bg="#2196F3", fg="white", font=('Roboto', 12), 
              relief="flat", width=15, height=2).grid(row=4, column=0, columnspan=2, pady=20)

# Function to delete a contact
def delete_contact():
    contact_id = simpledialog.askinteger("Delete Contact", "Enter the ID of the contact to delete:")
    if contact_id:
        cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
        conn.commit()
        messagebox.showinfo("Success", "Contact deleted successfully!")
        refresh_contacts()

# Function to refresh contacts list (after adding, updating, or deleting)
def refresh_contacts():
    pass  # This function would re-fetch contacts and refresh the UI if needed.

# Main Window Setup
root = tk.Tk()
root.title("Contact Book")
root.config(bg="#F5F5F5")  # Light gray background
root.geometry("450x600")  # Initial window size

# Set font style for the main window
font_style = font.Font(family="Roboto", size=12)

# Add buttons with rounded design and material colors
tk.Button(root, text="Add Contact", command=add_contact, bg="#2196F3", fg="white", font=font_style, 
          relief="flat", width=20, height=2).pack(pady=20)

tk.Button(root, text="View Contacts", command=view_contacts, bg="#4CAF50", fg="white", font=font_style, 
          relief="flat", width=20, height=2).pack(pady=20)

tk.Button(root, text="Delete Contact", command=delete_contact, bg="#F44336", fg="white", font=font_style, 
          relief="flat", width=20, height=2).pack(pady=20)

root.mainloop()
