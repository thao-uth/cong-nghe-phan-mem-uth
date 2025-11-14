import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime
import os

DB_FILE = "attendance_gui.db"
LOGO_FILE = "uth.png"

# =================== DATABASE SETUP ===================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Tạo bảng người dùng
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)

    # Tạo bảng điểm danh
    c.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        student_name TEXT,
        date TEXT,
        status TEXT
    )
    """)

    # Tạo tài khoản mặc định nếu chưa có
    c.execute("INSERT OR IGNORE INTO users VALUES ('teacher','1234','teacher')")
    c.execute("INSERT OR IGNORE INTO users VALUES ('student','0000','student')")

    conn.commit()
    conn.close()

init_db()

# =================== MAIN APPLICATION ===================
class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Attendance System")
        self.root.geometry("950x600")
        self.root.resizable(False, False)
        self.logo_path = LOGO_FILE
        self.create_login_screen()

    # ---------- HEADER ----------
    def create_header(self):
        header = tk.Frame(self.root, bg="#d9e1f2", height=70)
        header.pack(fill="x")

        try:
            if os.path.exists(self.logo_path):
                img = Image.open(self.logo_path)
                img = img.resize((150, 90), Image.LANCZOS)
                self.logo = ImageTk.PhotoImage(img)
                tk.Label(header, image=self.logo, bg="#d9e1f2").pack(side="right", padx=30, pady=2)
        except Exception:
            pass

        tk.Label(header, text="Student Attendance System",
                 font=("Times New Roman", 22, "bold"),
                 fg="navy", bg="#d9e1f2").pack(side="left", padx=60, pady=5)

    # ---------- LOGIN SCREEN ----------
    def create_login_screen(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.root.configure(bg="#f2f4f7")
        self.create_header()

        # Giao diện login
        login_frame = tk.Frame(self.root, bg="#f2f4f7")
        login_frame.place(relx=0.5, rely=0.55, anchor="center")

        tk.Label(login_frame, text="User Login", font=("Times New Roman", 20, "bold"),
                 fg="#003366", bg="#f2f4f7").grid(row=0, column=0, columnspan=2, pady=(20, 10))

        tk.Label(login_frame, text="Username:", font=("Times New Roman", 14),
                 bg="#f2f4f7").grid(row=1, column=0, padx=15, pady=10, sticky="e")
        self.username_entry = tk.Entry(login_frame, font=("Times New Roman", 14),
                                       width=25, bd=2, relief="solid")
        self.username_entry.grid(row=1, column=1, padx=15, pady=10)

        tk.Label(login_frame, text="Password:", font=("Times New Roman", 14),
                 bg="#f2f4f7").grid(row=2, column=0, padx=15, pady=10, sticky="e")
        self.password_entry = tk.Entry(login_frame, font=("Times New Roman", 14),
                                       show="*", width=25, bd=2, relief="solid")
        self.password_entry.grid(row=2, column=1, padx=15, pady=10)

        tk.Button(login_frame, text="Login",
                  font=("Times New Roman", 14, "bold"),
                  bg="#2e8b57", fg="white",
                  activebackground="#2f975e",
                  width=15, height=1, relief="flat",
                  command=self.login).grid(row=3, column=0, columnspan=2, pady=20)

    # ---------- LOGIN LOGIC ----------
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter username and password.")
            return

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone()
        conn.close()

        if not result:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            return

        role = result[0]
        messagebox.showinfo("Welcome", f"Welcome {username} ({role})")

        if role == "teacher":
            self.create_teacher_screen()
        elif role == "student":
            self.create_student_screen()
        else:
            messagebox.showerror("Role Error", "Unknown user role!")

    # ---------- TEACHER SCREEN ----------
    def create_teacher_screen(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.root.configure(bg="white")
        self.create_header()

        tk.Label(self.root, text="Teacher Dashboard",
                 font=("Times New Roman", 20, "bold"), fg="navy", bg="white").pack(pady=15)

        self.create_attendance_form()
        self.create_table_buttons(admin=True)
        self.load_attendance()

    # ---------- STUDENT SCREEN ----------
    def create_student_screen(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.root.configure(bg="white")
        self.create_header()

        tk.Label(self.root, text="Student Dashboard",
                 font=("Times New Roman", 20, "bold"), fg="darkred", bg="white").pack(pady=15)

        self.create_attendance_form()
        self.create_table_buttons(admin=False)
        self.load_attendance()

    # ---------- ATTENDANCE FORM ----------
    def create_attendance_form(self):
        form_frame = tk.Frame(self.root, bg="white")
        form_frame.pack(pady=15)

        tk.Label(form_frame, text="Student ID:", font=("Times New Roman", 14),
                 bg="white").grid(row=0, column=0, padx=8, pady=5, sticky="e")
        self.student_id = tk.Entry(form_frame, font=("Times New Roman", 14), width=14)
        self.student_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Student Name:", font=("Times New Roman", 14),
                 bg="white").grid(row=0, column=2, padx=8, pady=5, sticky="e")
        self.student_name = tk.Entry(form_frame, font=("Times New Roman", 14), width=18)
        self.student_name.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Status:", font=("Times New Roman", 14),
                 bg="white").grid(row=0, column=4, padx=8, pady=5, sticky="e")
        self.status_var = tk.StringVar()
        combo = ttk.Combobox(form_frame, textvariable=self.status_var,
                             values=["Present", "Absent", "Late"],
                             width=12, font=("Times New Roman", 13))
        combo.grid(row=0, column=5, padx=5, pady=5)
        combo.current(0)

        tk.Button(form_frame, text="Save Attendance",
                  font=("Times New Roman", 13, "bold"),
                  bg="green", fg="white", width=16,
                  command=self.save_attendance).grid(row=0, column=6, padx=15, pady=5)

        cols = ("id", "student_id", "student_name", "date", "status")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=150, anchor="center")
        self.tree.pack(pady=10, fill="x", padx=20)

    # ---------- BUTTONS ----------
    def create_table_buttons(self, admin=False):
        btn_frame = tk.Frame(self.root, bg="white")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Refresh", command=self.load_attendance,
                  bg="blue", fg="white", font=("Times New Roman", 13), width=10).pack(side="left", padx=10)

        if admin:
            tk.Button(btn_frame, text="Reset All", command=self.reset_attendance,
                      bg="orange", fg="black", font=("Times New Roman", 13), width=12).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Logout", command=self.create_login_screen,
                  bg="red", fg="white", font=("Times New Roman", 13), width=12).pack(side="left", padx=10)

    # ---------- SAVE ----------
    def save_attendance(self):
        sid = self.student_id.get().strip()
        name = self.student_name.get().strip()
        status = self.status_var.get().strip()

        if not sid or not name:
            messagebox.showwarning("Input Error", "Please enter both Student ID and Name.")
            return
        try:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("INSERT INTO attendance (student_id, student_name, date, status) VALUES (?, ?, ?, ?)",
                      (sid, name, datetime.now().strftime("%Y-%m-%d %H:%M"), status))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Attendance saved successfully.")
            self.student_id.delete(0, tk.END)
            self.student_name.delete(0, tk.END)
            self.load_attendance()
        except Exception as e:
            messagebox.showerror("DB Error", f"Error saving attendance:\n{e}")

    # ---------- LOAD ----------
    def load_attendance(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("SELECT * FROM attendance ORDER BY id DESC")
            rows = c.fetchall()
            conn.close()
            for r in rows:
                self.tree.insert("", tk.END, values=r)
        except Exception as e:
            messagebox.showerror("DB Error", f"Load error:\n{e}")

    # ---------- RESET ----------
    def reset_attendance(self):
        if not messagebox.askyesno("Confirm", "Delete all attendance records?"):
            return
        try:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("DELETE FROM attendance")
            conn.commit()
            conn.close()
            self.load_attendance()
            messagebox.showinfo("Reset", "All records cleared.")
        except Exception as e:
            messagebox.showerror("DB Error", f"Reset error:\n{e}")


# =================== RUN ===================
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
