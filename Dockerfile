FROM python:3.13-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

EXPOSE 80
# Run your app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "backend_new:app"]