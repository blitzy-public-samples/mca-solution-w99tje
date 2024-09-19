# Use Python 3.9 slim image as the base
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY src ./src

# Copy the Alembic configuration file
COPY alembic.ini .

# Expose port 8000 for the API
EXPOSE 8000

# Set the command to run the API server using Uvicorn
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]