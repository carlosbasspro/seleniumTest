# Use a imagem oficial do Python como base
FROM python:3.11-slim

# Instale dependências necessárias para o Selenium, navegador Chrome e Chromedriver
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium \
    && apt-get clean

# Baixe e instale o Chromedriver compatível com a versão do Chromium
RUN wget -q "https://chromedriver.storage.googleapis.com/130.0.6723.116/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm chromedriver_linux64.zip


# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo Python para o contêiner
COPY main.py .

# Copie e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta 10000
EXPOSE 10000

# Comando para rodar o script
CMD ["python", "main.py"]
