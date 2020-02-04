# Bookify
> Transform pdf files into books for double-sided printing

## Preparing the book: Layout
1. Use Calibre to convert the book to .docx format
2. Modify the resulting docx, applying the following changes:
	- Add title page + empty page (usually the second page is empty)
	- Maybe add extra pages such as index or dedication
	- Add page numbering (make sure to make it start only after the special pages such as index/dedication)
	- Make sure that every new chaper is in an odd page (this is to make it so that the first page of every chaper appears on the left)
	- Make the total number of pages a multiple of 4 (if it's not, empty pages will be added at the end to pad it)
	- It's recommended to set the size of the document to A5 and use generous margins
3. Export the document into a pdf (we will refer to this pdf as `formatted.pdf`)

## Build book
### Install pdfjam
```
sudo apt-get install pdfjam # Ubuntu
sudo dnf install texlive-pdfjam-bin # Fedora
```

### Build
```
pip install bookify
bookify formatted.pdf
```

## Appendix: Getting books from wattpad
```
pip install FanFicFare
fanficfare https://www.wattpad.com/story/31983802-kaylor-the-timeline
```
Use URLs like:
 * https://www.wattpad.com/story/9999999-story-title
 * https://www.wattpad.com/story/9999999
 * https://www.wattpad.com/9999999-chapter-is-ok-too
