import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import sqlite3
from course import CourseClass
from student import studentClass
from result import resultClass
from report import reportClass
from logout import LoginSystem
import os

class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard | Student Management")
        self.root.state('zoomed')  # Maximize window

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        bg_path = "images/full_background.png"
        if os.path.exists(bg_path):
            self.full_bg_img = Image.open(bg_path).resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            self.full_bg_img = ImageTk.PhotoImage(self.full_bg_img)
            bg_label = ttk.Label(self.root, image=self.full_bg_img)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.root.configure(bg='#2b2b2b')

        self.logo = ImageTk.PhotoImage(file="images/logo_p.png")

        # Top Banner
        banner = ttk.Frame(self.root, bootstyle="primary")
        banner.place(x=0, y=0, relwidth=1, height=80)

        ttk.Label(
            banner,
            text="  Student Result Management System",
            image=self.logo,
            compound=LEFT,
            font=("Segoe UI", 24, "bold"),
            bootstyle="inverse-primary"
        ).place(x=20, y=15)

        # Top Menu Buttons
        menu_bar = ttk.Frame(self.root, bootstyle="light")
        menu_bar.place(x=0, y=80, relwidth=1, height=60)

        menu_buttons = [
            ("Course", self.add_course),
            ("Student", self.add_student),
            ("Result", self.add_result),
            ("View Student Result", self.add_report),
            ("Logout", self.logout),
            ("Exit", self.root.quit)
        ]

        x_offset = 20
        for text, cmd in menu_buttons:
            ttk.Button(
                menu_bar,
                text=text,
                command=cmd,
                bootstyle="primary-outline",
            ).place(x=x_offset, y=10, width=180, height=40)
            x_offset += 190

        # Dashboard Cards
        self.card_course = ttk.Label(
            self.root,
            text="Courses\n[ 0 ]",
            font=("Segoe UI", 18, "bold"),
            bootstyle="danger",
            borderwidth=2,
            relief="ridge",
            anchor=CENTER,
            padding=10,
            background="white"
        )
        self.card_course.place(x=120, y=220, width=300, height=150)

        self.card_student = ttk.Label(
            self.root,
            text="Students\n[ 0 ]",
            font=("Segoe UI", 18, "bold"),
            bootstyle="success",
            borderwidth=2,
            relief="ridge",
            anchor=CENTER,
            padding=10,
            background="white"
        )
        self.card_student.place(x=480, y=220, width=300, height=150)

        self.card_result = ttk.Label(
            self.root,
            text="Results\n[ 0 ]",
            font=("Segoe UI", 18, "bold"),
            bootstyle="info",
            borderwidth=2,
            relief="ridge",
            anchor=CENTER,
            padding=10,
            background="white"
        )
        self.card_result.place(x=840, y=220, width=300, height=150)

        # Footer
        footer = ttk.Label(
            self.root,
            text="SRMS | Student Result Management System | Contact: admin@example.com",
            font=("Segoe UI", 11),
            bootstyle="dark",
            anchor=CENTER,
            padding=5
        )
        footer.pack(side=BOTTOM, fill=X)

        self.update_details()

    def update_details(self):
        con = sqlite3.connect("student_results.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM course")
            course = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM student")
            student = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM result")
            result = cur.fetchone()[0]

            self.card_course.config(text=f"Courses\n[ {course} ]")
            self.card_student.config(text=f"Students\n[ {student} ]")
            self.card_result.config(text=f"Results\n[ {result} ]")
        except Exception as ex:
            print(f"Error updating details: {ex}")
        finally:
            con.close()

    def add_course(self):
        self.new_win = ttk.Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win)

    def add_student(self):
        self.new_win = ttk.Toplevel(self.root)
        self.new_obj = studentClass(self.new_win)

    def add_result(self):
        self.new_win = ttk.Toplevel(self.root)
        self.new_obj = resultClass(self.new_win)

    def add_report(self):
        self.new_win = ttk.Toplevel(self.root)
        self.new_obj = reportClass(self.new_win)

    def logout(self):
        self.new_win = ttk.Toplevel(self.root)
        self.new_obj = LoginSystem(self.new_win)

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    obj = RMS(root)
    root.mainloop()