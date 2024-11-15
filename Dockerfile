FROM python:3.12
WORKDIR /app
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
 && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/bioimage-io/spec-bioimage-io.git@main

#Temp fix until next biomiageio.spec release
RUN git clone --depth 1 https://github.com/bioimage-io/spec-bioimage-io.git /bioimageio-spec
RUN cp -r /bioimageio-spec/bioimageio /usr/local/lib/python3.12/site-packages/

#Check that get_conda_env exists
RUN python -c "import bioimageio.spec.get_conda_env" 

COPY . .

ENTRYPOINT ["python", "src/main.py"]
