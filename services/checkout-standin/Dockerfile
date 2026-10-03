FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir "fastapi>=0.115" "uvicorn[standard]>=0.30"

COPY src/checkout_standin ./checkout_standin

EXPOSE 8081

CMD ["python", "-m", "uvicorn", "checkout_standin.main:app", "--host", "0.0.0.0", "--port", "8081"]
