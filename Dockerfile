FROM python:3.9-slim

WORKDIR /app

# Copy requirements file first
COPY requirements.txt /app/

# Install dependencies with verbose output
RUN echo "Installing dependencies" \
    && pip install --no-cache-dir --verbose -r requirements.txt \
    && echo "Dependencies installed successfully"

# Copy the rest of the application code
COPY . /app

EXPOSE 5000

CMD ["python", "app.py"]