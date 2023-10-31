import pytesseract
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'

def on_click(event):
    global start_x, start_y, end_x, end_y
    if start_x is None:
        start_x, start_y = event.x, event.y
    else:
        end_x, end_y = event.x, event.y
        crop_roi()

def crop_roi():
    if start_x is not None and start_y is not None:
        roi_coordinates = (start_x, start_y, end_x, end_y)
        roi_image = image.crop(roi_coordinates)
        print(start_x, start_y, end_x, end_y)
        text = pytesseract.image_to_string(roi_image)
        print("Text in ROI: ")
        print(text)
        root.destroy()
        root.quit()

# Open a file dialog to select the image
root = tk.Tk()
root.withdraw()  # Hide the main window
file_path = filedialog.askopenfilename()

if file_path:
    image = Image.open(file_path)
    tk_image = ImageTk.PhotoImage(image)

    # Store the tk_image object in a list to prevent it from being garbage collected
    image_references = []  
    image_references.append(tk_image)

    start_x, start_y, end_x, end_y = None, None, None, None

    root = tk.Toplevel()
    root.title("Select ROI")
    label = tk.Label(root, image=tk_image)
    label.pack()

    root.bind("<ButtonPress-1>", on_click)
    root.mainloop()
