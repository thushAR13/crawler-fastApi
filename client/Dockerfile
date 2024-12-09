# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt from the parent directory to the container
COPY ../requirements.txt ./requirements.txt

# Copy only the necessary files from the client directory
COPY client/client.py ./client.py
COPY client/client_config.yaml ./client_config.yaml
COPY client/templates ./templates

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8001 for the client service
EXPOSE 8001

# Run the FastAPI application
CMD ["uvicorn", "client:app", "--host", "0.0.0.0", "--port", "8001"]
