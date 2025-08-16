FROM apache/airflow:2.8.1

# Copier le fichier requirements.txt dans l'image
COPY requirements.txt /

# Installer les dépendances Python
RUN pip install --no-cache-dir -r /requirements.txt
