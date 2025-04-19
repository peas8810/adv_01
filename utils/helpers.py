# utils/helpers.py
import datetime
import pandas as pd
from fpdf import FPDF
from docx import Document

def converter_data(data_str):
    if not data_str:
        return datetime.date.today()
    try:
        s = data_str.replace("Z", "")
        if "T" in s:
            return datetime.datetime.fromisoformat(s).date()
        return datetime.date.fromisoformat(s)
    except:
        return datetime.date.today()

def calcular_status_processo(data_prazo, houve_movimentacao, encerrado=False):
    if encerrado:
        return "⚫ Encerrado"
    hoje = datetime.date.today()
    dias = (data_prazo - hoje).days
    if houve_movimentacao:
        return "🔵 Movimentado"
    if dias < 0:
        return "🔴 Atrasado"
    if dias <= 10:
        return "🟡 Atenção"
    return "🟢 Normal"

def exportar_pdf(texto, nome_arquivo="relatorio"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, texto)
    pdf.output(f"{nome_arquivo}.pdf")
    return f"{nome_arquivo}.pdf"

def exportar_docx(texto, nome_arquivo="relatorio"):
    doc = Document()
    doc.add_paragraph(texto)
    doc.save(f"{nome_arquivo}.docx")
    return f"{nome_arquivo}.docx"

def get_dataframe_with_cols(data, columns):
    data_list = data if isinstance(data, list) else [data]
    df = pd.DataFrame(data_list)
    for c in columns:
        if c not in df.columns:
            df[c] = ""
    return df[columns]
