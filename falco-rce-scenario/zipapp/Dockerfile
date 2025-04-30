FROM debian:bullseye-slim

WORKDIR /app

# Copy app
COPY app.py .
RUN mkdir -p templates
COPY templates/base.html templates/base.html
COPY templates/index.html templates/index.html
COPY templates/list.html templates/list.html

# Install Python and tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip \
        curl \
        net-tools \
        iputils-ping \
        dnsutils \
        whois \
        nmap \
        procps \
        nano \
        bash \
        wget \
        zip \
        unzip \
    && pip3 install flask \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["python3", "-u", "app.py"]
