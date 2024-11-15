FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
 && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/bioimage-io/spec-bioimage-io.git@main
COPY . .

ENTRYPOINT ["python", "src/main.py"]
