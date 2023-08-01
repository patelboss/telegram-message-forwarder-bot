
# Start with the official Python 3.8 slim buster image
FROM python:3.8-slim-buster

# Update and upgrade the system packages
RUN apt-get update -y && apt-get upgrade -y

# Install git
RUN apt-get install -y git

# Copy requirements.txt file
COPY requirements.txt /requirements.txt

# Install Python dependencies from requirements.txt
RUN pip3 install -r /requirements.txt

# Set the working directory
WORKDIR /cd

# Copy start.sh script
COPY start.sh /start.sh

# Make the start.sh script executable
RUN chmod +x /start.sh

# Set the command to run when the container starts
CMD ["/bin/bash", "/start.sh"]
