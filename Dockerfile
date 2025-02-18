# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Set environment variables (if needed)
ENV PYTHONUNBUFFERED=1

# Make the start script executable
RUN chmod +x scripts/start_bot.sh

# Command to run the bot
CMD ["./scripts/start_bot.sh"]