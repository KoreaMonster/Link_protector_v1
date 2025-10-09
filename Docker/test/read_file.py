# read_file.py
import os

print("=" * 50)
print(" 파일 읽기 테스트")
print("=" * 50)

# 공유 폴더의 파일 읽기
file_path = "/shared/message.txt"

if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f" 파일을 성공적으로 읽었습니다!")
    print(f" 내용: {content}")
else:
    print(f" 파일을 찾을 수 없습니다: {file_path}")

print("=" * 50)