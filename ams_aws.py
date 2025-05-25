import threading
import tkinter as tk
from tkinter import Label, Button, Entry, Canvas, messagebox
from PIL import Image, ImageTk, ImageEnhance
import cv2
import pandas as pd
from pyzbar.pyzbar import decode
import mysql.connector
from datetime import datetime
import openpyxl
import re

# from attendance_system import mark_attendance

class AttendanceHome:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")
        self.root.state("zoomed")
        
        # Load Background Image
        self.bg_image = Image.open("college.jpg")  # Ensure this image is in the same directory
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        # Canvas for Background
        self.canvas = Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Load College Logo
        #remove_white_background("college_logo.png")
        self.logo_image = Image.open("college_logo.png").convert("RGBA")
        self.logo_image = self.logo_image.resize((60, 60), Image.Resampling.BICUBIC)  # Resize with high quality
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        
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
        #Button(header_frame, text="Home", font=("Arial", 12, "bold"), command=self.home_action).place(x=20, y=20)
        Button(header_frame, text="Close Window", font=("Arial", 12, "bold"), command=self.confirm_logout).place(x=self.root.winfo_screenwidth()-150, y=20)
        
        # Student Registration Section (Left)
        student_frame = tk.Frame(self.root, bg="#e6f0ff", bd=3, relief=tk.RIDGE)
        student_frame.place(relx=0.05, rely=0.3, relwidth=0.25, relheight=0.5)
        Label(student_frame, text="Student Register", font=("Arial", 14, "bold"), bg="#aad4ff").pack(pady=10)
        Label(student_frame, text="Student Name:").pack()
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

        # Button(student_frame, text="Scan ID card", command=self.capture_barcode).pack(pady=5)
        Button(student_frame, text="Register", font=("Arial", 12, "bold"), width=20, command=self.validate_student_registration).pack(pady=10)
        Button(student_frame, text="CLEAR", font=("Arial", 10, "bold"), command=self.clear_student_fields).pack(pady=5, side="left")
        
        # Faculty Registration Section (Center)
        faculty_frame = tk.Frame(self.root, bg="#e6f0ff", bd=3, relief=tk.RIDGE)
        faculty_frame.place(relx=0.375, rely=0.3, relwidth=0.25, relheight=0.5)
        Label(faculty_frame, text="Faculty Register", font=("Arial", 14, "bold"), bg="#99c2ff").pack(pady=10)
        Label(faculty_frame, text="Faculty Name:").pack()
        self.faculty_name = Entry(faculty_frame, width=30)
        self.faculty_name.pack(pady=5)
        Label(faculty_frame, text="Department:").pack()
        self.faculty_dept = Entry(faculty_frame, width=30)
        self.faculty_dept.pack(pady=5)
        Label(faculty_frame, text="ID Number:").pack()
        self.faculty_id = Entry(faculty_frame,width=30)
        self.faculty_id.pack(pady=5)
        self.faculty_error = Label(faculty_frame, text="", fg="red")
        self.faculty_error.pack()
        
        # Button(faculty_frame, text="Scan ID card", command=self.capture_barcode).pack(pady=5)
        Button(faculty_frame, text="Register", font=("Arial", 12, "bold"), width=20, command=self.validate_faculty_registration).pack(pady=10)
        Button(faculty_frame, text="CLEAR", font=("Arial", 10, "bold"), command=self.clear_faculty_fields).pack(pady=5, side="left")
        
        # Mark Attendance Section (Right)
        attendance_frame = tk.Frame(self.root, bg="#e6f0ff", bd=3, relief=tk.RIDGE)
        attendance_frame.place(relx=0.7, rely=0.3, relwidth=0.25, relheight=0.5)
        Label(attendance_frame, text="Student Attendance", font=("Arial", 14, "bold"), bg="#80bfff").pack(pady=(40,10))
        Button(attendance_frame, text="Mark Attendance", bg="#9FEF7B", font=("Arial", 12, "bold"), command=self.scan_barcode).pack(pady=(10,10))

        # Facutly Section
        Label(attendance_frame, text="Faculty Attendance", font=("Arial",14,"bold"), bg="#80bfff").pack(pady=(30,10))
        Button(attendance_frame, text="Mark Attendance",bg="#9FEF7B", font=("Arial", 12, "bold"),command=self.scan_faculty_idCard).pack(pady=(10))
        
        #Generate Attendance report
        month = datetime.now().strftime("%m")
        year = datetime.now().strftime("%Y")
        report_button = tk.Button(self.root, text="Generate Monthly Report", font=("Arial", 12, "bold"),bg="#9FEF7B", command=lambda: show_login_popup(month, year))
        report_button.place(relx=0.75, rely=0.2, relwidth=0.2, height=40)

        # ReadMe Button to Show Features
        readme_button = tk.Button(self.root, text="📖 README", font=("Arial", 14, "bold"), bg="#FFD700", command=self.show_features)
        readme_button.place(relx=0.85, rely=0.85, relwidth=0.1, height=40)  # Positioned slightly above previous placement


        # Footer
        footer_frame = tk.Frame(self.root, bg="black")
        footer_frame.place(relwidth=1, rely=0.95, height=30)
        Label(footer_frame, text="Developed and crafted by DeveloperDen.co.in Bengaluru", font=("Arial", 10, "bold"), bg="black", fg="white").pack()
        
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
    
    def capture_barcode(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            cv2.imshow("Capture Barcode", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    

    #     cap = cv2.VideoCapture(0)
    #     while True:
    #         ret, frame = cap.read()
    #         for barcode in decode(frame):
    #             print("Scanned Data:", barcode.data.decode('utf-8'))
    #             cap.release()
    #             cv2.destroyAllWindows()
    #             return
    #         cv2.imshow("Scan Barcode", frame)
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #     cap.release()
    #     cv2.destroyAllWindows()

    def clear_student_fields(self):
        self.student_name.delete(0, tk.END)
        self.student_usn.delete(0, tk.END)
        self.student_department.delete(0,tk.END)
        self.student_error.config(text="")
    
    def clear_faculty_fields(self):
        self.faculty_name.delete(0, tk.END)
        self.faculty_dept.delete(0, tk.END)
        #self.faculty_dept.delete(0,tk.END)
        self.faculty_id.delete(0,tk.END)
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

    # def validate_student_fields(self):
    #     regex = r"^[A-Za-zÀ-ÿ-'\s]{3,50}$"
    #     student_usn = self.student_usn
    #     if re.match(self.student_name,regex!=True):
    #         self.student_error.config(text="Username shouldn't be alpha numerical")
    #     if re.match(self.student_department!=True):
    #         self.student_error.config(text="Department shouldn't be alpha numerical")
    #     if (re.match(self.student_usn!=True) and student_usn.len!=10):
    #         self.student_error.config(text="Please Enter valid USN with 10 character")
        

    def validate_student_registration(self):
        regex = r"^[A-Za-zÀ-ÿ-'\s]{3,50}$"
        student_name = self.student_name.get().strip()
        student_usn = self.student_usn.get().strip()
        student_department = self.student_department.get().strip()

         # Clear previous errors
        self.student_error.config(text="", fg="red")
        is_valid = True

        if not self.student_name.get().strip() or not self.student_usn.get().strip() or not self.student_department.get().strip():
            self.student_error.config(text="All fields are mandatory!")
            is_valid = False

        # Validate Student Name (Only Alphabets)
        elif not all(c.isalpha() or c.isspace() for c in student_name):
            print(student_name)
            self.student_error.config(text="Invalid!, Please enter valid name", fg="red")
            is_valid = False

        # Validate USN (Exactly 10 characters, Alphanumeric, No Special Characters)
        elif len(student_usn) != 10 or not student_usn.isalnum():
            self.student_error.config(text="Invalid!, Please enter valid USN", fg="red")
            is_valid = False

        # Validate Department (Only Alphabets)
        elif not student_department.isalpha():
            self.student_error.config(text="Invalid!, Please enter valid deparment name", fg="red")
            is_valid = False

        # Register Student if all validations pass
        if is_valid:
            register_student(student_name, student_usn, student_department)
            #self.student_error.config(text="✅ Student Registered Successfully!", fg="green")


    def validate_faculty_registration(self):
        faculty_name = self.faculty_name.get().strip()
        department_name = self.faculty_dept.get().strip()
        faculty_id = self.faculty_id.get().strip()
        isValid = True

        self.faculty_error.config(text="",fg="red")

        if not self.faculty_name.get().strip() or not self.faculty_dept.get().strip() or not self.faculty_id.get().strip():
            self.faculty_error.config(text="All fields are mandatory!")
            isValid = False

        elif not all(f.isalpha() or f.isspace() for f in faculty_name):
            self.faculty_error.config(text="Invalid!, Please enter a valid name",fg="red")
            isValid = False

        elif not department_name.isalpha():
            self.faculty_error.config(text="Invalid!, Please enter valid department name", fg="red")
            isValid = False

        elif len(faculty_id)!=10 or  not faculty_id.isalnum():
            self.faculty_error.config(text="Invalid!, Please enter a valid ID", fg="red")
            isValid = False

        if isValid:
            register_faculty(faculty_name,department_name,faculty_id)


    def scan_barcode(self):
        threading.Thread(target=self.open_camera, daemon=True).start()

    def open_camera(self):
        cap = cv2.VideoCapture(0)  # Open webcam
        if not cap.isOpened():
            messagebox.showerror("Error", "Failed to open the camera!")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break  # If frame capture fails, exit loop

            for barcode in decode(frame):
                scanned_data = barcode.data.decode('utf-8')
                print("Scanned Data:", scanned_data)
                cap.release()
                cv2.destroyAllWindows()
                self.mark_attendance(scanned_data)
                return  # Exit function after scanning

            cv2.imshow("Scan Barcode", frame)

            # Exit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def mark_attendance(self, student_usn):
        conn = db_connect()
        cursor = conn.cursor()

        # Check if student exists
        cursor.execute("SELECT id, username FROM students WHERE usn = %s", (student_usn,))
        student = cursor.fetchone()

        if student:
            student_id, student_name = student

            # Check if attendance is already marked today
            today_date = datetime.now().date()
            cursor.execute("SELECT * FROM attendance WHERE student_id = %s AND date = %s", (student_id, today_date))
            existing_attendance = cursor.fetchone()

            if existing_attendance:
                messagebox.showerror("Error", f"Attendance already marked for {student_name} (USN: {student_usn}) today!")
            else:
                # Insert attendance record if not already marked
                query = "INSERT INTO attendance (student_id, date) VALUES (%s, %s)"
                cursor.execute(query, (student_id, today_date))
                conn.commit()
                messagebox.showinfo("Success", f"Attendance marked for {student_name} (USN: {student_usn}) for today")

        else:
            messagebox.showerror("Error", f"No student found with USN: {student_usn}, please register and try again!")

        conn.close()


    def scan_faculty_idCard(self):
        threading.Thread(target=self.faculty_open_camera, daemon=True).start()

    
    def faculty_open_camera(self):
        cap = cv2.VideoCapture(0)  # Open webcam
        if not cap.isOpened():
            messagebox.showerror("Error", "Failed to open the camera!")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break  # If frame capture fails, exit loop

            for barcode in decode(frame):
                scanned_data = barcode.data.decode('utf-8')
                print("Scanned Data:", scanned_data)
                cap.release()
                cv2.destroyAllWindows()
                self.faculty_mark_attendance(scanned_data)
                return  # Exit function after scanning

            cv2.imshow("Scan Barcode", frame)

            # Exit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


    #Mark Faculty attendance
    def faculty_mark_attendance(self,faculty_id):
        conn = db_connect()
        cursor = conn.cursor()

        # Check if faculty exists
        cursor.execute("SELECT id, username FROM faculty WHERE faculty_id = %s", (faculty_id,))
        faculty = cursor.fetchone()

        if faculty:
            faculty_id, faculty_name = faculty

            # Check if attendance is already marked today
            today_date = datetime.now().date()
            cursor.execute("SELECT * FROM attendance_faculty WHERE faculty_id = %s AND date = %s", (faculty_id, today_date))
            existing_attendance = cursor.fetchone()

            if existing_attendance:
                messagebox.showerror("Error", f"Attendance already marked for {faculty_id} (ID: {faculty_name}) today!")
            else:
                # Insert attendance record if not already marked
                query = "INSERT INTO attendance_facutly (faculty_id, date) VALUES (%s, %s)"
                cursor.execute(query, (faculty_id, today_date))
                conn.commit()
                messagebox.showinfo("Success", f"Attendance marked for {faculty_name} (ID: {faculty_id})")

        else:
            messagebox.showerror("Error", f"No Faculty found with ID: {faculty_id}, please register and try again!")

        conn.close()



#Student register        
def register_student(username, usn, department):
    conn = db_connect()
    cursor = conn.cursor()

    getStudent = """ SELECT * FROM students where usn= %s"""
    cursor.execute(getStudent,(usn,))
    student = cursor.fetchone()
    if(student):
        messagebox.showerror("Error!", f"Student already registered with this USN: {usn}")
    else:
        query = """INSERT INTO students (username, usn, department)
                VALUES (%s, %s, %s)"""
        cursor.execute(query, (username, usn, department))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"✅Student Registered Successfully! with USN: {usn}")   


#Faculty Register
def register_faculty(username,deparment,id):
    conn = db_connect()
    cursor = conn.cursor()

    getFacutly = """ SELECT * FROM faculty where faculty_id= %s"""
    cursor.execute(getFacutly,(id,))
    faculty = cursor.fetchone()
    if(faculty):
        messagebox.showerror("Error!", f"Faculty already registered with this USN: {id}")
    else:
        query = """INSERT INTO faculty (username, department, faculty_id)
                VALUES (%s, %s, %s)"""
        cursor.execute(query, (username, deparment, id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"✅Facutly Registered Successfully with USN: {id}")   


# Function to generate monthly attendance report
def generate_report(month, year):
    conn = db_connect()
    cursor = conn.cursor()

    # Fetch student attendance data
    student_query = """SELECT students.username, students.usn, COUNT(attendance.id) AS attendance_count
               FROM attendance
               JOIN students ON attendance.student_id = students.id
               WHERE YEAR(attendance.date) = %s AND MONTH(attendance.date) = %s
               GROUP BY students.username,students.usn"""
    cursor.execute(student_query, (year, month))
    students_results = cursor.fetchall()
    student_df = pd.DataFrame(students_results, columns=["Username", "USN", "Attendance Count"])

    # Fetch faculty attendance data
    faculty_query = """SELECT faculty.username, faculty.faculty_id, COUNT(attendance_faculty.id) AS attendance_count
                    FROM attendance_faculty
                    JOIN faculty ON attendance_faculty.faculty_code = faculty.id
                    WHERE YEAR(attendance_faculty.date) = %s AND MONTH(attendance_faculty.date) = %s
                    GROUP BY faculty.username,faculty.faculty_id"""
    cursor.execute(faculty_query, (year, month))
    faculty_results = cursor.fetchall()
    faculty_df = pd.DataFrame(faculty_results, columns=["Username", "Faculty ID","Attendance Count"])

    # Creating DataFrame to an Excel file with separate sheets
    report_filename = f"attendance_report_{month}_{year}.xlsx"
    with pd.ExcelWriter(report_filename, engine="openpyxl") as writer:
        student_df.to_excel(writer, sheet_name="student_attendance_report", index=False)
        faculty_df.to_excel(writer, sheet_name="faculty_attendance_report", index=False)
    messagebox.showinfo("Report", f"Report generated: {report_filename}")

def show_login_popup(month, year):
    login_window = tk.Toplevel()
    login_window.title("Authentication")
    login_window.geometry("300x180")
    login_window.resizable(False, False)

    tk.Label(login_window, text="Username:").pack(pady=(15, 0))
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password:").pack(pady=(10, 0))
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    def submit_login():
        username = username_entry.get()
        password = password_entry.get()

        # Static credentials
        if username == "admin" and password == "admin@kns":
            login_window.destroy()
            generate_report(month, year)
        else:
            messagebox.showerror("Access Denied", "Invalid username or password.")

    submit_btn = tk.Button(login_window, text="Submit", command=submit_login)
    submit_btn.pack(pady=15)

    # Creating DataFrame for reporting
    # df = pd.DataFrame(results, columns=["Username", "USN", "Attendance Count"])
    # df.to_csv(f"attendance_report_{month}_{year}.csv", index=False)
    # messagebox.showinfo("Report", f"Report generated: attendance_report_{month}_{year}.csv")


# def mark_attendance():
#     conn = db_connect()
#     cursor = conn.cursor()
    
#     # Open webcam for attendance recognition
#     cap = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Detect faces and barcode
#         #faces = face_recognition.face_locations(frame)
#         barcodes = decode(frame)

#         # Barcode scanning logic
#         if barcodes:
#             barcode_data = barcodes[0].data.decode("utf-8")
#             query = "SELECT * FROM students WHERE barcode_data = %s"
#             cursor.execute(query, (barcode_data,))
#             student = cursor.fetchone()
#             if student:
#                 student_id = student[0]
#                 date = datetime.now().date()
#                 query = "SELECT * FROM attendance WHERE student_id = %s AND date = %s"
#                 cursor.execute(query, (student_id, date))
#                 if cursor.fetchone() is None:
#                     query = "INSERT INTO attendance (student_id, date) VALUES (%s, %s)"
#                     cursor.execute(query, (student_id, date))
#                     conn.commit()
#                     messagebox.showinfo("Attendance", "Attendance marked for student " + student[1])
#                 else:
#                     messagebox.showerror("Attendance" "Attendance marked for student for today"+ student[1])
#             else:
#                 messagebox.showerror("Attendance","Sudent not registered, Please register and try again"+ student[1])

#     cap.release()
#     cv2.destroyAllWindows()
#     conn.close()


#Remove background color and increase brightness
def remove_white_background(image_path):
    image = Image.open(image_path).convert("RGBA")  
    data = image.getdata()

    new_data = []
    for item in data:
        # Check for white or near white pixels
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((255, 255, 255, 0)) 
        else:
            new_data.append(item)

    image.putdata(new_data)

    # Increase Brightness and Sharpness
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(19)  

    sharpness = ImageEnhance.Sharpness(image)
    image = sharpness.enhance(20)

    image.putdata(new_data)
    image.save("logo_without_bg.png")

#Database Connection
def db_connect():
    return mysql.connector.connect(
            host="ams.c3gyigam0110.eu-north-1.rds.amazonaws.com", user="admin", password="awstest2025", database="attendance_system")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceHome(root)
    root.mainloop()
