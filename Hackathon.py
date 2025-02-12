import mysql.connector
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Database Connection Function
def get_db_connection():
    return mysql.connector.connect(host="localhost", user="root", password="1234", database="hospital")

# Signup Function
def signup():
    user_id = a.get()
    name = b.get()
    password = c.get()

    if not user_id.isdigit():
        messagebox.showerror("Error", "User ID must be numeric.")
        return
    if not name.replace(" ", "").isalpha():
        messagebox.showerror("Error", "Name must contain only letters and spaces.")
        return
    if len(password) < 5:
        messagebox.showerror("Error", "Password must be at least 5 characters long.")
        return

    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO login (id, name, password) VALUES (%s, %s, %s)", (user_id, name, password))
            conn.commit()
        messagebox.showinfo("Success", "Account created successfully!")
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))

# Login Function
def login():
    user_id = d.get()
    password = e.get()

    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM login WHERE id = %s AND password = %s", (user_id, password))
            result = cur.fetchone()
        
        if result:
            messagebox.showinfo("Success", "Login successful!")
            root_1.after(500, lambda: root_1.destroy())  # Close login window
        else:
            messagebox.showerror("Error", "Invalid login credentials.")
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))

# Function to Display Patient Data
def display_patient():
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM patient")
            records = cur.fetchall()
        
        for record in records:
            print(f"Adhar ID: {record[2]}, Name: {record[3]}, Age: {record[4]}, Sex: {record[5]}")
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))

# GUI Window Setup
root_1 = tk.Tk()
root_1.title("Hospital Management System")
root_1.geometry("600x400")

# Login Frame
frame_log = tk.Frame(root_1)
frame_log.pack(pady=20)

tk.Label(frame_log, text="User ID:").grid(row=0, column=0, padx=10, pady=5)
d = tk.Entry(frame_log)
d.grid(row=0, column=1)

tk.Label(frame_log, text="Password:").grid(row=1, column=0, padx=10, pady=5)
e = tk.Entry(frame_log, show="*")
e.grid(row=1, column=1)

tk.Button(frame_log, text="Login", command=login).grid(row=2, column=0, columnspan=2, pady=10)

# Signup Frame
frame_signup = tk.Frame(root_1)
frame_signup.pack(pady=20)

tk.Label(frame_signup, text="New User ID:").grid(row=0, column=0, padx=10, pady=5)
a = tk.Entry(frame_signup)
a.grid(row=0, column=1)

tk.Label(frame_signup, text="Name:").grid(row=1, column=0, padx=10, pady=5)
b = tk.Entry(frame_signup)
b.grid(row=1, column=1)

tk.Label(frame_signup, text="Password:").grid(row=2, column=0, padx=10, pady=5)
c = tk.Entry(frame_signup, show="*")
c.grid(row=2, column=1)

tk.Button(frame_signup, text="Signup", command=signup).grid(row=3, column=0, columnspan=2, pady=10)

# Run the GUI
root_1.mainloop()

