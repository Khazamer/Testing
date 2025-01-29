# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents (including your code) into the container
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app will run on (change if necessary for your app)
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]