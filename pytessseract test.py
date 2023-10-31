# https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe


import pytesseract
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
# Set the path to Tesseract executable (modify this path according to your installation)
pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'

# Open an image file
# image_path = r'C:\Users\sijian\Desktop\aa.png'
# image = Image.open(image_path)



class ROISelector:
    def __init__(self, root, image_path):
        self.root = root
        self.image = Image.open(image_path)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.label = tk.Label(root, image=self.tk_image)
        self.label.pack()
        self.root.bind("<ButtonPress-1>", self.on_click)
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

    def on_click(self, event):
        if self.start_x is None:
            self.start_x = event.x
            self.start_y = event.y
        else:
            self.end_x = event.x
            self.end_y = event.y
            self.crop_roi()

    def crop_roi(self):
        roi_coordinates = (self.start_x, self.start_y, self.end_x, self.end_y)
        roi_image = self.image.crop(roi_coordinates)
        text = pytesseract.image_to_string(roi_image)
        print("Text in ROI: ")
        print(text)
        self.root.quit()


# Perform OCR on the image
# custom_config = r'--oem 3 --psm 6 -l chi_sim'
# custom_config = r'--oem 3 --psm 6 -l eng'

# text = pytesseract.image_to_string(image, config=custom_config)


# # Print the extracted text
# print("Extracted Text:")
# print(text)




# Open a file dialog to select the image
root = tk.Tk()
root.withdraw()  # Hide the main window
file_path = filedialog.askopenfilename(title="Select Image")

# Create the ROISelector object
if file_path:
    root = tk.Tk()
    root.title("Select ROI")
    selector = ROISelector(root, file_path)
    root.mainloop()
