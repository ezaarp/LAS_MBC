FROM python:3.11-slim

# Set timezone ke Indonesia
ENV TZ=Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set working directory
WORKDIR /app

# Copy requirements dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy aplikasi
COPY . .

# Expose port
EXPOSE 5000

# Run aplikasi
CMD ["python", "app.py"]