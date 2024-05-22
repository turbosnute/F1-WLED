FROM php:8.3-apache-bullseye

RUN apt-get update && apt-get install --no-install-recommends -y python3 python3-dev python3-venv python3-pip python3-wheel build-essential supervisor nano && \
   apt-get clean && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Make dir for app
RUN mkdir /app/
WORKDIR /app/

# Install requirements
COPY /requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Make dir for config
RUN mkdir /config/ && \
chown www-data /config/ && \
chmod 700 /config/

# Copy Code
COPY /src/* /app/

# Deploy Code
RUN bash /app/deploy.sh && rm /app/deploy.sh

# Permissions
RUN chmod 755 /app/app.sh /app/f1wled.py
