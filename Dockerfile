# Use a base image with Python and MongoDB pre-installed
FROM python:3.9
# Copy the Python requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade firebase-admin
# Copy the Python script
# COPY spotify/main.py .
# COPY spotify/serviceAccountKey.json .
# COPY spotify/login.html .
# COPY spotify/css/login.css .
COPY spotify /app/spotify

# Set the working directory
WORKDIR /app
# Start the Python application
# Set environment variable
ENV JWT_SECRET=test
CMD ["python", "spotify/main.py"]
