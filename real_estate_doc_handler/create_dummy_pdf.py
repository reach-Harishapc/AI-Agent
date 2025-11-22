from pypdf import PdfWriter
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, "RESIDENTIAL LEASE AGREEMENT")
    c.drawString(100, 730, "This Lease Agreement is made between Landlord: John Smith and Tenant: Jane Doe.")
    c.drawString(100, 710, "Property Address: 456 Oak Avenue, Springfield.")
    c.drawString(100, 690, "Term: 12 months beginning February 1, 2025.")
    c.drawString(100, 670, "Rent: The Tenant agrees to pay $1,800 per month.")
    c.drawString(100, 650, "Security Deposit: $1,800.")
    c.drawString(100, 630, "Pets: No pets allowed without prior written consent.")
    c.drawString(100, 610, "Governing Law: This agreement shall be governed by the laws of the State.")
    c.save()

if __name__ == "__main__":
    create_pdf("sample_lease.pdf")
    print("Created sample_lease.pdf")
