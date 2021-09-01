import os
import glob

pptx_files = glob.glob('*.{}'.format('pptx'))
docx_files = glob.glob('*.{}'.format('docx'))

for docx_file, pptx_file in zip(docx_files, pptx_files):
    os.remove(docx_file)
    os.remove(pptx_file)
