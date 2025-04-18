# Use Python base image
FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Copy all files & folders into the container
COPY . .

# Install required Python packages
RUN pip install -r requirements.txt

# Expose the correct Flask port
EXPOSE 8787

# Run the Flask app
CMD ["python", "app.py"]
