FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY backend/ ./backend/

# Copy the database file
COPY backend/song_database_trial.db ./backend/

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["python", "backend/start.py"] 