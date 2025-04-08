# Use uma imagem leve com Python 3.9
FROM python:3.9-slim

# Define o diretório de trabalho na imagem
WORKDIR /app

# Copia o arquivo de dependências e instala os pacotes necessários
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante do código para a imagem
COPY . .

# Expõe a porta que o Streamlit usará
EXPOSE 8501

# Configura variáveis de ambiente específicas do Streamlit (opcional)
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ENABLE_CORS=false

# Comando para iniciar a aplicação
CMD ["streamlit", "run", "main.py", "--server.enableCORS", "false", "--server.port", "8501"]
