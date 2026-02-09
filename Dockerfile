# Estágio 1: Imagem base leve
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências de sistema mínimas (se necessário)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas o arquivo de requisitos primeiro (otimiza o cache do Docker)
# Se você não tem um requirements.txt, rode: pip freeze > requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código
COPY . .

# Criar um usuário não-root para segurança
RUN useradd -m myuser
USER myuser

# Expor a porta que o Flask usa
EXPOSE 5000

# Comando para rodar a aplicação
# Usamos o host 0.0.0.0 para que o container aceite conexões externas
CMD ["python", "app.py"]