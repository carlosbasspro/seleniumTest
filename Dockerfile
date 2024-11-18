# Use a imagem oficial do Python como base
FROM python:3.11-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo Python para o contêiner
COPY main.py .

# Instale as dependências, se houver um requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta 10000
EXPOSE 10000

# Comando para rodar o script no host 0.0.0.0 e porta 10000
CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "10000"]
