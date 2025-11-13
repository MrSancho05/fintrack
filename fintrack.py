from abc import ABC, abstractmethod

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
        

class PDFInvoiceGenerator(InvoiceGenerator):
    pass

class ExcelInvoiceGenerator(InvoiceGenerator):
    pass

class HTMLInvoiceGenerator(InvoiceGenerator):
    pass