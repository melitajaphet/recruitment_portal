import os

import cv2
import numpy as np
from pdf2image import convert_from_path
import pytesseract

def pdf_to_text(pdf_file_path):
    pages = convert_from_path(pdf_file_path, fmt="jpeg")
    pytesseract.pytesseract.tesseract_cmd = r"C:/Users/marcu/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"

    path = pdf_file_path
    output_path = "C:/College/BE_Project/Project/spacy3/uploads/text/"
    filename = pdf_file_path.split("/")[-1].split(".")[0]
    f_name = filename + '.pdf'
    file = open(output_path + filename + ".txt", "w")
    for page in pages:
        text = pytesseract.image_to_string(page)
        file.write(text)
    file.close()

    '''new = path.replace(f_name, '')
    os.chdir(new)
    os.remove(f_name)'''