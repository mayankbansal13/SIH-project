from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
import mysql.connector
from tkinter import ttk
import time
import threading


root_1=Tk()
root_1.title("Hospital Management")
root_1.attributes("-fullscreen",True)
root_1.configure(bg='aqua')
L1=Label(root_1,text=" == HOSPITAL MANAGEMENT == ",bg="black",fg='white',font=("Broadway",22),pady=20).place(x=1025,y=22)
        ####################################################################################################################
def update_image(alpha):
    blended_image = Image.blend(white, black, alpha)
    photo = ImageTk.PhotoImage(blended_image)
    image_label.config(image=photo)
    image_label.image = photo

def resize_image(image, size):
    return image.resize(size, Image.LANCZOS)

def run_image_update():
    alpha = 0.0
    while alpha <= 1.0:
        update_image(alpha)
        alpha += 0.01
        root_1.update_idletasks()
        time.sleep(0.1)

white = Image.open("Image-1.webp")
black = Image.open("image2.jpg")

target_size = (1010, 955)

white = resize_image(white, target_size)
black = resize_image(black, target_size)

if white.size != black.size:
    black = black.resize(white.size, Image.LANCZOS)
    
if white.mode != black.mode:
    black = black.convert(white.mode)

initial_image = Image.blend(white, black, 0)
photo = ImageTk.PhotoImage(initial_image)
image_label = Label(root_1, image=photo)
image_label.place(x=0,y=0)

image_update_thread = threading.Thread(target=run_image_update, daemon=True)
image_update_thread.start()

        #######################################################################################################

def open_login_window():
    global frame_log
    global username
    global password
    global u
    global p

    frame_log=LabelFrame(root_1,pady=5,bg="#c0c0c0",borderwidth=8, relief=RIDGE)
    frame_log.place(x=1014,y=0,height=960,width=523)

    l2=Label(frame_log, text="     LOGIN     ",bg='black',fg="#ffffff",font=("ALGERIAN",48),padx=20).place(x=63,y=10)
    Label(frame_log, text="Username", bg='#c0c0c0', font=("ALGERIAN",20)).place(x=15,y=250)
    username = Entry(frame_log,width=26,borderwidth=3,bg="white",font=("Georgia",14))
    username.place(x=180,y=250)

    Label(frame_log, text="Password",  bg='#c0c0c0', font=("ALGERIAN",20)).place(x=15,y=350)
    password = Entry(frame_log, show="*",width=26,borderwidth=3,bg="white",font=("Georgia",14))
    password.place(x=180,y=350)

    Button(frame_log, text="Login", bg='black',fg='white',font=('georgia', 14, 'bold'),width=10,height=2,bd=2,padx=10,pady=5,command=login).place(x=60,y=650)
    Button(frame_log, text="Return", bg='black',fg='white',font=('georgia', 14, 'bold'),width=10,height=2,bd=2,padx=10,pady=5,command=return_frame).place(x=300,y=650)

    
def login():
    global frame_log2
    global frame_log1
    u=username.get()
    p=password.get()
    
    if not u or not p:
        messagebox.showwarning("Input Error", "Please provide both username and password")
        return

    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='root1', database='hospitalmanagement')
        cr = conn.cursor()

        qr = "SELECT Username, Password FROM patient WHERE Username = %s"
        cr.execute(qr, (u,))
        result = cr.fetchone()

        if result:
            db_username, db_password = result
            if db_password == p:

                frame_log1=LabelFrame(root_1,bg="#c0c0c0",borderwidth=8, relief=RIDGE)
                frame_log1.place(x=1014,y=0,height=960,width=523)
                
                logo=Image.open("img3.jpg")
                resized=logo.resize((505,945), Image.LANCZOS)
                R_logo=ImageTk.PhotoImage(resized)
                lbl=Label(frame_log1, image=R_logo)
                lbl.place(x=2,y=0)

                frame_log2=LabelFrame(root_1,pady=5,bg="#ff9999",borderwidth=8, relief=RIDGE)
                frame_log2.place(x=1,y=0,height=960,width=1023)

                l3=Label(frame_log2, text="     PATIENT DETAILS     ",bg='black',fg="#ffffff",font=("ALGERIAN",48),padx=20).place(x=120,y=10)
                display_patient(u)
                
                messagebox.showinfo("Success", "Logged in successfully").place(x=2000,y=1000)
                
            else:
                messagebox.showwarning("Login Failed", "Incorrect password")
        else:
            messagebox.showwarning("Login Failed", "Username not found")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

    finally:
        if conn.is_connected():
            cr.close()
            conn.close()

