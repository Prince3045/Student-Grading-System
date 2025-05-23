from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import os

class reportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1000x400+80+150")
        self.root.config(bg='white')
        self.root.focus_force()

        self.var_search = StringVar()

        title = Label(self.root, text="View Student Results", font=("goudy old style", 20, "bold"),
                      bg='orange', fg='#262626')
        title.place(x=10, y=15, width=980, height=50)

        Label(self.root, text="Search by Roll No.", font=("goudy old style", 20, 'bold'), bg='white').place(x=100, y=100)
        Entry(self.root, textvariable=self.var_search, font=("goudy old style", 20), bg='lightyellow').place(x=370, y=100, width=150)
        Button(self.root, text='Search', font=("goudy old style", 15, "bold"),
               bg="#03a9f4", fg="white", cursor="hand2", command=self.search).place(x=530, y=100, width=100, height=35)
        Button(self.root, text='Clear', font=("goudy old style", 15, "bold"),
               bg="gray", fg="white", cursor="hand2", command=self.clear).place(x=650, y=100, width=100, height=35)

        labels = ["Roll No", "Name", "Course", "Total Marks\nObtained", "Total Marks", "Percentage"]
        positions = [50, 180, 310, 440, 620, 760]
        for i, text in enumerate(labels):
            Label(self.root, text=text, font=("goudy old style", 15, 'bold'),
                  bg='white', bd=2, relief=GROOVE).place(x=positions[i], y=170, width=120 if i != 3 else 160, height=50)

        self.roll = Label(self.root, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE)
        self.roll.place(x=50, y=220, width=120, height=50)
        self.name = Label(self.root, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE)
        self.name.place(x=180, y=220, width=120, height=50)
        self.course = Label(self.root, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE)
        self.course.place(x=310, y=220, width=120, height=50)
        self.total_obtained = Label(self.root, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE)
        self.total_obtained.place(x=440, y=220, width=160, height=50)
        self.total_marks = Label(self.root, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE)
        self.total_marks.place(x=620, y=220, width=120, height=50)
        self.percentage = Label(self.root, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE)
        self.percentage.place(x=760, y=220, width=120, height=50)

        Button(self.root, text='Delete', font=("goudy old style", 15, "bold"),
               bg="red", fg="white", cursor="hand2", command=self.delete).place(x=350, y=300, width=150, height=35)
        Button(self.root, text='Download PDF', font=("goudy old style", 15, "bold"),
               bg="green", fg="white", cursor="hand2", command=self.export_pdf).place(x=520, y=300, width=180, height=35)

    def search(self):
        con = sqlite3.connect(database="student_results.db")
        cur = con.cursor()
        try:
            roll = self.var_search.get()
            if roll == "":
                messagebox.showerror("Error", "Roll No. should be required", parent=self.root)
                return

            cur.execute("SELECT name, course FROM student WHERE roll=?", (roll,))
            student = cur.fetchone()

            if not student:
                messagebox.showerror("Error", "No student found", parent=self.root)
                return

            self.roll.config(text=roll)
            self.name.config(text=student[0])
            self.course.config(text=student[1])

            cur.execute("SELECT marks_ob, full_marks FROM result WHERE roll=?", (roll,))
            self.results = cur.fetchall()

            if not self.results:
                messagebox.showinfo("Info", "No results found for this student.", parent=self.root)
                self.total_obtained.config(text="0")
                self.total_marks.config(text="0")
                self.percentage.config(text="0.00%")
                return

            total_obt = sum(float(row[0]) for row in self.results)
            total_full = sum(float(row[1]) for row in self.results)
            percentage = (total_obt / total_full) * 100 if total_full else 0

            self.total_obtained.config(text=f"{total_obt:.2f}")
            self.total_marks.config(text=f"{total_full:.2f}")
            self.percentage.config(text=f"{percentage:.2f}%")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def clear(self):
        self.roll.config(text="")
        self.name.config(text="")
        self.course.config(text="")
        self.total_obtained.config(text="")
        self.total_marks.config(text="")
        self.percentage.config(text="")
        self.var_search.set("")
        if hasattr(self, 'results'):
            self.results = []

    def delete(self):
        roll = self.var_search.get()
        if roll == "":
            messagebox.showerror("Error", "Search student result first", parent=self.root)
            return

        con = sqlite3.connect(database="student_results.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM result WHERE roll=?", (roll,))
            row = cur.fetchone()
            if row is None:
                messagebox.showerror("Error", "No result found to delete", parent=self.root)
            else:
                op = messagebox.askyesno("Confirm", "Do you really want to delete all results for this student?", parent=self.root)
                if op:
                    cur.execute("DELETE FROM result WHERE roll=?", (roll,))
                    con.commit()
                    messagebox.showinfo("Delete", "Result deleted successfully", parent=self.root)
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def export_pdf(self):
        if not hasattr(self, 'results') or not self.results:
            messagebox.showerror("Error", "No result data to export", parent=self.root)
            return

        file_name = f"Result_{self.roll.cget('text')}.pdf"
        c = canvas.Canvas(file_name, pagesize=A4)
        width, height = A4
        y = height - inch

        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, y, "Student Result Report")
        y -= 40

        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Roll No: {self.roll.cget('text')}")
        c.drawString(250, y, f"Name: {self.name.cget('text')}")
        c.drawString(450, y, f"Course: {self.course.cget('text')}")
        y -= 30

        y -= 10
        c.line(50, y, 550, y)
        y -= 30
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Total Obtained: {self.total_obtained.cget('text')}")
        c.drawString(250, y, f"Total Marks: {self.total_marks.cget('text')}")
        c.drawString(450, y, f"Percentage: {self.percentage.cget('text')}")

        c.save()
        messagebox.showinfo("Success", f"PDF saved as {file_name}", parent=self.root)
        os.startfile(file_name)

if __name__ == "__main__":
    root = Tk()
    obj = reportClass(root)
    root.mainloop()