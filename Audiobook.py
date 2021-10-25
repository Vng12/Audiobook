import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
from pdf2image import convert_from_path
import pyttsx3

# function to convert image to text


def img_to_text(_file):
    img = cv2.imread(_file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    fig = plt.figure(figsize=[10, 10])
    height, width, channel = img.shape
    plt.imshow(img)
    plt.show()

    # Let's do some image processing for better OCR
    # converting image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    fig = plt.figure(figsize=[10, 10])

    plt.imshow(gray, cmap='gray', vmin=0, vmax=255)
    plt.show()

    # adaptive thresholding
    adaptive_threshold = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)
    fig = plt.figure(figsize=[10, 10])
    plt.imshow(adaptive_threshold, cmap='gray', vmin=0, vmax=255)
    plt.show()

    text = pytesseract.image_to_string(adaptive_threshold)
    print(text)
    string_to_voice(text)

    print(type(img))
    print(height, width, channel)

    # the output of OCR can be saved in a file
    file = open('output.txt', 'a')  # file opened in append mode
    file.write(text)
    file.close()


def string_to_voice(text):
    engine = pyttsx3.init()
    engine. setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


# Storing file path in variable '_file'
_file = input("enter relative path of file:")

# Checking whether file is pdf or img and if pdf convert it to image first
if _file.endswith(".pdf"):
    pages = convert_from_path(_file, 500)  # Store pages in a variable

    image_counter = 1

    # iterating over the pages and saving them as images
    for page in pages:

        # Declaring filename for each page of PDF as JPG
        # For each page, filename will be:
        # PDF page 1 -> page_1.jpg
        filename = "page_"+str(image_counter)+".jpg"

        # Save the image of the page in system
        page.save(filename, 'JPEG')

        # Increment the counter to update filename
        image_counter = image_counter + 1

    filelimit = image_counter-1  # actual number of pages

    for i in range(1, filelimit + 1):

        # Set filename to recognize text from
        # Again, these files will be:
        # page_1.jpg
        # page_2.jpg
        # ....
        # page_n.jpg
        filename = "page_"+str(i)+".jpg"

        img_to_text(filename)
else:
    img_to_text(_file)
