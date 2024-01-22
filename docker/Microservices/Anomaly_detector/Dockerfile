# Use the official TensorFlow Lite image as the base
FROM eiqcloud/tflite-inference


# Set the working directory
WORKDIR /app

# Copy the application code and requirements
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Command to run your application
CMD ["python", "tflite.py"]
