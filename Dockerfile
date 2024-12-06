# Usar una imagen base de Python
FROM python:3.12-slim

RUN mkdir -p /app
# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app
RUN pip install Pillow
RUN pip install django-crispy-forms
# Copiar el archivo de requisitos al directorio de trabajo del contenedor
COPY requirements.txt .
# Instalar las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Copiar el contenido de tu aplicación al directorio de trabajo del contenedor
COPY . /app
COPY manage.py /app/manage.py
COPY .env.example /app/.env


# Exponer el puerto que usa Django
EXPOSE 8000

# Comando para ejecutar la aplicación Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]