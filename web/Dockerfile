FROM python:3.12-slim

COPY ./web /app
WORKDIR /app

# Fix base_url to use environment variable
RUN sed -i "s|base_url = 'http://127.0.0.1:8001'|base_url = os.environ.get('API_BASE_URL', 'http://api:8001')|g" /app/src/clinica/mysite/views.py || true
RUN sed -i "s|base_url = 'http://localhost:8001'|base_url = os.environ.get('API_BASE_URL', 'http://api:8001')|g" /app/src/clinica/mysite/views.py || true

RUN pip install uv

RUN uv sync

# Expor porta
EXPOSE 8000

# Comando para iniciar (migrações devem ser feitas manualmente ou via entrypoint)
CMD ["sh", "-c", "cd /app/src/clinica && uv run python manage.py runserver 0.0.0.0:8000"]