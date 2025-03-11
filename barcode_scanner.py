import cv2
from pyzbar.pyzbar import decode
import numpy as np

# def BarcodeReader(image): 
      
#     # read the image in numpy array using cv2 
#     img = cv2.imread(image) 
       
#     # Decode the barcode image 
#     detectedBarcodes = decode(img) 
       
#     # If not detected then print the message 
#     if not detectedBarcodes: 
#         print("Barcode Not Detected or your barcode is blank/corrupted!") 
#     else: 
        
#           # Traverse through all the detected barcodes in image 
#         for barcode in detectedBarcodes:   
            
#             # Locate the barcode position in image 
#             (x, y, w, h) = barcode.rect 
              
#             # Put the rectangle in image using  
#             # cv2 to highlight the barcode 
#             cv2.rectangle(img, (x-10, y-10), 
#                           (x + w+10, y + h+10),  
#                           (255, 0, 0), 2) 
              
#             if barcode.data!="": 
                
#             # Print the barcode data 
#                 print(barcode.data) 
#                 print(barcode.type) 
                  
#     #Display the image 
#     cv2.imshow("Image", img) 
#     cv2.waitKey(0) 
#     cv2.destroyAllWindows() 
  
# if __name__ == "__main__": 
#   # Take the image from user 
#     image=r"C:\Users\rakesh.c.p\Pictures\Camera Roll\WIN_20250303_20_24_09_Pro.jpg"
#     BarcodeReader(image) 


#Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame.")
        break

    # Detect barcodes in the frame
    barcodes = decode(frame)

    for barcode in barcodes:
        # Get the data from the barcode
        barcode_data = barcode.data.decode('utf-8')

        print(barcode_data)

        # Get the bounding box of the barcode
        # rect_points = barcode.polygon
        # if len(rect_points) == 4:
        #     pts = rect_points
        # else:
        #     pts = cv2.convexHull(np.array([pt for pt in rect_points], dtype=np.float32))

        # # Draw the bounding box
        # cv2.polylines(frame, [np.int32(pts)], True, (0, 255, 0), 3)

        # # Display the barcode data
        # cv2.putText(frame, barcode_data, (pts[0][0], pts[0][1] - 10),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Print the barcode data in the terminal
        print(f"Barcode Data: {barcode_data}")

    # Display the frame with the detected barcodes
    cv2.imshow('Barcode Scanner', frame)

    # Press 'q' to quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()