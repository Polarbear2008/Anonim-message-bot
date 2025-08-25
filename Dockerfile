FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port (Railway will set PORT environment variable)
EXPOSE $PORT

# Command to run the application
CMD ["python", "src/__main__.py"]