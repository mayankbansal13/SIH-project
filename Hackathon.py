import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Database Connection
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

# Create users table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        password TEXT NOT NULL
    )
""")
conn.commit()


# Function to handle signup
def signup():
    user_id = entry_new_user_id.get()
    name = entry_name.get()
    password = entry_new_password.get()

    if not user_id or not name or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        cursor.execute("INSERT INTO users (user_id, name, password) VALUES (?, ?, ?)", (user_id, name, password))
        conn.commit()
        messagebox.showinfo("Success", "Signup Successful!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "User ID already exists!")


# Function to handle login
def login():
    user_id = entry_user_id.get()
    password = entry_password.get()

    cursor.execute("SELECT * FROM users WHERE user_id = ? AND password = ?", (user_id, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Login Success", f"Welcome, {user[2]}!")  # Display name
        root.withdraw()  # Hide the login window
        open_dashboard(user[2])  # Open dashboard with username
    else:
        messagebox.showerror("Error", "Invalid Credentials!")


# Function to open Dashboard after login
def open_dashboard(username):
    dashboard = tk.Toplevel(root)  # Create a new window
    dashboard.title("Dashboard")
    dashboard.geometry("400x300")
    dashboard.configure(bg="#f0f0f0")

    tk.Label(dashboard, text=f"Welcome, {username}!", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=20)

    tk.Button(dashboard, text="Logout", command=lambda: logout(dashboard)).pack(pady=20)


# Function to logout and go back to login screen
def logout(dashboard):
    dashboard.destroy()  # Close dashboard
    root.deiconify()  # Show the login window again


# GUI Setup
root = tk.Tk()
root.title("Hospital Management System")
root.geometry("500x450")
root.configure(bg="#f0f0f0")  # Light grey background

# Header Label
tk.Label(root, text="🏥 Hospital Management System", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

# Login Frame
frame_login = ttk.LabelFrame(root, text="Login", padding=15)
frame_login.pack(pady=10, padx=20, fill="x")

ttk.Label(frame_login, text="User ID:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_user_id = ttk.Entry(frame_login)
entry_user_id.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(frame_login, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_password = ttk.Entry(frame_login, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=5)

ttk.Button(frame_login, text="Login", command=login).grid(row=2, columnspan=2, pady=10)

# Signup Frame
frame_signup = ttk.LabelFrame(root, text="Signup", padding=15)
frame_signup.pack(pady=10, padx=20, fill="x")

ttk.Label(frame_signup, text="New User ID:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_new_user_id = ttk.Entry(frame_signup)
entry_new_user_id.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(frame_signup, text="Name:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_name = ttk.Entry(frame_signup)
entry_name.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(frame_signup, text="Password:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_new_password = ttk.Entry(frame_signup, show="*")
entry_new_password.grid(row=2, column=1, padx=10, pady=5)

ttk.Button(frame_signup, text="Signup", command=signup).grid(row=3, columnspan=2, pady=10)

# Run the GUI
root.mainloop()

# Close DB connection when GUI is closed
conn.close()
