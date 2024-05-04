FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src/ .

# Give permissions to dump.rdb
# RUN chmod +r /app/data/dump.rdb

# Command to run the application

CMD ["python", "src/api.py"]
