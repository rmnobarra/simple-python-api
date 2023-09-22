# Use uma imagem base Python 3.8
FROM python:3.8-slim

# Defina a variável de ambiente para garantir que a saída Python seja enviada diretamente para o terminal sem buffer
ENV PYTHONUNBUFFERED=1

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o arquivo de requisitos e instale as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código-fonte para o diretório de trabalho
COPY . .

# Exponha a porta em que o app roda
EXPOSE 5000

# Comando para executar o aplicativo
CMD ["python", "app.py"]
