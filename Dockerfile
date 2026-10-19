# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости для компиляции (нужно для asyncpg, bcrypt и т.д.)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY auth_service/requirements.txt auth_service/requirements.txt
COPY order_service/requirements.txt order_service/requirements.txt
COPY notification_service/requirements.txt notification_service/requirements.txt

# Устанавливаем зависимости (упрощенно для всех сразу)
RUN pip install --no-cache-dir -r auth_service/requirements.txt \
    && pip install --no-cache-dir -r order_service/requirements.txt \
    && pip install --no-cache-dir -r notification_service/requirements.txt

COPY . .

# По умолчанию команда пустая, мы переопределим её в docker-compose
CMD ["bash"]