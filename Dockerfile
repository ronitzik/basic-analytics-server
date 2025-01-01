FROM ubuntu:latest
LABEL authors="Ron"
FROM python:3.10-slim

FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run your app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

