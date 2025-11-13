from abc import ABC, abstractmethod
from datetime import datetime

class InvoiceGenerator(ABC):
    def __init__(self, client_name, items):
        self.client_name = client_name
        self.items = items

    def calculate_total(self):
        jami = 0
        for item in self.items:
            jami += item['price']
        return jami

    @abstractmethod
    def generate_invoice(self, output_path):
        pass

# only for PDFInvoiceGenerator class
from reportlab.lib.pagesizes import letter 
from reportlab.pdfgen import canvas

class PDFInvoiceGenerator(InvoiceGenerator):
    def generate_invoice(self, output_path):
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        
        c.setFont("Helvetica-Bold", 20)
        c.drawString(72, height - 72, "Hisob-faktura")
        
        c.setFont("Helvetica", 12)
        c.drawString(72, height - 100, f"Mijoz: {self.client_name}")
        c.drawString(72, height - 115, f"Yaratilgan sana: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        c.drawString(72, height - 140, "Mahsulotlar:")
        y = height - 160
        for item in self.items:
            c.drawString(80, y, f"{item['name']} - ${item['price']:.2f}")
            y -= 20
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, y - 20, f"Jami summa: ${self.calculate_total():.2f}")
        
        c.save()


if __name__ == '__main__':
    items = [
        {'name': 'Laptop', 'price': 700},
        {'name': 'Smartphone', 'price': 500},
        {'name': 'Charger', 'price': 50}
    ]

    client_name =  'Ehsmat'

    pdf_generator = PDFInvoiceGenerator(client_name, items)
    pdf_generator.generate_invoice('faktura.pdf')

    print('PDF fakturasi muvaffaqiyatli yaratildi!')