def display_patient(u):
    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='root1', database='hospitalmanagement')
        cr = conn.cursor()
        query = "SELECT * FROM patient WHERE Username = %s"
        cr.execute(query, (u,))
        result = cr.fetchone()

        if result:
            _, _, adhar_id, name, age, sex = result

            Label(frame_log2, text=f"Adhar ID: {adhar_id}", bg="#ff9999", font=("Georgia", 24,'bold')).place(x=120, y=150)
            Label(frame_log2, text=f"Name: {name}", bg="#ff9999", font=("Georgia", 24,'bold')).place(x=120, y=250)
            Label(frame_log2, text=f"Age: {age}", bg="#ff9999", font=("Georgia", 24,'bold')).place(x=120, y=350)
            Label(frame_log2, text=f"Sex: {sex}", bg="#ff9999", font=("Georgia", 24,'bold')).place(x=120, y=450)

            Button(frame_log2, text="Medical History", bg='black',fg='white',font=('georgia', 14, 'bold'),width=50,height=2,bd=2,padx=10,pady=2,command=history).place(x=160,y=650)
            Button(frame_log2, text="AI Recommendation", bg='black',fg='white',font=('georgia', 14, 'bold'),width=50,height=2,bd=2,padx=10,pady=3,command=recmm).place(x=160,y=750)
            Button(frame_log2, text="Return", bg='black',fg='white',font=('georgia', 14, 'bold'),width=50,height=2,bd=2,padx=10,pady=2,command=return_2).place(x=160,y=850)
            

        else:
            messagebox.showwarning("Data Error", "No details found for this user.")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

    finally:
        if conn.is_connected():
            cr.close()
            conn.close()

def history():
    pass

def recmm():
    pass

        ###############################################################################################################################

def return_frame():
    frame_log.destroy()
def return_():
       frame_sin.destroy()
def return_1():
       frame_con.destroy()
def return_2():
    frame_log2.destroy()
    frame_log1.destroy()
    frame_log.destroy()


def open_signup_window():
    global frame_sin
    global username
    global password
  
    
    frame_sin=LabelFrame(root_1,pady=5,bg="#c0c0c0",borderwidth=8, relief=RIDGE)
    frame_sin.place(x=1014,y=0,height=960,width=523)

    l2=Label(frame_sin, text="     SIGN UP     ",bg='black',fg="#ffffff",font=("ALGERIAN",48),padx=20).place(x=40,y=10)
    Label(frame_sin, text="Username", bg='#c0c0c0', font=("ALGERIAN",20)).place(x=15,y=250)
    username = Entry(frame_sin,width=26,borderwidth=3,bg="white",font=("Georgia",14))
    username.place(x=180,y=250)

    Label(frame_sin, text="Password",  bg='#c0c0c0', font=("ALGERIAN",20)).place(x=15,y=350)
    password = Entry(frame_sin, show="*",width=26,borderwidth=3,bg="white",font=("Georgia",14))
    password.place(x=180,y=350)

    Button(frame_sin, text="Continue", bg='black',fg='white',font=('georgia', 14, 'bold'),width=10,height=2,bd=2,padx=10,pady=5,command=conti).place(x=60,y=650)
    Button(frame_sin, text="Return", bg='black',fg='white',font=('georgia', 14, 'bold'),width=10,height=2,bd=2,padx=10,pady=5,command=return_).place(x=300,y=650)
    
