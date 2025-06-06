FROM python:3.12-slim

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Set the working directory
WORKDIR /app

# Copy all files into the container
COPY . .

# Install Python packages
RUN pip install -r requirements.txt

# Start your bot
CMD ["python", "main.py"]
