import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def analyze_url(url):
    """
    URL 분석 메인 함수

    왜 이 함수가 필요한가?
    - Django가 Docker 컨테이너로 이 스크립트 실행
    - 컨테이너 내부에서 Selenium으로 URL 접속
    - 결과를 파일로 저장하면 Django가 읽어감
    """
    print(f"분석 시작: {url}")

    # Chrome 옵션 설정
    options = Options()
    # options.add_argument('--headless')  # 화면 없이 실행
    options.add_argument('--no-sandbox')  # Docker 필수!
    options.add_argument('--disable-dev-shm-usage')  # 메모리 이슈 방지
    options.add_argument('--disable-gpu')  # GPU 비활성화
    options.add_argument('--window-size=1920,1080')  # 초기 창 크기

    # Chrome 드라이버 실행
    driver = webdriver.Chrome(options=options)

    try:
        # URL 접속
        driver.get(url)
        driver.implicitly_wait(3)  # 페이지 로딩 대기

        # 전체 페이지 높이 계산
        total_height = driver.execute_script("return document.body.scrollHeight")

        # 최대 높이 제한 (무한 스크롤 페이지 대비)
        max_height = 10000
        total_height = min(total_height, max_height)

        # 전체 페이지 캡처를 위한 창 크기 조절
        driver.set_window_size(1920, total_height)

        # 분석 결과 데이터
        result = {
            'original_url': url,
            'final_url': driver.current_url,
            'page_title': driver.title,
            'page_height': total_height,
            'success': True
        }

        # 스크린샷 저장
        driver.save_screenshot('/output/screenshot.png')

        # 결과 JSON으로 저장
        with open('/output/result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"분석 완료!")
        print(f"   - 최종 URL: {result['final_url']}")
        print(f"   - 페이지 제목: {result['page_title']}")
        print(f"   - 페이지 높이: {result['page_height']}px")

    except Exception as e:
        print(f" 오류 발생: {e}")

        # 오류도 JSON으로 저장
        error_result = {
            'original_url': url,
            'success': False,
            'error': str(e)
        }

        with open('/output/result.json', 'w', encoding='utf-8') as f:
            json.dump(error_result, f, ensure_ascii=False, indent=2)

    finally:
        driver.quit()  # 브라우저 종료 (반드시!)


if __name__ == '__main__':
    # 명령행 인자 확인
    if len(sys.argv) < 2:
        print(" 사용법: python analyze.py <URL>")
        sys.exit(1)

    # 첫 번째 인자를 URL로 사용
    url = sys.argv[1]
    analyze_url(url)