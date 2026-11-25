FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd --system --create-home cripto
COPY --chown=cripto:cripto . .
USER cripto
ENV APP_MODULE=servidor:app
CMD ["sh", "-c", "exec python -m uvicorn \"$APP_MODULE\" --host 0.0.0.0 --port \"${PORT:-8080}\""]
