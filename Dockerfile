# Use an official lightweight Python image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Install firebase-tools globally
RUN npm install -g firebase-tools

# Set working directory
WORKDIR /app

# Copy all project files into container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose dynamic port (optional)
EXPOSE 8080

# Use the correct entrypoint to handle PORT
CMD exec gunicorn --bind 0.0.0.0:${PORT:-5000} modus_backend:app
