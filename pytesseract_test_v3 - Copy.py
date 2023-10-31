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

# def crop_roi():
#     global rect_id
#     if start_x is not None and start_y is not None and end_x is not None and end_y is not None:
#         roi_coordinates = (min(start_x, end_x), min(start_y, end_y), max(start_x, end_x), max(start_y, end_y))
#         roi_image = image.crop(roi_coordinates)
#         print("Text in ROI: ")
#         custom_config = r'--oem 3 --psm 6 outputbase digits'  # Set OCR mode to recognize only digits
#         text = pytesseract.image_to_string(roi_image, config=custom_config)
#         print(text)
#         canvas.delete(rect_id)  # Remove the red rectangle after cropping
#         canvas.update()  # Update the canvas to remove the rectangle immediately
#         root.destroy()  # Close the window after 5 seconds
#         root.quit()

def crop_roi():
    global rect_id
    if start_x is not None and start_y is not None and end_x is not None and end_y is not None:
        # Map coordinates back to the original image size
        original_start_x = start_x #int(start_x * 2)  # Multiply by 2 because the image was resized to half
        original_start_y = start_y# int(start_y * 2)  # Multiply by 2 because the image was resized to half
        original_end_x = end_x # int(end_x * 2)  # Multiply by 2 because the image was resized to half
        original_end_y = end_y#int(end_y * 2)  # Multiply by 2 because the image was resized to half
        
        roi_coordinates = (min(original_start_x, original_end_x), min(original_start_y, original_end_y),
                            max(original_start_x, original_end_x), max(original_start_y, original_end_y))
        roi_image = original_image.crop(roi_coordinates)
        print("Text in ROI: ")
        custom_config = r'--psm 6 -l chi_sim'
        text = pytesseract.image_to_string(roi_image, config=custom_config)  # Set appropriate OCR configuration
        print(text)
        canvas.delete(rect_id)  # Remove the red rectangle after cropping
        canvas.update()  # Update the canvas to remove the rectangle immediately
        # root.after(3000, lambda: root.destroy())  # Close the window after 5 seconds
        root.destroy()
        root.quit()

        
        
# Open a file dialog to select the image
root = tk.Tk()
root.withdraw()  # Hide the main window
file_path = filedialog.askopenfilename()

if file_path:
    
    original_image = Image.open(file_path)
    original_width, original_height = original_image.size
    new_width = original_width
    new_height = original_height

    # Resize the image to fit half of the screen
    resized_image = original_image.resize((new_width, new_height))
    
    # image = Image.open(file_path)
    tk_image = ImageTk.PhotoImage(resized_image)

    # Store the tk_image object in a list to prevent it from being garbage collected
    image_references = []  
    image_references.append(tk_image)

    start_x, start_y, end_x, end_y = None, None, None, None
    rect_id = None

    root = tk.Toplevel()
    root.title("Select ROI")
    canvas = tk.Canvas(root, width=new_width, height=new_height)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)

    root.mainloop()
