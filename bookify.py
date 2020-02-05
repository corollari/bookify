from os import system, getcwd, chdir, path
from sys import argv
from PyPDF2 import PdfFileReader, PdfFileWriter
from math import log10, ceil
from tempfile import mkdtemp

def getPageCount(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        return pdf.getNumPages()

def getPageOrder(signatureSize):
    assert (signatureSize%4 == 0), "The size of the signature must be a multiple of 4 (eg: 4, 8, 12, 16, 20...)"
    pageOrder = {}
    for i in range(signatureSize):
        pageOrder[(signatureSize - i//2 - 1) if (i%2 == 0) else i//2] = i + 1
    return pageOrder

def main():
    assert (len(argv) == 3), "You need to provide two arguments, the filename of the pdf and the signature size"
    SIGNATURE_SIZE = int(argv[2])

    INITIAL_WORKING_DIRECTORY = getcwd()
    chdir(mkdtemp(prefix="book-"))
    system("cp %s %s"%(path.join(INITIAL_WORKING_DIRECTORY, argv[1]), path.join(getcwd(), "book.pdf")))

    NUM_PAGES = getPageCount("book.pdf")
    if (NUM_PAGES % 4) != 0:
        print("Padding pdf to make the number of pages a multiple of 4")
        with open("book.pdf", 'rb') as f:
            pdf = PdfFileReader(f)
            newPdf = PdfFileWriter()
            for i in range(NUM_PAGES):
                page = pdf.getPage(i)
                if (getPageOrder(SIGNATURE_SIZE)[i%SIGNATURE_SIZE]+1)%4 <= 1:
                    page.rotateClockwise(180)
                newPdf.addPage(pdf.getPage(i))
            for i in range(4 - (NUM_PAGES % 4)):
                newPdf.addBlankPage()
            with open("book2.pdf", 'wb') as f2:
                newPdf.write(f2)
            system("mv book2.pdf book.pdf")
        NUM_PAGES = getPageCount("book.pdf")
    NUM_DIGITS = ceil(log10(NUM_PAGES))

    system("stapler split book.pdf")
    for i in range(1, NUM_PAGES + 1):
        pages = []
        if (NUM_PAGES - i) < (NUM_PAGES % SIGNATURE_SIZE):
            pages = getPageOrder(NUM_PAGES % SIGNATURE_SIZE)
        else:
            pages = getPageOrder(SIGNATURE_SIZE)
        newpage=((i-1)//SIGNATURE_SIZE)*SIGNATURE_SIZE+pages[(i-1)%SIGNATURE_SIZE]
        system(("mv book_%0"+str(NUM_DIGITS)+"d.pdf pt_%0"+str(NUM_DIGITS)+"d.pdf")%(i, newpage))

    # `pdfnup` can only process up to 1016 pages per call, thus calls must be separated
    for i in range((NUM_PAGES - 1)//1000 + 1):
        system("pdfnup " + " ".join([("pt_%0"+str(NUM_DIGITS)+"d.pdf")%j for j in range(i*1000+1, min((i+1)*1000, NUM_PAGES) + 1)]) + " --outfile final-book%d.pdf &> pdfnup.log"%i)
    system("stapler cat final-book* final-book.pdf") # Merge pdfs

    system("cp final-book.pdf %s"%path.join(INITIAL_WORKING_DIRECTORY, "bookified-" + argv[1]))
