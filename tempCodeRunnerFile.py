from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
from hashlib import sha256
import os

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("1350x700+0+0")
        self.root.resizable(False, False)

        #========== Background Image ==========
        self.bg_img = Image.open("C:/Users/HP/OneDrive/Desktop/RMS/images/logo_p.png")
        self.bg_img = self.bg_img.resize((1350, 700), Image.Resampling.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)

        # Place background first so it stays behind all other widgets
        self.lb1_bg = Label(self.root, image=self.bg_img)
        self.lb1_bg.place(x=0, y=0, relwidth=1, relheight=1)

        #========== Login Variables ==========
        self.var_email = StringVar()
        self.var_password = StringVar()

        #========== Login Frame ==========
        frame = Frame(self.root, bg="gray", bd=2)
        frame.place(x=500, y=150, width=400, height=300)

        Label(frame, text="Login", font=("Arial", 25, "bold"), bg="gray").pack(pady=20)

        Label(frame, text="Email", font=("Arial", 12, "bold"), bg="gray").place(x=30, y=80)
        Entry(frame, textvariable=self.var_email, font=("Arial", 12), bg="lightyellow").place(x=130, y=80, width=220)

        Label(frame, text="Password", font=("Arial", 12, "bold"), bg="gray").place(x=30, y=130)
        Entry(frame, textvariable=self.var_password, show="*", font=("Arial", 12), bg="lightyellow").place(x=130, y=130, width=220)

        Button(frame, text="Login", font=("Arial", 12, "bold"), bg="#4caf50", fg="white", command=self.login).place(x=130, y=180, width=100)
        Button(frame, text="Register", font=("Arial", 10, "underline", "bold"), bd=0, bg="gray", fg="blue", command=self.register_window).place(x=130, y=220)
        Button(frame, text="Forgot Password?", font=("Arial", 10, "underline", "bold"), bd=0, bg="gray", fg="blue", command=self.forgot_password_window).place(x=200, y=220)

    def login(self):
        con = sqlite3.connect("student_results.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE email=? AND password=?", 
                        (self.var_email.get(), self.hash_password(self.var_password.get())))
            row = cur.fetchone()
            if row is None:
                messagebox.showerror("Error", "Invalid Email or Password", parent=self.root)
            else:
                self.root.destroy()
                from dashboard import RMS
                dash_root = Tk()
                obj = RMS(dash_root)
                dash_root.mainloop()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def register_window(self):
        self.root.destroy()
        from register import Register
        reg_root = Tk()
        obj = Register(reg_root)
        reg_root.mainloop()

    def forgot_password_window(self):
        self.root.destroy()
        from forgot_password import ForgotPassword
        fp_root = Tk()
        obj = ForgotPassword(fp_root)
        fp_root.mainloop()

    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()

if __name__ == "__main__":
    root = Tk()
    obj = LoginSystem(root)
    root.mainloop()