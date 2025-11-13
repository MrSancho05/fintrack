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

from openpyxl import Workbook
class ExcelInvoiceGenerator(InvoiceGenerator):
    def generate_invoice(self, output_path):
        wb = Workbook()
        ws = wb.active
        ws.title = 'Invoice'

        ws.append(['Mahsulot nomi', 'Narxi'])

        for item in self.items:
            ws.append([item['name'], item['price']])

        ws.append([])

        ws.append(['Jami summa: ', self.calculate_total()])
        ws.append(['Yaratilgan vaqt : ', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

        wb.save(output_path)

class HTMLInvoiceGenerator(InvoiceGenerator):
    def generate_invoice(self, output_path):
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Hisob-faktura</title>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>Hisob-faktura</h1>
            <p>Mijoz: {self.client_name}</p>
            <p>Yaratilgan sana: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <h2>Mahsulotlar</h2>
            <ul>
        """

        for item in self.items:
            html_content += f"<li>{item['name']} - ${item['price']:.2f}</li>"

        html_content += f"""
        </ul>
            <h3>Jami summa: ${self.calculate_total():.2f}</h3>
        </body>
        </html>
        """

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

if __name__ == '__main__':
    items = [
        {'name': 'Laptop', 'price': 700},
        {'name': 'Smartphone', 'price': 500},
        {'name': 'Charger', 'price': 50}
    ]

    client_name =  'Ehsmat'

    pdf_generator = PDFInvoiceGenerator(client_name, items)
    pdf_generator.generate_invoice('faktura.pdf')

    excel_generator = ExcelInvoiceGenerator(client_name, items)
    excel_generator.generate_invoice('faktura.xlsx')

    html_generator = HTMLInvoiceGenerator(client_name, items)
    html_generator.generate_invoice('faktura.html')

    print('Barcha fakturalar yaratildi)')

