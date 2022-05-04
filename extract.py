import fitz
from PIL import Image
import io
import os
from os.path import isfile, join, isdir, splitext
import shutil

def pdf_to_text(file_path):
    with fitz.open(file_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        return text

def text_to_txt(text, destination):
    f = open(destination, "w+")
    f.write(text)
    f.close()
    return

def extract_image(filename, destination):
    with fitz.open(filename) as my_pdf_file:
        for page_number in range(1, len(my_pdf_file)+1):
            page = my_pdf_file[page_number-1]
            for image_number, image in enumerate(page.getImageList(), start=1):
                xref_value = image[0]
                base_image = my_pdf_file.extractImage(xref_value)
                image_bytes = base_image["image"]
                ext = base_image["ext"]
                image = Image.open(io.BytesIO(image_bytes))
                image.save(open(destination+"/"+f"Page{page_number}Image{image_number}.{ext}", "wb"))
    return


current = os.getcwd()
ext_dir = current+"/extract"
files = [f for f in os.listdir(ext_dir) if isfile(join(ext_dir, f))]
for file in files:
    n, e = splitext(file)
    if e=='.pdf':
        source = join(ext_dir, file)
        destination = join(ext_dir, n)
        if isdir(destination):
            shutil.rmtree(destination)
        os.mkdir(destination)
        text = pdf_to_text(source)
        text_to_txt(text, destination+"/"+n+".txt")
        extract_image(source, destination)