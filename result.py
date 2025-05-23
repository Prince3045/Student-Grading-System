from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class resultClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x700+80+50")
        self.root.config(bg='white')
        self.root.focus_force()

        # ==== Title ====
        title = Label(self.root, text="Add Student Results",
                      font=("goudy old style", 25, "bold"),
                      bg='orange', fg='#262626')
        title.place(x=10, y=10, width=1180, height=50)

        # ==== Variables ====
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_subject = StringVar()
        self.var_marks = StringVar()
        self.var_full_marks = StringVar()
        self.roll_list = []
        self.fetch_roll()

        # ==== Widgets ====
        y_start = 80
        y_gap = 60
        x_lbl = 50
        x_entry = 260
        width_entry = 280

        Label(self.root, text="Select Student", font=("goudy old style", 18), bg='white').place(x=x_lbl, y=y_start)
        Label(self.root, text="Name", font=("goudy old style", 18), bg='white').place(x=x_lbl, y=y_start + y_gap)
        Label(self.root, text="Course", font=("goudy old style", 18), bg='white').place(x=x_lbl, y=y_start + 2 * y_gap)
        Label(self.root, text="Subject", font=("goudy old style", 18), bg='white').place(x=x_lbl, y=y_start + 3 * y_gap)
        Label(self.root, text="Marks Obtained", font=("goudy old style", 18), bg='white').place(x=x_lbl, y=y_start + 4 * y_gap)
        Label(self.root, text="Full Marks", font=("goudy old style", 18), bg='white').place(x=x_lbl, y=y_start + 5 * y_gap)

        self.txt_student = ttk.Combobox(self.root, textvariable=self.var_roll, values=self.roll_list,
                                        font=("goudy old style", 15))
        self.txt_student.place(x=x_entry, y=y_start, width=200)
        self.txt_student.set("Select")

        Button(self.root, text='Search', font=("goudy old style", 14, "bold"), bg="#03a9f4", fg="white",
               cursor="hand2", command=self.search).place(x=480, y=y_start, width=100, height=30)

        Entry(self.root, textvariable=self.var_name, font=("goudy old style", 18),
              bg='lightyellow', state='readonly').place(x=x_entry, y=y_start + y_gap, width=width_entry)
        Entry(self.root, textvariable=self.var_course, font=("goudy old style", 18),
              bg='lightyellow', state='readonly').place(x=x_entry, y=y_start + 2 * y_gap, width=width_entry)
        Entry(self.root, textvariable=self.var_subject, font=("goudy old style", 18),
              bg='lightyellow').place(x=x_entry, y=y_start + 3 * y_gap, width=width_entry)
        Entry(self.root, textvariable=self.var_marks, font=("goudy old style", 18),
              bg='lightyellow').place(x=x_entry, y=y_start + 4 * y_gap, width=width_entry)
        Entry(self.root, textvariable=self.var_full_marks, font=("goudy old style", 18),
              bg='lightyellow').place(x=x_entry, y=y_start + 5 * y_gap, width=width_entry)

        # ==== Buttons ====
        btn_y = y_start + 6 * y_gap
        self.delete_button = Button(self.root, text='Delete Selected', font=("goudy old style", 14), bg="tomato", fg="black",
               cursor="hand2", command=self.delete_selected, state=DISABLED)
        self.delete_button.place(x=530, y=btn_y, width=150, height=35)

        Button(self.root, text='Submit', font=("goudy old style", 14), bg="lightgreen",
               cursor="hand2", command=self.add).place(x=200, y=btn_y, width=100, height=35)
        Button(self.root, text='Clear', font=("goudy old style", 14), bg="lightgray",
               cursor="hand2", command=self.clear).place(x=310, y=btn_y, width=100, height=35)
        Button(self.root, text='Clear All', font=("goudy old style", 14), bg="red", fg="white",
               cursor="hand2", command=self.clear_all).place(x=420, y=btn_y, width=100, height=35)

        # ==== Image ====
        self.bg_img = Image.open("images/result.jpg")
        self.bg_img = self.bg_img.resize((450, 300), Image.Resampling.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        Label(self.root, image=self.bg_img).place(x=680, y=80)

        # ==== Table ====
        self.result_frame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        self.result_frame.place(x=680, y=400, width=480, height=250)

        self.result_table = ttk.Treeview(self.result_frame, columns=("subject", "marks", "full"), show="headings")
        self.result_table.heading("subject", text="Subject")
        self.result_table.heading("marks", text="Marks")
        self.result_table.heading("full", text="Full Marks")
        self.result_table.column("subject", width=150)
        self.result_table.column("marks", width=80)
        self.result_table.column("full", width=80)
        self.result_table.pack(fill=BOTH, expand=1)

        # Label to display total marks and percentage
        self.total_marks_label = Label(self.root, text="Total Marks: 0 / 0  (0.00%)", font=("goudy old style", 18), bg='white')
        self.total_marks_label.place(x=680, y=670)

        # Bind select row event to enable/disable delete button
        self.result_table.bind("<<TreeviewSelect>>", self.on_select_row)

    # ==== Functions ====

    def fetch_roll(self):
        con = sqlite3.connect(database="student_results.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT roll FROM student")
            rows = cur.fetchall()
            self.roll_list.clear()
            self.roll_list.extend([row[0] for row in rows])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def search(self):
        con = sqlite3.connect(database="student_results.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name, course FROM student WHERE roll=?", (self.var_roll.get(),))
            row = cur.fetchone()
            if row:
                self.var_name.set(row[0])
                self.var_course.set(row[1])
                self.load_existing_results()
            else:
                messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def add(self):
        con = sqlite3.connect(database="student_results.db")
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Please search for a student first.", parent=self.root)
                return
            if self.var_subject.get() == "":
                messagebox.showerror("Error", "Please enter the subject.", parent=self.root)
                return
            if self.var_marks.get() == "" or self.var_full_marks.get() == "":
                messagebox.showerror("Error", "Please enter marks and full marks.", parent=self.root)
                return

            subject = self.var_subject.get()

            cur.execute("SELECT * FROM result WHERE roll=? AND course=? AND subject=?",
                        (self.var_roll.get(), self.var_course.get(), subject))
            row = cur.fetchone()
            if row:
                messagebox.showerror("Error", f"Result for {subject} already exists.", parent=self.root)
            else:
                cur.execute("INSERT INTO result (roll, name, course, subject, marks_ob, full_marks) VALUES (?, ?, ?, ?, ?, ?)",
                            (
                                self.var_roll.get(),
                                self.var_name.get(),
                                self.var_course.get(),
                                subject,
                                self.var_marks.get(),
                                self.var_full_marks.get()
                            ))
                con.commit()
                messagebox.showinfo("Success", "Result Added Successfully", parent=self.root)
                self.result_table.insert('', END, values=(
                    subject,
                    self.var_marks.get(),
                    self.var_full_marks.get()
                ))
                self.clear()
                self.load_existing_results()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def clear(self):
        self.var_subject.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")

    def clear_all(self):
        self.var_roll.set("Select")
        self.var_name.set("")
        self.var_course.set("")
        self.clear()
        self.result_table.delete(*self.result_table.get_children())
        self.total_marks_label.config(text="Total Marks: 0 / 0  (0.00%)")

    def load_existing_results(self):
        self.result_table.delete(*self.result_table.get_children())  # Clear old results
        
        con = sqlite3.connect("student_results.db")
        cur = con.cursor()

        total_obtained = 0
        total_full = 0
        
        try:
            # Get results only for the selected student and course
            cur.execute("SELECT subject, marks_ob, full_marks FROM result WHERE roll=? AND course=?",
                        (self.var_roll.get(), self.var_course.get()))
            rows = cur.fetchall()
            
            for row in rows:
                obtained = int(row[1])  # marks obtained
                full = int(row[2])      # full marks
                total_obtained += obtained
                total_full += full
                
                self.result_table.insert('', END, values=row)  # Show result row
            
            # Calculate percentage
            if total_full > 0:
                percentage = (total_obtained / total_full) * 100
            else:
                percentage = 0
            
            # Show total and percentage
            self.total_marks_label.config(text=f"Total Marks: {total_obtained} / {total_full}  ({percentage:.2f}%)")

        except Exception as ex:
            messagebox.showerror("Error", f"Error loading results: {str(ex)}")


    def delete_selected(self):
        selected_item = self.result_table.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a subject to delete", parent=self.root)
            return

        values = self.result_table.item(selected_item, "values")
        subject = values[0]

        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete result for '{subject}'?", parent=self.root)
        if not confirm:
            return

        try:
            con = sqlite3.connect(database="student_results.db")
            cur = con.cursor()
            cur.execute("DELETE FROM result WHERE roll=? AND course=? AND subject=?",
                        (self.var_roll.get(), self.var_course.get(), subject))
            con.commit()
            messagebox.showinfo("Deleted", f"Result for '{subject}' deleted successfully.", parent=self.root)
            self.load_existing_results()
        except Exception as ex:
            messagebox.showerror("Error", f"Error while deleting: {str(ex)}")

    def on_select_row(self, event):
        selected_item = self.result_table.focus()
        if selected_item:
            self.delete_button.config(state=NORMAL)
        else:
            self.delete_button.config(state=DISABLED)


if __name__ == "__main__":
    root = Tk()
    obj = resultClass(root)
    root.mainloop()
