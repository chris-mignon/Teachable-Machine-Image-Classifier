# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files to container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && rm -rf /root/.cache


# Expose the port Flask will run on
EXPOSE 10000

# Set environment variable so Flask runs in production mode
ENV PORT=10000
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run using gunicorn (production-grade server)
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
