# selenium_local_test.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print("=" * 50)
print("🌐 Selenium 로컬 테스트 시작")
print("=" * 50)

# Chrome 설정
options = webdriver.ChromeOptions()
# options.add_argument('--headless') # 일단 주석 -> 화면 안보이게 돌아가는 거
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 전체 페이지 캡처를 위한 설정
options.add_argument('--start-maximized')  # 최대 화면
options.add_argument('--window-size=1920,1080')  # 화면 크기 고정

# ChromeDriver 자동 설치 및 실행
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # 테스트 URL 접속
    test_url = "https://www.naver.com"  # 긴 페이지로 테스트
    print(f"📍 접속 중: {test_url}")

    driver.get(test_url)

    # 페이지 로딩 대기
    driver.implicitly_wait(3)

    # 정보 수집
    print(f"✅ 접속 완료!")
    print(f"📄 페이지 제목: {driver.title}")
    print(f"🔗 최종 URL: {driver.current_url}")

    # 전체 페이지 높이 가져오기
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")
    print(f" 전체 높이: {total_height}px")
    print(f" 보이는 높이: {viewport_height}px")

    # 방법 1: 브라우저 높이를 페이지 전체 높이로 설정
    driver.set_window_size(1920, total_height)

    # 스크린샷
    screenshot_path = "test_screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f" 전체 페이지 스크린샷 저장: {screenshot_path}")

except Exception as e:
    print(f" 오류 발생: {e}")
    import traceback

    traceback.print_exc()

finally:
    driver.quit()
    print("=" * 50)
    print("✅ 테스트 완료!")
    print("=" * 50)