from os import system, getcwd, chdir, path
from sys import argv
from PyPDF2 import PdfFileReader, PdfFileWriter
from math import log10, ceil
from tempfile import mkdtemp

def getPageCount(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        return pdf.getNumPages()

def main():
    assert (len(argv) == 2), "You need to provide a single argument, the filename of the pdf"

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
                newPdf.addPage(pdf.getPage(i))
            for i in range(4 - (NUM_PAGES % 4)):
                newPdf.addBlankPage()
            with open("book2.pdf", 'wb') as f2:
                newPdf.write(f2)
            system("mv book2.pdf book.pdf")
        NUM_PAGES = getPageCount("book.pdf")
    NUM_DIGITS = ceil(log10(NUM_PAGES))

    rearranging = {
            4: [2, 3, 4, 1],
            8: [2, 3, 6, 7, 8, 5, 4, 1],
            12: [2, 3, 6, 7, 10, 11, 12, 9, 8, 5, 4, 1],
            16: [2, 3, 6, 7, 10, 11, 14, 15, 16, 13, 12, 9, 8, 5, 4, 1],
            20: [2, 3, 6, 7, 10, 11, 14, 15, 18, 19, 20, 17, 16, 13, 12, 9, 8, 5, 4, 1]
            }

    system("stapler split book.pdf")
    for i in range(1, NUM_PAGES + 1):
        pages = []
        if (NUM_PAGES - i) < (NUM_PAGES % 20):
            pages = rearranging[NUM_PAGES % 20]
        else:
            pages = rearranging[20]
        newpage=((i-1)//20)*20+pages[(i-1)%20]
        system(("mv book_%0"+str(NUM_DIGITS)+"d.pdf pt_%0"+str(NUM_DIGITS)+"d.pdf")%(i, newpage))

    # `pdfnup` can only process up to 1016 pages per call, thus calls must be separated
    for i in range((NUM_PAGES - 1)//1000 + 1):
        system("pdfnup " + " ".join([("pt_%0"+str(NUM_DIGITS)+"d.pdf")%j for j in range(i*1000+1, min((i+1)*1000, NUM_PAGES) + 1)]) + " --outfile final-book%d.pdf"%i)
    system("stapler cat final-book* final-book.pdf") # Merge pdfs

    system("cp final-book.pdf %s"%path.join(INITIAL_WORKING_DIRECTORY, "bookified-" + argv[1]))
