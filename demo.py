import tkinter as tk
from tkinter import Label, Button, Entry, Canvas, messagebox
from PIL import Image, ImageTk, ImageEnhance
import cv2
import pandas as pd
from pyzbar.pyzbar import decode
import mysql.connector
from datetime import datetime

class AttendanceHome:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")
        self.root.state("zoomed")
        
        # Load Background Image
        self.bg_image = Image.open("college.jpg")  # Ensure this image is in the same directory
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Load College Logo
        remove_white_background("college_logo.png") 
        self.logo_image = Image.open("logo_without_bg.png").resize((60, 60), Image.Resampling.LANCZOS)  # Resize with high quality
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)


        # Canvas for Background
        self.canvas = Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        
        # Header
        header_frame = tk.Frame(self.root, bg="#004488")
        header_frame.place(relwidth=1, height=80)
        
        Label(header_frame, text="Attendance Management System", font=("Arial", 20, "bold"), bg="#004488", fg="white").pack()
        Label(header_frame, text="KNS Institute of Technology and Engineering", font=("Arial", 14, "bold"), bg="#004488", fg="white").pack()
        
        # College Logo on the Left Side
        logo_label = Label(header_frame, image=self.logo_photo, bg="#004488")
        logo_label.place(x=335, y=10)

        # Right Logo
        logo_right = tk.Label(header_frame, image=self.logo_photo, bg="#004488")
        logo_right.place(x=875, y=10)

        # Home and Logout Buttons
        Button(header_frame, text="Home", font=("Arial", 12, "bold"), command=self.home_action).place(x=20, y=20)
        Button(header_frame, text="Logout", font=("Arial", 12, "bold"), command=self.confirm_logout).place(x=self.root.winfo_screenwidth()-100, y=20)
        
        # Student Registration Section (Left)
        student_frame = tk.Frame(self.root, bg="#e6f0ff", bd=3, relief=tk.RIDGE)
        student_frame.place(relx=0.05, rely=0.3, relwidth=0.25, relheight=0.5)
        Label(student_frame, text="Student Register", font=("Arial", 14, "bold"), bg="#aad4ff").pack(pady=10)
        Label(student_frame, text="Username:").pack()
        self.student_name = Entry(student_frame, width=30)
        self.student_name.pack(pady=5)
        Label(student_frame, text="USN:").pack()
        self.student_usn = Entry(student_frame, width=30)
        self.student_usn.pack(pady=5)
        Label(student_frame, text="Department:").pack()
        self.student_department = Entry(student_frame, width=30)
        self.student_department.pack(pady=5)
        self.student_error = Label(student_frame, text="", fg="red")
        self.student_error.pack()
        Button(student_frame, text="Register", font=("Arial", 12, "bold"), width=20, command=self.validate_student_registration).pack(pady=10)
        Button(student_frame, text="CLEAR", font=("Arial", 10, "bold"), command=self.clear_student_fields).pack(pady=5, side="left")
        
        # Faculty Registration Section (Center)
        faculty_frame = tk.Frame(self.root, bg="#e6f0ff", bd=3, relief=tk.RIDGE)
        faculty_frame.place(relx=0.375, rely=0.3, relwidth=0.25, relheight=0.5)
        Label(faculty_frame, text="Faculty Register", font=("Arial", 14, "bold"), bg="#99c2ff").pack(pady=10)
        Label(faculty_frame, text="Username:").pack()
        self.faculty_name = Entry(faculty_frame, width=30)
        self.faculty_name.pack(pady=5)
        Label(faculty_frame, text="Department:").pack()
        self.faculty_dept = Entry(faculty_frame, width=30)
        self.faculty_dept.pack(pady=5)
        self.faculty_error = Label(faculty_frame, text="", fg="red")
        self.faculty_error.pack()
        Button(faculty_frame, text="Register", font=("Arial", 12, "bold"), width=20, command=self.validate_faculty_registration).pack(pady=10)
        Button(faculty_frame, text="CLEAR", font=("Arial", 10, "bold"), command=self.clear_faculty_fields).pack(pady=5, side="left")
        
        # Generate Attendance Report Button (Moved Above Mark Attendance Panel)
        month = datetime.now().strftime("%m")
        year = datetime.now().strftime("%Y")
        report_button = tk.Button(self.root, text="Generate Monthly Report", font=("Arial", 12, "bold"), command=lambda: generate_report(month, year))
        report_button.place(relx=0.7, rely=0.23, relwidth=0.25, height=40)
        
        # Mark Attendance Section (Right)
        attendance_frame = tk.Frame(self.root, bg="#e6f0ff", bd=3, relief=tk.RIDGE)
        attendance_frame.place(relx=0.7, rely=0.3, relwidth=0.25, relheight=0.5)
        Label(attendance_frame, text="Student Attendance", font=("Arial", 14, "bold"), bg="#80bfff").pack(pady=(40,10))
        Button(attendance_frame, text="Mark Attendance", bg="#358958", font=("Arial", 12, "bold")).pack(pady=(10,10))

        Label(attendance_frame, text="Faculty Attendance", font=("Arial",14,"bold"), bg="#80bfff").pack(pady=(40,10))
        Button(attendance_frame, text="Mark Attendance",bg="#358958", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg="black")
        footer_frame.place(relwidth=1, rely=0.95, height=30)
        Label(footer_frame, text="Developed and crafted by DeveloperDen.co.in Bengaluru", font=("Arial", 10, "bold"), bg="black", fg="white").pack()

        # ReadMe Button to Show Features
        readme_button = tk.Button(self.root, text="📖 README", font=("Arial", 14, "bold"), bg="#FFD700", command=self.show_features)
        readme_button.place(relx=0.85, rely=0.85, relwidth=0.1, height=40)  # Positioned slightly above previous placement

        # readme_button = tk.Button(self.root, text="ℹ️", font=("Arial", 16, "bold"), bg="#FFD700", relief="ridge", bd=2)
        # readme_button.place(relx=0.88, rely=0.78, width=50, height=50)  # Adjust position as needed
        # readme_button.config(borderwidth=2, highlightthickness=2)
        
        self.root.protocol("WM_DELETE_WINDOW", self.confirm_exit)


    def home_action(self):
        # self.root.destroy()  
        # root = tk.Tk()  
        # app = AttendanceHome(root)  
        # root.mainloop()
        self.root.update_idletasks()
        self.root.update()
    
    def confirm_logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.quit()
    
    def confirm_exit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()
    def validate_student_registration(self):
        if not self.student_name.get().strip() or not self.student_usn.get().strip() or not self.student_department.get().strip():
            self.student_error.config(text="All fields are mandatory!")
        else:
            studentName = self.student_name.get().strip()
            studentUsn = self.student_usn.get().strip()
            studentDepartment = self.student_department.get().strip()
            #register_student(studentName,studentUsn,studentDepartment)
            print(f"student Name:{studentName} student usn:{studentUsn} student department:{studentDepartment}")
            self.student_error.config(text="Student Registered Successfully", fg="green")
    
    def validate_faculty_registration(self):
        if not self.faculty_name.get().strip() or not self.faculty_dept.get().strip():
            self.faculty_error.config(text="All fields are mandatory!")
        else:
            facultyName = self.faculty_name.get().strip()
            departmentName = self.faculty_dept.get().strip()
            print(f"Facutly name:{facultyName} Faculty deparment:{departmentName}")
            # print("Faculty Name:", facultyName)
            self.faculty_error.config(text="Faculty Registered Successfully", fg="green")

    def clear_student_fields(self):
        self.student_name.delete(0, tk.END)
        self.student_usn.delete(0, tk.END)
        self.student_department.delete(0,tk.END)
        self.student_error.config(text="")
    
    def clear_faculty_fields(self):
        self.faculty_name.delete(0, tk.END)
        self.faculty_dept.delete(0, tk.END)
        self.faculty_dept.delete(0,tk.END)
        self.faculty_error.config(text="")
    
    def show_features(self):
        features = (
            "📌 Features of Attendance Management System:\n\n"
            "✅ Student Registration\n"
            "✅ Faculty Registration\n"
            "✅ Barcode-based Attendance Marking\n"
            "✅ Prevents Duplicate Attendance Entries\n"
            "✅ Generates Monthly Attendance Reports\n"
            "✅ Home & Logout Functionality\n"
            "✅ User-Friendly Interface\n"
        )
        messagebox.showinfo("Application Features", features)

    def generate_report(month, year):
        conn = db_connect()
        cursor = conn.cursor()

        # Fetch student attendance data
        student_query = """SELECT students.username, COUNT(attendance.id) AS attendance_count
                        FROM attendance
                        JOIN students ON attendance.student_id = students.id
                        WHERE YEAR(attendance.date) = %s AND MONTH(attendance.date) = %s
                        GROUP BY students.username"""
        cursor.execute(student_query, (year, month))
        student_results = cursor.fetchall()
        student_df = pd.DataFrame(student_results, columns=["Username", "Attendance Count"])

        # Fetch faculty attendance data
        faculty_query = """SELECT faculty.username, COUNT(attendance.id) AS attendance_count
                        FROM attendance
                        JOIN faculty ON attendance.faculty_id = faculty.id
                        WHERE YEAR(attendance.date) = %s AND MONTH(attendance.date) = %s
                        GROUP BY faculty.username"""
        cursor.execute(faculty_query, (year, month))
        faculty_results = cursor.fetchall()
        faculty_df = pd.DataFrame(faculty_results, columns=["Username", "Attendance Count"])

        # Write both dataframes to an Excel file with separate sheets
        report_filename = f"attendance_report_{month}_{year}.xlsx"
        with pd.ExcelWriter(report_filename) as writer:
            student_df.to_excel(writer, sheet_name="student_attendance_report", index=False)
            faculty_df.to_excel(writer, sheet_name="faculty_attendance_report", index=False)

        conn.close()
        messagebox.showinfo("Report", f"Report generated: {report_filename}")

def remove_white_background(image_path):
    image = Image.open(image_path).convert("RGBA")  
    data = image.getdata()

    new_data = []
    for item in data:
        # Check for white or near white pixels
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((255, 255, 255, 0))  # Replace white with transparent
        else:
            new_data.append(item)

    image.putdata(new_data)

    # Increase Brightness and Sharpness
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(19)  # Increase brightness by 1.5x

    sharpness = ImageEnhance.Sharpness(image)
    image = sharpness.enhance(20)

    image.putdata(new_data)
    image.save("logo_without_bg.png")

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceHome(root)
    root.mainloop()
