# https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe


import pytesseract
from PIL import Image

# Set the path to Tesseract executable (modify this path according to your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Open an image file
image_path = r'B:\dd.png'
image = Image.open(image_path)

# Perform OCR on the image
custom_config = r'--oem 3 --psm 6 -l chi_sim'
text = pytesseract.image_to_string(image, config=custom_config)


# Print the extracted text
print("Extracted Text:")
print(text)
