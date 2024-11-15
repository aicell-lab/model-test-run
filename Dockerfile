FROM python:3.12
WORKDIR /app
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
 && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/bioimage-io/spec-bioimage-io.git@main

RUN python -c "from bioimageio.spec.get_conda_env import get_conda_env, BioimageioCondaEnv" 

COPY . .

ENTRYPOINT ["python", "src/main.py"]
