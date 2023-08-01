# Use a imagem base do Python
FROM python:3.9-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos do projeto para o diretório de trabalho no contêiner
COPY . /app/

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta em que a aplicação Flask estará executando (defina a mesma porta que está configurada no app.run())
ENV PORT=5000
EXPOSE $PORT

# Comando para iniciar a aplicação quando o contêiner for executado
CMD ["python", "api/api.py"]