import re
from PIL import Image
import pytesseract

# Path to the Tesseract executable (change this according to your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to extract serial number from ID card image using regular expressions
def extract_serial_number(image_path):
    # Open the image using Pillow
    image = Image.open(image_path)
    
    # Perform OCR on the entire image
    extracted_text = pytesseract.image_to_string(image)
    
    # Regular expression pattern for matching 18-digit numbers or 17-digit numbers followed by a letter
    serial_number_pattern = r'\b\d{17}([A-Za-z]|\d{1})\b|\b\d{18}\b'
    
    # Search for the pattern in the extracted text
    matches = re.findall(serial_number_pattern, extracted_text)
    
    # Extract the first match as the serial number
    if matches:
        serial_number = matches[0][0] if matches[0][0] else matches[0][1]
        return serial_number
    else:
        return None

# Example usage
image_path = 'path/to/your/id_card_image.jpg'  # Replace this with the path to your ID card image
serial_number = extract_serial_number(image_path)

if serial_number:
    print('Serial Number:', serial_number)
else:
    print('Serial number not found.')
