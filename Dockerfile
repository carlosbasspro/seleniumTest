# Use the official Python image as the base
FROM python:3.11-slim

# Install necessary dependencies for Selenium, Chrome, and Chromedriver
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium \
    && apt-get clean

# Remove any previous versions of Chromedriver, if they exist
RUN rm -f /usr/local/bin/chromedriver

# Download and install the Chromedriver compatible with the Chromium version
RUN wget -q "https://chromedriver.storage.googleapis.com/130.0.6723.116/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm chromedriver_linux64.zip

# Verify the installed versions (optional, for debug)
RUN chromium --version && chromedriver --version

# Set the working directory in the container
WORKDIR /app

# Copy the Python script to the container
COPY main.py .

# Copy and install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 10000
EXPOSE 10000

# Command to run the script
CMD ["python", "main.py"]
