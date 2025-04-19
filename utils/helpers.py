import datetime
import pandas as pd
from fpdf import FPDF
from docx import Document

# Converte string ISO em datetime.date
def converter_data(data_str):
    if not data_str:
        return datetime.date.today()
    try:
        data_str = data_str.replace("Z", "")
        if "T" in data_str:
            return datetime.datetime.fromisoformat(data_str).date()
        return datetime.date.fromisoformat(data_str)
    except Exception:
        return datetime.date.today()

# Calcula status de um processo baseado no prazo e movimentação
def calcular_status_processo(data_prazo, houve_movimentacao, encerrado=False):
    if encerrado:
        return "⚫ Encerrado"
    hoje = datetime.date.today()
    dias_restantes = (data_prazo - hoje).days
    if houve_movimentacao:
        return "🔵 Movimentado"
    if dias_restantes < 0:
        return "🔴 Atrasado"
    if dias_restantes <= 10:
        return "🟡 Atenção"
    return "🟢 Normal"

# Exporta texto simples para PDF
def exportar_pdf(texto, nome_arquivo="relatorio"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, texto)
    pdf.output(f"{nome_arquivo}.pdf")
    return f"{nome_arquivo}.pdf"

# Exporta texto simples para DOCX
def exportar_docx(texto, nome_arquivo="relatorio"):
    doc = Document()
    doc.add_paragraph(texto)
    doc.save(f"{nome_arquivo}.docx")
    return f"{nome_arquivo}.docx"

# Cria DataFrame com colunas fixas, mesmo se ausentes
def get_dataframe_with_cols(data, columns):
    data_list = data if isinstance(data, list) else [data]
    df = pd.DataFrame(data_list)
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    return df[columns]
