# Use a base image with Python and MongoDB pre-installed
FROM python:3.9
# Copy the Python requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade firebase-admin
RUN pip install Flask[async]
RUN pip install kubernetes
# Copy the Python script
# COPY spotify/main.py .
# COPY spotify/serviceAccountKey.json .
# COPY spotify/login.html .
# COPY spotify/css/login.css .
WORKDIR /app
COPY spotify /app/spotify
# Set the working directory

# Start the Python application
# Set environment variable
CMD ["python", "spotify/app.py"]
