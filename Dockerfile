FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
CMD ["gunicorn", "backend.app:create_app()", "-b", "0.0.0.0:5000", "--workers", "2"]