def conti():
    global sanitized_username
    global adhar
    global name
    global age
    global sex
    global frame_con
    global pas

    user=username.get()
    pas=password.get()

    sanitized_username = user.strip().replace(" ", "_").lower()
    
    if not user or not pas:
        messagebox.showwarning("Input Error", "Please provide both username and password")
        return
    
    else:
        frame_con=LabelFrame(root_1,pady=5,bg="#c0c0c0",borderwidth=8, relief=RIDGE)
        frame_con.place(x=1014,y=0,height=960,width=523)

        l2=Label(frame_con, text="     REGISTER     ",bg='black',fg="#ffffff",font=("ALGERIAN",48),padx=10).place(x=10,y=10)
        Label(frame_con, text="Adhar id", bg='#c0c0c0', font=("ALGERIAN",20)).place(x=15,y=250)
        adhar = Entry(frame_con,width=26,borderwidth=3,bg="white",font=("Georgia",14))
        adhar.place(x=180,y=250)

        Label(frame_con, text="Name",  bg='#c0c0c0', font=("ALGERIAN",20)).place(x=15,y=350)
        name = Entry(frame_con,width=26,borderwidth=3,bg="white",font=("Georgia",14))
        name.place(x=180,y=350)

        Label(frame_con, text="Age",  bg='#c0c0c0', font=("ALGERIAN",20)).place(x=15,y=450)
        age = Entry(frame_con,width=26,borderwidth=3,bg="white",font=("Georgia",14))
        age.place(x=180,y=450)

        Label(frame_con, text="Sex",  bg='#c0c0c0', font=("ALGERIAN",20)).place(x=15,y=550)
        sex = Entry(frame_con,width=26,borderwidth=3,bg="white",font=("Georgia",14))
        sex.place(x=180,y=550)



        Button(frame_con, text="Sign Up", bg='black',fg='white',font=('georgia', 14, 'bold'),width=10,height=2,bd=2,padx=10,pady=5,command=signup).place(x=60,y=650)
        Button(frame_con, text="Return", bg='black',fg='white',font=('georgia', 14, 'bold'),width=10,height=2,bd=2,padx=10,pady=5,command=return_1).place(x=300,y=650)

def signup():
    a = adhar.get()
    b = name.get()
    c = age.get()
    d = sex.get()
    
    if not (a and b and c and d):
        messagebox.showwarning("Input Error", "Please fill in all fields")
        return

    if not (a.isdigit() and b.isalnum() and c.isdigit() and d.isalnum()):
        messagebox.showwarning("Type Error", "Invalid Data Type, Please enter valid data only")
        return
    
    data = (sanitized_username,pas,a, b, c, d)
    
    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='root1', database='hospitalmanagement')
        cr = conn.cursor()

        qr = "INSERT INTO patient (Username,Password,AdharID, Name, Age, Sex) VALUES (%s,%s, %s, %s, %s,%s)"
        cr.execute(qr, data)
        conn.commit()
        messagebox.showinfo("Success", "Registered Successfully")
        frame_con.destroy()
        frame_sin.destroy()
        
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        
    finally:
        if conn.is_connected():
            cr.close()
            conn.close()

            

    #####################################################################################################################################################

def exit_window():
    root_1.destroy()

button_style = {
    'bg': 'black', 
    'fg': 'white',  
    'font': ('georgia', 14, 'bold'),  
    'width': 15,    
    'height': 2,  
    'bd': 2,           
    'padx': 10,     
    'pady': 5   
}


Button(root_1, text="Login", **button_style, command=open_login_window).place(x=1275,y=400, anchor='center')
Button(root_1, text="Sign Up", **button_style, command=open_signup_window).place(x=1275,y=550, anchor='center')
Button(root_1, text="Close", **button_style, command=exit_window).place(x=1275,y=700, anchor='center')

    ###############################################################################################################

root_1.mainloop()
