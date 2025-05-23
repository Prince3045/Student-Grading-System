from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Course Details")
        self.root.geometry("1100x500+100+100")
        self.root.configure(bg="white")

        # Variables
        self.var_course_id = StringVar()
        self.var_name = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()
        self.var_search = StringVar()

        # Title
        title = Label(self.root, text="Manage Course Details", font=("Segoe UI", 20, "bold"), bg="#3498db", fg="white")
        title.pack(side=TOP, fill=X)

        # Left Frame
        left_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        left_frame.place(x=10, y=60, width=500, height=400)

        Label(left_frame, text="Course Name", font=("Segoe UI", 12), bg="white").place(x=30, y=30)
        Entry(left_frame, textvariable=self.var_name, font=("Segoe UI", 12), bg="#f0f0f0", fg="black").place(x=150, y=30, width=300)

        Label(left_frame, text="Duration", font=("Segoe UI", 12), bg="white").place(x=30, y=80)
        Entry(left_frame, textvariable=self.var_duration, font=("Segoe UI", 12), bg="#f0f0f0", fg="black").place(x=150, y=80, width=300)

        Label(left_frame, text="Charges", font=("Segoe UI", 12), bg="white").place(x=30, y=130)
        Entry(left_frame, textvariable=self.var_charges, font=("Segoe UI", 12), bg="#f0f0f0", fg="black").place(x=150, y=130, width=300)

        Label(left_frame, text="Description", font=("Segoe UI", 12), bg="white").place(x=30, y=180)
        self.txt_description = Text(left_frame, font=("Segoe UI", 12), bg="#f0f0f0", fg="black")
        self.txt_description.place(x=150, y=180, width=300, height=80)

        Button(left_frame, text="Save", command=self.add, font=("Segoe UI", 11), bg="#3498db", fg="white").place(x=30, y=280, width=100)
        Button(left_frame, text="Update", command=self.update, font=("Segoe UI", 11), bg="#27ae60", fg="white").place(x=140, y=280, width=100)
        Button(left_frame, text="Delete", command=self.delete, font=("Segoe UI", 11), bg="#e74c3c", fg="white").place(x=250, y=280, width=100)
        Button(left_frame, text="Clear", command=self.clear, font=("Segoe UI", 11), bg="#7f8c8d", fg="white").place(x=360, y=280, width=100)

        # Right Frame
        right_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        right_frame.place(x=520, y=60, width=570, height=400)

        Label(right_frame, text="Course Name", font=("Segoe UI", 12), bg="white").place(x=10, y=10)
        Entry(right_frame, textvariable=self.var_search, font=("Segoe UI", 12), bg="#f0f0f0", fg="black").place(x=130, y=10, width=250)
        Button(right_frame, text="Search", command=self.search, font=("Segoe UI", 11), bg="#17a2b8", fg="white").place(x=400, y=9, width=100)

        # Treeview with matching columns to DB
        self.course_table = ttk.Treeview(right_frame, columns=("cid", "name", "duration", "charges", "description"), show='headings')
        self.course_table.heading("cid", text="Course ID")
        self.course_table.heading("name", text="Course Name")
        self.course_table.heading("duration", text="Duration")
        self.course_table.heading("charges", text="Charges")
        self.course_table.heading("description", text="Description")

        self.course_table.column("cid", width=70)
        self.course_table.column("name", width=150)
        self.course_table.column("duration", width=100)
        self.course_table.column("charges", width=100)
        self.course_table.column("description", width=150)

        self.course_table.place(x=0, y=50, width=560, height=320)
        self.course_table.bind("<ButtonRelease-1>", self.get_data)

        self.fetch()

    def add(self):
        if self.var_name.get() == "":
            messagebox.showerror("Error", "Course name is required", parent=self.root)
            return
        try:
            con = sqlite3.connect("student_results.db")
            cur = con.cursor()
            cur.execute("INSERT INTO course (name, duration, charges, description) VALUES (?, ?, ?, ?)",
                        (
                            self.var_name.get(),
                            self.var_duration.get(),
                            self.var_charges.get(),
                            self.txt_description.get("1.0", END)
                        ))
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Course added successfully", parent=self.root)
            self.fetch()
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def fetch(self):
        con = sqlite3.connect("student_results.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM course ORDER BY cid ASC")
        rows = cur.fetchall()
        self.course_table.delete(*self.course_table.get_children())
        for row in rows:
            self.course_table.insert('', END, values=row)
        con.close()

    def get_data(self, ev):
        selected = self.course_table.focus()
        data = self.course_table.item(selected)
        row = data['values']
        if row:
            self.var_course_id.set(row[0])
            self.var_name.set(row[1])
            self.var_duration.set(row[2])
            self.var_charges.set(row[3])
            self.txt_description.delete("1.0", END)
            self.txt_description.insert(END, row[4])

    def update(self):
        if self.var_course_id.get() == "":
            messagebox.showerror("Error", "Select a course to update", parent=self.root)
            return
        try:
            con = sqlite3.connect("student_results.db")
            cur = con.cursor()
            cur.execute("UPDATE course SET name=?, duration=?, charges=?, description=? WHERE cid=?",
                        (
                            self.var_name.get(),
                            self.var_duration.get(),
                            self.var_charges.get(),
                            self.txt_description.get("1.0", END),
                            self.var_course_id.get()
                        ))
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Course updated successfully", parent=self.root)
            self.fetch()
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete(self):
        if self.var_course_id.get() == "":
            messagebox.showerror("Error", "Select a course to delete", parent=self.root)
            return
        try:
            con = sqlite3.connect("student_results.db")
            cur = con.cursor()
            cur.execute("DELETE FROM course WHERE cid=?", (self.var_course_id.get(),))
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Course deleted successfully", parent=self.root)
            self.fetch()
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_course_id.set("")
        self.var_name.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete("1.0", END)

    def search(self):
        con = sqlite3.connect("student_results.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM course WHERE name LIKE ? ORDER BY cid ASC", ('%' + self.var_search.get() + '%',))
        rows = cur.fetchall()
        self.course_table.delete(*self.course_table.get_children())
        for row in rows:
            self.course_table.insert('', END, values=row)
        con.close()
