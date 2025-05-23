from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
from hashlib import sha256
import os

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Login | Student Management System")
        self.root.geometry("1350x700+0+0")
        self.root.resizable(False, False)

        # ========== Background Image ==========
        bg_path = "images/full_background.png"
        if os.path.exists(bg_path):
            self.bg_img = Image.open(bg_path)
            self.bg_img = self.bg_img.resize((1350, 700), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(self.bg_img)
            self.lb1_bg = Label(self.root, image=self.bg_img)
            self.lb1_bg.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.root.configure(bg="#2b2b2b")

        # ========== Login Variables ==========
        self.var_email = StringVar()
        self.var_password = StringVar()

        # ========== Login Frame ==========
        frame = Frame(self.root, bg="#ffffff", bd=2, relief=RIDGE)
        frame.place(x=475, y=150, width=400, height=350)

        title = Label(frame, text="LOGIN", font=("Segoe UI", 22, "bold"), fg="#222", bg="#ffffff")
        title.pack(pady=20)

        lbl_email = Label(frame, text="Email", font=("Segoe UI", 12), bg="#ffffff", anchor=W)
        lbl_email.place(x=30, y=80, width=340)
        txt_email = Entry(frame, textvariable=self.var_email, font=("Segoe UI", 12), bg="#f0f0f0", relief=FLAT)
        txt_email.place(x=30, y=110, width=340, height=30)

        lbl_pass = Label(frame, text="Password", font=("Segoe UI", 12), bg="#ffffff", anchor=W)
        lbl_pass.place(x=30, y=150, width=340)
        txt_pass = Entry(frame, textvariable=self.var_password, font=("Segoe UI", 12), show="*", bg="#f0f0f0", relief=FLAT)
        txt_pass.place(x=30, y=180, width=340, height=30)

        btn_login = Button(frame, text="Login", font=("Segoe UI", 12, "bold"), bg="#4caf50", fg="white", cursor="hand2", command=self.login)
        btn_login.place(x=30, y=230, width=150, height=35)

        btn_register = Button(frame, text="Register", font=("Segoe UI", 10, "underline"), bg="#ffffff", fg="#1e88e5", bd=0, cursor="hand2", command=self.register_window)
        btn_register.place(x=30, y=280)

        btn_forgot = Button(frame, text="Forgot Password?", font=("Segoe UI", 10, "underline"), bg="#ffffff", fg="#1e88e5", bd=0, cursor="hand2", command=self.forgot_password_window)
        btn_forgot.place(x=200, y=280)

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