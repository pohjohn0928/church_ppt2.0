import os
import glob

from PIL import Image


def delete_files():
    pptx_files = glob.glob('*.{}'.format('pptx'))
    docx_files = glob.glob('*.{}'.format('docx'))

    for docx_file, pptx_file in zip(docx_files, pptx_files):
        os.remove(docx_file)
        os.remove(pptx_file)


def replace_images():
    im1 = Image.open(r"1.jpeg")
    im1.save('2.png')


if __name__ == '__main__':
    replace_images()