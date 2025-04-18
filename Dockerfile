FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install "uv" && uv install
COPY . .
CMD ["uv", "run", "python service/main.py"]