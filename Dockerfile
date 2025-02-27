# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that Cloud Run dynamically assigns (via the $PORT environment variable)
EXPOSE 8080

# Run the application using Gunicorn, binding to the port provided by Google Cloud
CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "app:app"]
