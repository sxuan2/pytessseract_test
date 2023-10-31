import pytesseract
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'

def on_press(event):
    global start_x, start_y, rect_id
    start_x, start_y = event.x, event.y
    rect_id = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red')

def on_drag(event):
    global rect_id
    canvas.coords(rect_id, start_x, start_y, event.x, event.y)

def on_release(event):
    global end_x, end_y
    end_x, end_y = event.x, event.y
    canvas.coords(rect_id, start_x, start_y, end_x, end_y)
    crop_roi()

def crop_roi():
    global rect_id
    if start_x is not None and start_y is not None and end_x is not None and end_y is not None:
        roi_coordinates = (min(start_x, end_x), min(start_y, end_y), max(start_x, end_x), max(start_y, end_y))
        roi_image = image.crop(roi_coordinates)
        print("Text in ROI: ")
        text = pytesseract.image_to_string(roi_image)
        print(text)
        canvas.delete(rect_id)  # Remove the red rectangle after cropping
        canvas.update()  # Update the canvas to remove the rectangle immediately
        root.after(3000, lambda: root.destroy())  # Close the window after 5 seconds

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
    rect_id = None

    root = tk.Toplevel()
    root.title("Select ROI")
    canvas = tk.Canvas(root, width=image.width, height=image.height)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)

    root.mainloop()
