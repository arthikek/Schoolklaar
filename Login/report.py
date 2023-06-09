from fpdf import FPDF

pdf=FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(40,10,"Hello World")
pdf.output("simple_demo.pdf")

