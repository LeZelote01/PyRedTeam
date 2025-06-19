# Base image Python 3.10 slim
FROM python:3.10-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie et installe les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code source
COPY . .

# Variables d'environnement pour la sécurité
# Désactive la mise en buffer
ENV PYTHONUNBUFFERED=1
# Empêche la création de .pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Point d'entrée principal
ENTRYPOINT ["python", "main.py"]