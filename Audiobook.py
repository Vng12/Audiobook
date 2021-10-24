import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
from pdf2image import convert_from_path

# function to convert image to text


def img_to_text(_file):
    img = cv2.imread(_file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    fig = plt.figure(figsize=[10, 10])
    height, width, channel = img.shape
    plt.imshow(img)
    plt.show()

    text = pytesseract.image_to_string(img)
    print(text)
    # Let's do some image processing for better OCR

    img = cv2.resize(img, None, fx=.5, fy=0.5)  # resizing the image
    print(img.shape)
    fig = plt.figure(figsize=[10, 10])
    plt.imshow(img)
    plt.show()

    # converting image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    fig = plt.figure(figsize=[10, 10])
    # while plotting grayscale image with matplotlib, cmap should be defined
    plt.imshow(gray, cmap='gray', vmin=0, vmax=255)
    plt.show()
    text1 = pytesseract.image_to_string(gray)
    print(text1)

    # lets try adaptive thresholding
    adaptive_threshold = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)
    fig = plt.figure(figsize=[10, 10])
    plt.imshow(adaptive_threshold, cmap='gray', vmin=0, vmax=255)
    plt.show()

    text2 = pytesseract.image_to_string(adaptive_threshold)
    print(text2)

    print(type(img))
    print(height, width, channel)

    # the output of OCR can be saved in a file in necessary
    file = open('output.txt', 'a')  # file opened in append mode
    file.write(text2)
    file.close()


# Storing file path in variable '_file'
_file = "UT-II Guidelines for Students.pdf"

# Checking whether file is pdf or img and if pdf convert it to image first
if _file.endswith(".pdf"):
    pages = convert_from_path(_file, 500)  # Store pages in a variable

    image_counter = 1

    # iterating over the pages and saving them as images
    for page in pages:

        # Declaring filename for each page of PDF as JPG
        # For each page, filename will be:
        # PDF page 1 -> page_1.jpg
        # PDF page 2 -> page_2.jpg
        # PDF page 3 -> page_3.jpg
        # ....
        # PDF page n -> page_n.jpg
        filename = "page_"+str(image_counter)+".jpg"

        # Save the image of the page in system
        page.save(filename, 'JPEG')

        # Increment the counter to update filename
        image_counter = image_counter + 1

    filelimit = image_counter-1  # actual number of pages

    # Creating a text file to write the output
    outfile = "out_text.txt"

    f = open(outfile, "a")

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
