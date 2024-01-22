# Dockerfile for Consumer
FROM python:3.8

WORKDIR /app

# Copy the Python preprocessing script into the container
COPY . /app

# Install any dependencies your preprocessing script might need
RUN pip install -r requirements.txt

# Run the preprocessing script when the container starts
CMD ["python", "preprocess_packets.py"]
