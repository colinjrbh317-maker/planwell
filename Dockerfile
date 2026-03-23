FROM python:3.11-slim

WORKDIR /app

# Copy the full planwell-site so the .env path resolution works
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir flask flask-cors python-dotenv requests google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Set working directory to execution
WORKDIR /app/execution

# Expose the port Railway assigns (defaults to 5001)
EXPOSE 5001

# Start the webhook server
CMD ["python", "webhook_server.py"]
