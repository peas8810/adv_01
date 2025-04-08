import datetime
import time
import requests
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from fpdf import FPDF
from docx import Document

# Dados do sistema - Em um cenário real, isso viria de um banco de dados
USERS = {
    "dono": {"senha": "dono123", "papel": "owner"},
    "gestor1": {"senha": "gestor123", "papel": "manager", "escritorio": "Escritorio A"},
    "adv1": {"senha": "adv123", "papel": "lawyer", "escritorio": "Escritorio A", "area": "Cível"},
}

def login(usuario: str, senha: str) -> dict | None:
    """
    Autentica o usuário no sistema.

    Args:
        usuario (str): Nome do usuário.
        senha (str): Senha do usuário.

    Returns:
        dict or None: Dados do usuário autenticado ou None se a autenticação falhar.
    """
    user = USERS.get(usuario)
    return user if user and user["senha"] == senha else None


def calcular_status_processo(data_prazo: datetime.date, houve_movimentacao: bool) -> str:
    """
    Calcula o status do processo com base na data de prazo e na movimentação recente.

    Args:
        data_prazo (datetime.date): Data limite (prazo) do processo.
        houve_movimentacao (bool): Indica se houve movimentação recente no processo.

    Returns:
        str: Status do processo representado por símbolos e texto.
    """
    hoje = datetime.date.today()
    dias_restantes = (data_prazo - hoje).days
    if houve_movimentacao:
        return "🔵 Movimentado"
    elif dias_restantes < 0:
        return "🔴 Atrasado"
    elif dias_restantes <= 10:
        return "🟡 Atenção"
    else:
        return "🟢 Normal"


def consultar_movimentacoes_simples(numero_processo: str) -> list:
    """
    Consulta movimentações processuais simuladas por meio de scraping.

    Args:
        numero_processo (str): Número do processo a ser consultado.

    Returns:
        list: Lista com as movimentações encontradas ou mensagem padrão caso nenhuma seja encontrada.
    """
    url = f"https://esaj.tjsp.jus.br/cpopg/show.do?processo.codigo={numero_processo}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    andamentos = soup.find_all("tr", class_="fundocinza1")
    return [a.get_text(strip=True) for a in andamentos[:5]] if andamentos else ["Nenhuma movimentação encontrada"]


def exportar_pdf(texto: str, nome_arquivo: str = "peticao") -> str:
    """
    Exporta um texto para um arquivo PDF.

    Args:
        texto (str): Conteúdo que será exportado.
        nome_arquivo (str, optional): Nome base do arquivo PDF. Default é "peticao".

    Returns:
        str: Caminho do arquivo PDF gerado.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, texto)
    pdf_filename = f"{nome_arquivo}.pdf"
    pdf.output(pdf_filename)
    return pdf_filename


def exportar_docx(texto: str, nome_arquivo: str = "peticao") -> str:
    """
    Exporta um texto para um arquivo DOCX.

    Args:
        texto (str): Conteúdo que será exportado.
        nome_arquivo (str, optional): Nome base do arquivo DOCX. Default é "peticao".

    Returns:
        str: Caminho do arquivo DOCX gerado.
    """
    doc = Document()
    doc.add_paragraph(texto)
    doc_filename = f"{nome_arquivo}.docx"
    doc.save(doc_filename)
    return doc_filename


def gerar_relatorio_pdf(dados: list, nome_arquivo: str = "relatorio") -> str:
    """
    Gera um relatório em PDF a partir dos dados informados.

    Args:
        dados (list): Lista de dicionários com dados (ex.: informações de processos).
        nome_arquivo (str, optional): Nome base do arquivo PDF. Default é "relatorio".

    Returns:
        str: Caminho do arquivo PDF gerado.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Título do relatório
    pdf.cell(200, 10, txt="Relatório de Processos", ln=1, align='C')
    pdf.ln(10)
    
    # Cabeçalho da tabela
    col_widths = [40, 30, 50, 30, 40]
    headers = ["Cliente", "Número", "Área", "Status", "Responsável"]
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, txt=header, border=1)
    pdf.ln()
    
    # Processa cada linha do relatório
    for processo in dados:
        prazo_str = processo.get("prazo", datetime.date.today().isoformat())
        prazo = datetime.date.fromisoformat(prazo_str)
        status = calcular_status_processo(prazo, processo.get("houve_movimentacao", False))
        cols = [
            processo.get("cliente", ""),
            processo.get("numero", ""),
            processo.get("area", ""),
            status,
            processo.get("responsavel", "")
        ]
        for i, col in enumerate(cols):
            pdf.cell(col_widths[i], 10, txt=str(col), border=1)
        pdf.ln()
    
    pdf_filename = f"{nome_arquivo}.pdf"
    pdf.output(pdf_filename)
    return pdf_filename


def aplicar_filtros(dados: list, filtros: dict) -> list:
    """
    Aplica filtros aos dados com base nos critérios fornecidos.

    Args:
        dados (list): Lista de dicionários (ex.: registros de cadastros ou processos).
        filtros (dict): Dicionário de filtros com o formato {campo: valor}.

    Returns:
        list: Dados filtrados conforme os critérios.
    """
    resultados = dados.copy()
    for campo, valor in filtros.items():
        if valor:
            if campo == "data_inicio":
                resultados = [
                    r for r in resultados
                    if datetime.date.fromisoformat(r["data_cadastro"][:10]) >= valor
                ]
            elif campo == "data_fim":
                resultados = [
                    r for r in resultados
                    if datetime.date.fromisoformat(r["data_cadastro"][:10]) <= valor
                ]
            else:
                resultados = [
                    r for r in resultados
                    if str(valor).lower() in str(r.get(campo, "")).lower()
                ]
    return resultados


def verificar_movimentacao_manual(numero_processo: str) -> list:
    """
    Realiza uma verificação manual de movimentação processual,
    simulando o tempo de consulta e retornando as movimentações encontradas.

    Args:
        numero_processo (str): Número do processo a ser verificado.

    Returns:
        list: Lista de movimentações ou mensagem padrão caso nenhuma seja encontrada.
    """
    with st.spinner(f"Verificando movimentações para o processo {numero_processo}..."):
        time.sleep(2)  # Simula o tempo de consulta
        movimentacoes = consultar_movimentacoes_simples(numero_processo)
    return movimentacoes


def obter_processos_por_usuario(papel: str, escritorio: str = None, area: str = None, processos: list = None) -> list:
    """
    Filtra os processos de acordo com as permissões do usuário.

    Args:
        papel (str): Papel do usuário (ex.: "owner", "manager", "lawyer").
        escritorio (str, optional): Escritório do usuário.
        area (str, optional): Área de atuação (para advogados).
        processos (list, optional): Lista de processos. Se não for fornecida, deverá ser obtida via integração.

    Returns:
        list: Lista de processos filtrados conforme as permissões.
    """
    processos = processos or []
    
    if papel == "owner":
        return processos
    elif papel == "manager":
        return [p for p in processos if p.get("escritorio") == escritorio]
    elif papel == "lawyer":
        return [
            p for p in processos
            if p.get("escritorio") == escritorio and p.get("area") == area
        ]
    else:
        return []

