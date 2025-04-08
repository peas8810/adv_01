import datetime
import time
import functools
import logging

# Configuração do logging (aplicação geral)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def parse_iso_date(date_str: str) -> datetime.date:
    """
    Converte uma string no formato ISO ("YYYY-MM-DD") para um objeto datetime.date.
    Se a conversão falhar (por exemplo, se date_str estiver vazio ou em formato inválido),
    retorna a data de hoje.
    
    Args:
        date_str (str): Data no formato ISO (ex: "2023-10-08").
    
    Returns:
        datetime.date: Objeto de data, ou data de hoje se ocorrer erro.
    """
    try:
        return datetime.date.fromisoformat(date_str)
    except (TypeError, ValueError):
        logger.warning(f"Não foi possível converter '{date_str}' para data, retornando data atual.")
        return datetime.date.today()

def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """
    Decorador para repetir a execução de uma função caso ocorra uma exceção específica.
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
    Decorador para medir e logar o tempo de execução de uma função.
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
    """
    if isinstance(date_obj, (datetime.date, datetime.datetime)):
        return date_obj.strftime("%Y-%m-%d")
    raise ValueError("O argumento não é um objeto de data válido.")

def safe_get(dictionary: dict, key, default=None):
    """
    Retorna o valor associado a uma chave em um dicionário de forma segura.
    """
    return dictionary.get(key, default)
