FROM python:latest

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

# Copiar código do projeto
COPY . .

# Rodar migrações e popular banco
RUN cd src/clinica && python manage.py migrate
RUN cd src/clinica && python populate.db
CMD ["cd", "src/clinica", "&&", "python", "manage.py", "runserver", "0.0.0.0:8000"]