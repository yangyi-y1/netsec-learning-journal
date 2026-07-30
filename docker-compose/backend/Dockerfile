FROM python:3.13-slim

WORKDIR /app

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
