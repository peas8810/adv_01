import requests
from bs4 import BeautifulSoup


def consultar_movimentacoes_simples(numero_processo):
    """
    Busca as últimas movimentações de um processo no site do ESAJ (TJSP).
    Retorna lista de strings ou mensagem de erro.
    """
    url = f"https://esaj.tjsp.jus.br/cpopg/show.do?processo.codigo={numero_processo}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        andamentos = soup.find_all("tr", class_="fundocinza1")
        if andamentos:
            return [a.get_text(strip=True) for a in andamentos[:5]]
        return ["Nenhuma movimentação encontrada"]
    except Exception:
        return ["Erro ao consultar movimentações"]
