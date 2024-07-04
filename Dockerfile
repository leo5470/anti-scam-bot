FROM python:3.8-slim

# 設定容器的工作目錄，後續RUN CMD ENTRYPOINT COPY ADD指令都在該目錄下執行
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
