from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class PDF:
    def __init__(self, filename, pagesize=A4, font="Helvetica", size=4):
        self.filename = filename
        self.c = canvas.Canvas(filename, pagesize=letter)
        self.c.setFont(font, size) 

    def setText(self,x, y, text):
        self.c.drawString(x, y, text)        

    def savePdf(self):
        self.c.save()