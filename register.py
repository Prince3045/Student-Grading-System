from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
from hashlib import sha256
import os

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Register | Student Management System")
        self.root.geometry("1350x700+0+0")
        self.root.resizable(False, False)

        # ========== Background Image ==========
        bg_path = "images/register_background.png"
        if os.path.exists(bg_path):
            self.bg_img = Image.open(bg_path)
            self.bg_img = self.bg_img.resize((1350, 700), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(self.bg_img)
            self.lb1_bg = Label(self.root, image=self.bg_img)
            self.lb1_bg.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.root.configure(bg="#2b2b2b")

        self.var_email = StringVar()
        self.var_password = StringVar()

        # ========== Register Frame ==========
        frame = Frame(self.root, bg="#ffffff", bd=2, relief=RIDGE)
        frame.place(x=475, y=150, width=400, height=320)

        Label(frame, text="REGISTER", font=("Segoe UI", 22, "bold"), fg="#222", bg="#ffffff").pack(pady=20)

        Label(frame, text="Email", font=("Segoe UI", 12), bg="#ffffff", anchor=W).place(x=30, y=80, width=340)
        Entry(frame, textvariable=self.var_email, font=("Segoe UI", 12), bg="#f0f0f0", relief=FLAT).place(x=30, y=110, width=340, height=30)

        Label(frame, text="Password", font=("Segoe UI", 12), bg="#ffffff", anchor=W).place(x=30, y=150, width=340)
        Entry(frame, textvariable=self.var_password, show="*", font=("Segoe UI", 12), bg="#f0f0f0", relief=FLAT).place(x=30, y=180, width=340, height=30)

        Button(frame, text="Register", font=("Segoe UI", 12, "bold"), bg="#4caf50", fg="white", cursor="hand2", command=self.register).place(x=30, y=230, width=150, height=35)

        Button(frame, text="Back to Login", font=("Segoe UI", 10, "underline"), bg="#ffffff", fg="#1e88e5", bd=0, cursor="hand2", command=self.back_to_login).place(x=200, y=235)

    def register(self):
        con = sqlite3.connect("student_results.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE email=?", (self.var_email.get(),))
            if cur.fetchone():
                messagebox.showerror("Error", "User already exists")
            else:
                cur.execute("INSERT INTO users(email,password) VALUES (?,?)", (self.var_email.get(), self.hash_password(self.var_password.get())))
                con.commit()
                messagebox.showinfo("Success", "Registered Successfully")
                self.back_to_login()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def back_to_login(self):
        self.root.destroy()
        from login import LoginSystem
        login_root = Tk()
        obj = LoginSystem(login_root)
        login_root.mainloop()

    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()

if __name__ == "__main__":
    root = Tk()
    obj = Register(root)
    root.mainloop()
