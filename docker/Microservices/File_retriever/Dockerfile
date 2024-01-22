# Use a lightweight base image
FROM alpine:3.15

# Set the working directory
WORKDIR /app

# Copy the Bash script into the container
COPY . /app

# Make the script executable
RUN chmod +x retrieve_files.sh

# Run the Bash script when the container starts
CMD ["/bin/sh", "/app/retrieve_files.sh"]

