import cv2
import mysql.connector
from pyzbar.pyzbar import decode
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import numpy as np
from PIL import Image
from datetime import datetime
import pandas as pd

# Database Connection
def db_connect():
    return mysql.connector.connect(
        host="localhost", user="root", password="techspace@123", database="attendance_system"
    )

# Function to register a student
def register_student(username, usn, department):
    conn = db_connect()
    cursor = conn.cursor()

    # Capture face encoding if no image is provided
    # if image_path:
    #     image = cv2.imread(image_path)
    #     face_locations = face_recognition.face_locations(image)
    #     if len(face_locations) == 0:
    #         messagebox.showerror("Error", "No face found in the image")
    #         return

    #     # Get the encoding for the face
    #     face_encoding = face_recognition.face_encodings(image, face_locations)[0]
    # else:
    #     face_encoding = None

    # Insert student data into the database
    query = """INSERT INTO students (username, usn, department)
               VALUES (%s, %s, %s)"""
    cursor.execute(query, (username, usn, department))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student Registered Successfully!")

# Function to register from UI
def register_ui():
    def on_register():
        username = entry_username.get()
        usn = entry_usn.get()
        department = entry_department.get()
        image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])

        barcode_data = barcode_input.get()
        if barcode_data == "":
            barcode_data = None

        if username and usn and department:
            register_student(username, usn, department, image_path, barcode_data)
        else:
            messagebox.showerror("Error", "All fields must be filled!")

    register_window = tk.Toplevel()
    register_window.title("Register Student")
    
    # Form Fields
    tk.Label(register_window, text="Username").grid(row=0, column=0)
    entry_username = tk.Entry(register_window)
    entry_username.grid(row=0, column=1)
    
    tk.Label(register_window, text="USN").grid(row=1, column=0)
    entry_usn = tk.Entry(register_window)
    entry_usn.grid(row=1, column=1)
    
    tk.Label(register_window, text="Department").grid(row=2, column=0)
    entry_department = tk.Entry(register_window)
    entry_department.grid(row=2, column=1)

    barcode_input = tk.Entry(register_window)
    barcode_input.grid(row=3, column=1)
    tk.Label(register_window, text="Barcode (optional)").grid(row=3, column=0)
    
    register_button = tk.Button(register_window, text="Register", command=on_register)
    register_button.grid(row=4, column=1)
    
    register_window.mainloop()

# Function to perform face recognition or barcode scan for attendance
def mark_attendance():
    conn = db_connect()
    cursor = conn.cursor()
    
    # Open webcam for attendance recognition
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect faces and barcode
        #faces = face_recognition.face_locations(frame)
        barcodes = decode(frame)

#         # Barcode scanning logic
        if barcodes:
            barcode_data = barcodes[0].data.decode("utf-8")
            query = "SELECT * FROM students WHERE barcode_data = %s"
            cursor.execute(query, (barcode_data,))
            student = cursor.fetchone()
            if student:
                student_id = student[0]
                date = datetime.now().date()
                query = "SELECT * FROM attendance WHERE student_id = %s AND date = %s"
                cursor.execute(query, (student_id, date))
                if cursor.fetchone() is None:
                    query = "INSERT INTO attendance (student_id, date) VALUES (%s, %s)"
                    cursor.execute(query, (student_id, date))
                    conn.commit()
                    messagebox.showinfo("Attendance", "Attendance marked for student " + student[1])
                break
            else:
                messagebox.showerror("Attendance","Already marked for today"+ student[1])

#         # Face recognition logic
#         if faces:
#             for face_location in faces:
#                 top, right, bottom, left = face_location
#                 face_image = frame[top:bottom, left:right]
#                 face_encoding = face_recognition.face_encodings(face_image)
#                 if face_encoding:
#                     face_encoding = face_encoding[0]
#                     query = "SELECT * FROM students WHERE face_encoding = %s"
#                     cursor.execute(query, (face_encoding,))
#                     student = cursor.fetchone()
#                     if student:
#                         student_id = student[0]
#                         date = datetime.now().date()
#                         query = "SELECT * FROM attendance WHERE student_id = %s AND date = %s"
#                         cursor.execute(query, (student_id, date))
#                         if cursor.fetchone() is None:
#                             query = "INSERT INTO attendance (student_id, date) VALUES (%s, %s)"
#                             cursor.execute(query, (student_id, date))
#                             conn.commit()
#                             messagebox.showinfo("Attendance", "Attendance marked for student " + student[1])
#                         break

#         # Display the frame
#         cv2.imshow('Attendance System', frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

    cap.release()
    cv2.destroyAllWindows()
    conn.close()

# Function to generate monthly attendance report
def generate_report(month, year):
    conn = db_connect()
    cursor = conn.cursor()

    query = """SELECT students.username, COUNT(attendance.id) AS attendance_count
               FROM attendance
               JOIN students ON attendance.student_id = students.id
               WHERE YEAR(attendance.date) = %s AND MONTH(attendance.date) = %s
               GROUP BY students.username"""
    cursor.execute(query, (year, month))
    results = cursor.fetchall()

    # Creating DataFrame for easy reporting
    df = pd.DataFrame(results, columns=["Username", "Attendance Count"])
    df.to_csv(f"attendance_report_{month}_{year}.csv", index=False)
    messagebox.showinfo("Report", f"Report generated: attendance_report_{month}_{year}.csv")


    month = datetime.now().strftime("%m")
    year = datetime.now().strftime("%Y")
    #return month.strftime("%m") +","+year.strftime("%Y")


# GUI Initialization
root = tk.Tk()
root.title("Attendance Management System")
root.geometry("600x400")

# Header Section (College Name)
header_frame = tk.Frame(root)
header_frame.pack()

college_name_label = tk.Label(header_frame, text="My College Attendance System", font=("Arial", 16))
college_name_label.pack()

# Register Button
register_button = tk.Button(root, text="Register Student", command=register_ui)
register_button.pack()

#Mark Attendance Button
attendance_button = tk.Button(root, text="Mark Attendance", command=mark_attendance)
attendance_button.pack()

month = datetime.now().strftime("%m")
year = datetime.now().strftime("%Y")
# Report Button
report_button = tk.Button(root, text="Generate Monthly Report", command=lambda:generate_report(month,year))
report_button.pack()
root.mainloop()
