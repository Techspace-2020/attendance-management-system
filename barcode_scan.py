import mysql.connector
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="techspace@123"
# )

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Set the width of the frame
cap.set(4, 480)  # Set the height of the frame

# Read the authorized barcode data from file
with open('myData.text') as f:
    myDataList = f.read().splitlines()

barcode_found = False  # To ensure we only process the barcode once

while True:
    success, img = cap.read()

    if not success:
        print("Failed to grab frame.")
        break

    # Decode the barcodes in the image
    barcodes = decode(img)

    # Process the first barcode found
    if not barcode_found and barcodes:  # Only process if barcode is detected and not yet processed
        barcode = barcodes[0]  # Process the first barcode (assuming only one barcode is visible)
        barcode_data = barcode.data.decode('utf-8')

        if barcode_data in myDataList:
            myOutput = "Authorized"
            myColor = (0, 255, 0)  # Green color
        else:
            myOutput = "Unauthorized"
            myColor = (0, 0, 255)  # Red color

        # Get the bounding box of the barcode
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, myColor, 5)

        pts2 = barcode.rect

        # Display the status (Authorized/Unauthorized)
        cv2.putText(img, myOutput, (pts2[0], pts2[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor, 2)

        # Print the barcode data in the terminal
        print(f"Barcode Data: {barcode_data}")

        # Set the flag to prevent further barcode processing
        barcode_found = True
        

    # Display the frame with the detected barcode
    cv2.imshow('Barcode Scanner', img)

    # Press 'q' to quit the program or continue to process other frames
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
