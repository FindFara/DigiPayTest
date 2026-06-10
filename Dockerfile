FROM mcr.microsoft.com/playwright/python:v1.45.3-jammy
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["pytest", "-m", "smoke or regression"]
