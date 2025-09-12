FROM python:3.9-slim

WORKDIR /

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        wget \
        git \
        gnupg \
        libicu-dev \
        ca-certificates \
        apt-transport-https && \
    rm -rf /var/lib/apt/lists/*

# Add Microsoft package repository for .NET
RUN wget https://packages.microsoft.com/config/debian/11/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    rm packages-microsoft-prod.deb

# Install .NET Runtime 6.0
RUN apt-get update && \
    apt-get install -y dotnet-runtime-6.0 && \
    rm -rf /var/lib/apt/lists/*

# Copy your Python application
COPY trainer /trainer

# Set the entrypoint
ENTRYPOINT ["python", "-m", "trainer.task"]
