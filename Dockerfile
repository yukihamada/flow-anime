FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir tweepy
COPY . /app
RUN mkdir -p /data
ENV PORT=8080 STATIC_DIR=/app DASH_KEY=flow2026
EXPOSE 8080
CMD ["python3", "server.py"]
