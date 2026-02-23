from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_pdf(filename="test.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Page 1
    c.drawString(100, 750, "Hello World! This is a test PDF for OCR.")
    c.drawString(100, 730, "It contains some simple text to verify the service.")
    c.drawString(100, 710, "1234567890")
    c.showPage()
    
    # Page 2
    c.drawString(100, 750, "This is the second page.")
    c.drawString(100, 730, "More text here to test multi-page processing.")
    c.save()
    print(f"Created {filename}")

if __name__ == "__main__":
    create_pdf()
