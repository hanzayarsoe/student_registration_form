import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="student_db"
)
cursor = db.cursor()

def insert_data():
    student_id = student_id_entry.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    address = address_entry.get()
    phone = phone_entry.get()
    
    insert_query = "INSERT INTO students (student_id, first_name, last_name, address, phone) VALUES (%s, %s, %s, %s, %s)"
    values = (student_id, first_name, last_name, address, phone)
    
    cursor.execute(insert_query, values)
    db.commit()
    clear_entries()
    refresh_table()

def update_data():
    selected = tree.selection()
    if not selected:
        return
    
    student_id = student_id_entry.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    address = address_entry.get()
    phone = phone_entry.get()

    for item in selected:
        # Get the database record ID from the first column of the selected item
        record_id = tree.item(item, "values")[0]

        # Update the record in the database using the ID
        update_query = "UPDATE students SET student_id = %s, first_name = %s, last_name = %s, address = %s, phone = %s WHERE id = %s"
        values = (student_id, first_name, last_name, address, phone, record_id)

        cursor.execute(update_query, values)
        db.commit()

        # Update the item in the Treeview
        tree.item(item, values=(record_id, student_id, first_name, last_name, address, phone))

    clear_entries()


def delete_data():
    selected = tree.selection()
    if not selected:
        return
    for item in selected:
        # Get the database record ID from the first column of the selected item
        record_id = tree.item(item, "values")[0]
        
        # Delete the record from the database using the ID
        delete_query = "DELETE FROM students WHERE id = %s"
        cursor.execute(delete_query, (record_id,))
        db.commit()
        
        # Delete the item from the Treeview
        tree.delete(item)
    
    clear_entries()

def search_data():
    student_id = student_id_entry.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    
    search_query = "SELECT * FROM students WHERE student_id LIKE %s AND first_name LIKE %s AND last_name LIKE %s"
    
    cursor.execute(search_query, (f"%{student_id}%", f"%{first_name}%", f"%{last_name}%"))
    results = cursor.fetchall()
    clear_table()
    for row in results:
        tree.insert('', 'end', values=row)

def clear_entries():
    student_id_entry.delete(0, tk.END)
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)

def clear_table():
    for record in tree.get_children():
        tree.delete(record)

def refresh_table():
    cursor.execute("SELECT * FROM students")
    results = cursor.fetchall()
    clear_table()
    for row in results:
        tree.insert('', 'end', values=row)

def on_closing():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()

# Create the main window
root = tk.Tk()
root.title("Student Registration System")
root.minsize(600, 400)
root.protocol("WM_DELETE_WINDOW", on_closing)

# Create the title
title = tk.Label(root, text="Student Registration Form", font=('Arial Bold', 20))
title.grid(row=0, column=0, columnspan=3)

# Create labels and entry fields
student_id_label = tk.Label(root, text="Student ID:")
student_id_label.grid(row=1, column=0)
student_id_entry = tk.Entry(root)
student_id_entry.grid(row=1, column=1)

first_name_label = tk.Label(root, text="First Name:")
first_name_label.grid(row=2, column=0)
first_name_entry = tk.Entry(root)
first_name_entry.grid(row=2, column=1)

last_name_label = tk.Label(root, text="Last Name:")
last_name_label.grid(row=3, column=0)
last_name_entry = tk.Entry(root)
last_name_entry.grid(row=3, column=1)

address_label = tk.Label(root, text="Address:")
address_label.grid(row=4, column=0)
address_entry = tk.Entry(root)
address_entry.grid(row=4, column=1)

phone_label = tk.Label(root, text="Phone:")
phone_label.grid(row=5, column=0)
phone_entry = tk.Entry(root)
phone_entry.grid(row=5, column=1)

# Create buttons
insert_button = tk.Button(root, text="Insert", command=insert_data)
insert_button.grid(row=1, column=2)
update_button = tk.Button(root, text="Update", command=update_data)
update_button.grid(row=2, column=2)
delete_button = tk.Button(root, text="Delete", command=delete_data)
delete_button.grid(row=3, column=2)
search_button = tk.Button(root, text="Search", command=search_data)
search_button.grid(row=4, column=2)

# Create and configure the treeview
tree = ttk.Treeview(root, columns=("ID", "Student ID", "First Name", "Last Name", "Address", "Phone"), show="headings")
tree.grid(row=7, column=0, columnspan=3)
tree.heading("ID", text="ID")
tree.heading("Student ID", text="Student ID")
tree.heading("First Name", text="First Name")
tree.heading("Last Name", text="Last Name")
tree.heading("Address", text="Address")
tree.heading("Phone", text="Phone")
tree.column("ID", width=30)
tree.column("Student ID", width=100)
tree.column("First Name", width=100)
tree.column("Last Name", width=100)
tree.column("Address", width=100)
tree.column("Phone", width=100)
refresh_table()

# Start the main loop
root.mainloop()
