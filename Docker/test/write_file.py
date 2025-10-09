# write_file.py
import datetime

print("=" * 50)
print("✍ 파일 쓰기 테스트")
print("=" * 50)

# 컨테이너에서 파일 생성
output_path = "/shared/output.txt"

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(f"이 파일은 Docker 컨테이너에서 생성되었습니다!\n")
    f.write(f"생성 시간: {datetime.datetime.now()}\n")

print(f" 파일 생성 완료: {output_path}")
print(" 호스트의 shared/ 폴더를 확인해보세요")
print("=" * 50)