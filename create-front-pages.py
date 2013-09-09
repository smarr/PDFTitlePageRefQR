#!/usr/bin/env python
import bib
import sys
import os
import urllib
from subprocess import call
from PyPDF2 import PdfFileWriter, PdfFileReader

bibfile_name = sys.argv[1]

DIR = os.path.abspath(os.path.dirname(__file__))


def load_bibtex(bibfile_name):
    with open(bibfile_name, 'r') as bibfile:
        content = bibfile.read()
        bibtex = bib.Bibparser(content)
        bibtex.parse()
        return bibtex.records

def download_pdf(bibentry, entry_name):
    if 'pdf' not in bibentry:
        print "ERROR: bibentry %s does not define a pdf field. Cannot download file." % entry_name
        return None
    else:
        if not os.path.exists("%s.original.pdf" % entry_name):
            print "Downloading %s." % bibentry['pdf']
            urllib.urlretrieve(bibentry['pdf'], "%s.original.pdf" % entry_name)
        return bibentry['pdf']

def create_overlay(entry_name, url, bibfile_name):
    input1 = PdfFileReader(open("%s.original.pdf" % entry_name, "rb"))
    page1  = input1.getPage(0)
    width  = page1.mediaBox.getUpperRight_x()
    height = page1.mediaBox.getUpperRight_y()
    
    with open('%s/template.tex' % DIR, 'r') as tex_template:
        tpl = tex_template.read()
        tpl = tpl.replace("BIBKEY", entry_name)
        tpl = tpl.replace("PDFURL", url)
        tpl = tpl.replace("BIBFILE", bibfile_name)
        tpl = tpl.replace("PAPERWIDTH",  "%dpt" % width)
        tpl = tpl.replace("PAPERHEIGHT", "%dpt" % height)
        
        with open("overlay_tmp.tex", "w") as tex_file:
            tex_file.write(tpl)
    
        with open("overlay_tmp.aux", "w") as tex_file:
            tex_file.write("""\\relax
\\citation{%s}
\\bibstyle{plainnat}
\\bibdata{%s}
""" % (entry_name, bibfile_name.replace(".bib", "")))

    call(["bibtex", "overlay_tmp"])
    call(["pdflatex", "-shell-escape", "overlay_tmp.tex"])

def create_overlayed_page(entry_name):
    output = PdfFileWriter()
    input1 = PdfFileReader(open("%s.original.pdf" % entry_name, "rb"))
    watermark = PdfFileReader(open("overlay_tmp.pdf", "rb"))

    page1 = input1.getPage(0)
    page1_watermark = watermark.getPage(0)
    
    page1.mergePage(page1_watermark)
    output.addPage(page1)

    outputStream = file("%s.with-ref.pdf" % entry_name, "wb")
    output.write(outputStream)

## Main

records = load_bibtex(bibfile_name)
    
for entry in records:
    print entry
    url = download_pdf(records[entry], entry)
    if url:
        create_overlay(entry, url, bibfile_name)
        create_overlayed_page(entry)




