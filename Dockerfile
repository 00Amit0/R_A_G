# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . /app

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Ensure stdout/stderr are not buffered
ENV PYTHONUNBUFFERED=1

# Default command to run both FastAPI (uvicorn) and Streamlit
# We'll run Streamlit separately in docker-compose for easier management
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
