FROM python:3.13-slim

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV HEADLESS=true

# Instalar dependências do sistema incluindo xvfb e xauth
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    unzip \
    xvfb \
    xauth \ 
    libxi6 \
    libgconf-2-4 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*


RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME ["/app/logs", "/app/reports"]

CMD ["xvfb-run", "--server-args='-screen 0 1920x1080x24'", "python", "-m", "unittest", "discover", "-s", "tests"]