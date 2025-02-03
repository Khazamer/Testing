# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install necessary dependencies for Chrome and Selenium
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    ca-certificates \
    libx11-dev \
    libxrender-dev \
    libxtst-dev \
    libglib2.0-0 \
    libsm6 \
    libfontconfig1 \
    libxdamage1 \
    libgdk-pixbuf2.0-0 \
    libdbus-1-3 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcairo2 \
    libcups2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libvulkan1 \
    libxcomposite1 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*  # Clean up the apt cache

# Download and install Google Chrome (or use a specific version of Chrome if needed)
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb \
    && apt-get -f install -y \
    && rm google-chrome-stable_current_amd64.deb

# Install Selenium
RUN pip install selenium

# Install chromedriver matching the version of Google Chrome you installed
RUN LATEST=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -N https://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm chromedriver_linux64.zip

# Set environment variables for Chrome
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/google-chrome-stable
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

# Set the working directory inside the container
WORKDIR /app

# Ensure the images folder exists
RUN mkdir -p /app/images

# Copy the current directory contents (including your code) into the container
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app will run on (change if necessary for your app)
EXPOSE 5000

# Run the docker up command
CMD ["docker", "compose", "up", "-d"]

# Run the application
CMD ["python", "app.py"]