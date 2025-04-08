"""
utils.py - Funções utilitárias e decoradores para a aplicação.
"""

import time
import datetime
import functools
import logging

# Configuração do logging (aplicação geral)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """
    Decorador para repetir a execução de uma função caso ocorra alguma exceção específica.

    Args:
        max_attempts (int): Número máximo de tentativas.
        delay (float): Tempo de espera (em segundos) entre as tentativas.
        exceptions (tuple): Exceções que disparam a nova tentativa.

    Returns:
        Função decorada que implementa a lógica de repetição.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(f"Tentativa {attempt} de {max_attempts} para {func.__name__} falhou: {e}")
                    if attempt == max_attempts:
                        logger.error(f"Máximo de tentativas atingido para {func.__name__}.")
                        raise
                    time.sleep(delay)
                    attempt += 1
        return wrapper
    return decorator


def timeit(func):
    """
    Decorador para medir o tempo de execução de uma função e logar o resultado.

    Returns:
        Resultado da função decorada, após a medição do tempo.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        logger.info(f"{func.__name__} executada em {elapsed:.4f} segundos")
        return result
    return wrapper


def format_date(date_obj):
    """
    Formata um objeto datetime ou date em string no formato 'YYYY-MM-DD'.

    Args:
        date_obj (datetime.date ou datetime.datetime): Objeto de data a ser formatado.

    Returns:
        str: Data formatada.
    """
    if isinstance(date_obj, (datetime.date, datetime.datetime)):
        return date_obj.strftime("%Y-%m-%d")
    raise ValueError("O argumento não é um objeto de data válido.")


def safe_get(dictionary: dict, key, default=None):
    """
    Retorna o valor associado a uma chave em um dicionário de forma segura.

    Args:
        dictionary (dict): Dicionário de onde extrair o valor.
        key (qualquer tipo): Chave a ser buscada.
        default (Any, opcional): Valor padrão caso a chave não exista.

    Returns:
        Qualquer: Valor associado à chave ou o valor padrão.
    """
    return dictionary.get(key, default)

