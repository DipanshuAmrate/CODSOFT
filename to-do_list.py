from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

# Functions
def add_task():
    task_string = task_field.get()
    if len(task_string) == 0:
        messagebox.showinfo('Error', 'Field is Empty.')
    elif task_string in tasks:
        messagebox.showinfo('Error', 'Task already exists.')
    else:
        tasks.append(task_string)
        try:
            the_cursor.execute('INSERT INTO tasks VALUES (?)', (task_string,))
            the_connection.commit()  # Save changes
            list_update()
            task_field.delete(0, 'end')
        except sql.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

def list_update():
    clear_list()
    for idx, task in enumerate(tasks):
        var = BooleanVar()  # To track the checkbox state (checked/unchecked)
        checkbox = Checkbutton(task_frame, text=task, variable=var, bg="white", fg="black", font=("Arial", 12))
        checkbox.grid(row=idx, column=0, sticky="w", padx=10, pady=5)
        task_checkboxes.append((checkbox, var))  # Save the checkbox and variable reference

def remove_checked_tasks():
    tasks_to_remove = []  # List to hold tasks that are checked
    for idx, (checkbox, var) in enumerate(task_checkboxes):
        if var.get() == 1:  # If checkbox is checked (marked)
            task_to_remove = tasks[idx]
            tasks_to_remove.append(task_to_remove)
    
    # Remove the tasks from the list and database
    for task in tasks_to_remove:
        tasks.remove(task)
        try:
            the_cursor.execute('DELETE FROM tasks WHERE title = ?', (task,))
            the_connection.commit()  # Commit changes to the database
        except sql.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
    
    # Update the list to reflect the changes
    list_update()

def delete_all_tasks():
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')
    if message_box:
        try:
            tasks.clear()
            the_cursor.execute('DELETE FROM tasks')
            the_connection.commit()
            list_update()
        except sql.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

def clear_list():
    for checkbox, _ in task_checkboxes:
        checkbox.grid_forget()  # Remove all checkboxes from the frame
    task_checkboxes.clear()  # Clear the stored checkboxes

def toggle_theme():
    current_bg = guiWindow.cget('bg')
    if current_bg == '#FFA500':  # Orange mode
        guiWindow.configure(bg='#333333')
        task_frame.configure(bg='#555555')
    else:  # Dark mode
        guiWindow.configure(bg='#FFA500')
        task_frame.configure(bg='white')

def close():
    if messagebox.askyesno('Exit', 'Are you sure you want to close?'):
        guiWindow.destroy()

def retrieve_database():
    try:
        tasks.clear()
        for row in the_cursor.execute('SELECT title FROM tasks'):
            tasks.append(row[0])
    except sql.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

# Main GUI Application
if __name__ == "__main__":
    guiWindow = Tk()
    guiWindow.title("To-Do List")
    guiWindow.geometry("665x500+550+250")  # Adjusted height for more space
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#FFA500")  # Orange background

    # Database Setup
    try:
        the_connection = sql.connect('listOfTasks.db')
        the_cursor = the_connection.cursor()
        the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT)')
    except sql.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    tasks = []
    task_checkboxes = []  # To store checkbox references

    # Frames and Widgets
    functions_frame = Frame(guiWindow, bg="#FFA500")  # Orange background for the top section
    functions_frame.pack(side="top", expand=True, fill="both")

    task_label = Label(
        functions_frame,
        text="TO-DO-LIST \n Enter the Task Title:",
        font=("arial", "14", "bold"),
        background="#FFA500",  # Orange background
        foreground="black",    # Black text
    )
    task_label.place(x=20, y=30)

    task_field = Entry(
        functions_frame,
        font=("Arial", "14"),
        width=42,
        foreground="black",
        background="white",
    )
    task_field.place(x=180, y=30)

    add_button = Button(
        functions_frame,
        text="Add",
        width=15,
        bg="#555555",  # Dark button color
        font=("arial", "14", "bold"),
        command=add_task,
        fg="white"
    )
    del_button = Button(
        functions_frame,
        text="Remove Checked",
        width=15,
        bg="#555555",  # Dark button color
        font=("arial", "14", "bold"),
        command=remove_checked_tasks,
        fg="white"
    )
    del_all_button = Button(
        functions_frame,
        text="Delete All",
        width=15,
        font=("arial", "14", "bold"),
        bg="#555555",  # Dark button color
        command=delete_all_tasks,
        fg="white"
    )
    exit_button = Button(
        functions_frame,
        text="Exit / Close",
        width=52,
        bg="#555555",  # Dark button color
        font=("arial", "14", "bold"),
        command=close,
        fg="white"
    )
    theme_button = Button(
        functions_frame,
        text="Toggle Theme",
        width=15,
        bg="#555555",  # Dark button color
        font=("arial", "14", "bold"),
        command=toggle_theme,
        fg="white"
    )

    add_button.place(x=18, y=80)
    del_button.place(x=240, y=80)
    del_all_button.place(x=460, y=80)
    exit_button.place(x=17, y=330)
    theme_button.place(x=460, y=330)

    # Create a frame for the task list (white background section)
    task_frame = Frame(guiWindow, bg="white")
    task_frame.place(x=17, y=140, width=630, height=160)  # Position under the white section

    # Retrieve data and bind events
    retrieve_database()
    list_update()
    guiWindow.bind('<Return>', lambda event: add_task())
    guiWindow.bind('<Delete>', lambda event: remove_checked_tasks())

    guiWindow.mainloop()

    # Save changes and close database connection
    the_connection.commit()
    the_cursor.close()
