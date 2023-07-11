from selenium import webdriver
import time

# Chrome WebDriver 경로 설정
# webdriver_path = "./chromedriver_win32/chromedriver.exe"  # 다운로드한 Chrome WebDriver의 경로로 변경해야 합니다.

# 웹 브라우저 열기
browser = webdriver.Chrome()

# 카카오맵 로드뷰 페이지로 이동
keyword = '전라북도 장수군 장수읍 개실길'
browser.get('https://map.kakao.com/')

# 로드뷰 영역을 찾기 위해 필요한 정보
x_coord = '127.0561464'  # 경도(Longitude) 값을 입력하세요.
y_coord = '37.5050101'  # 위도(Latitude) 값을 입력하세요.

# 로드뷰 영역으로 이동
browser.execute_script(f"searchAround('{x_coord}', '{y_coord}');")

# 로드뷰 영역이 로드될 때까지 잠시 대기
time.sleep(5)

# 로드뷰 캡쳐
browser.save_screenshot('./roadview.png')

# 웹 브라우저 닫기
browser.quit()
