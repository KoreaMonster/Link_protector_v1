FROM python:3.9-slim

WORKDIR /app

# 세 개의 스크립트 복사
COPY hello.py /app/
COPY read_file.py /app/
COPY write_file.py /app/

# 기본 명령은 hello.py
CMD ["python", "hello.py"]