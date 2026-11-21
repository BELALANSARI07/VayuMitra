FROM python:3.11-slim AS builder

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim

RUN groupadd -r vayumitra && useradd -r -g vayumitra vayumitra

WORKDIR /app
COPY --from=builder /install /usr/local
COPY backend/ /app/backend/
COPY data/ /app/data/

ENV PYTHONPATH=/app/backend
USER vayumitra
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
