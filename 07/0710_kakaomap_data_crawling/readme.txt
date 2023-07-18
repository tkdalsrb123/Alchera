2023-07-17

1. 요청사항
[카카오맵 데이터 크롤링 코드 요청]

2. 실행방법
python main.py [excel 경로]

구동 전 셋팅 작업
1. line22 - wait = WebDriverWait(driver, sec)
sec를 설정하여 브라우저 창이 켜져있는 시간을 조정할 수 있습니다. 

2. line39 - for i in range(n):
n에 값을 넣어 스크린샷의 장 수를 설정할 수 있습니다.

3. line44 - move_by_offset(w, h)\
마우스가 클릭하는 위치를 조정하여 로드뷰 화면이 이동하는 위치를 정할 수 있습니다.
ex) 스크린샷 아이콘 위치를 기준으로 (-1200, 100)은 왼쪽으로 (-200, 100)은 오른쪽으로 이동합니다.

2023-07-18

수정사항
3. line49 - send_keys(Keys.ARROW_LEFT)
왼쪽으로 이동시 Keys.ARROW_LEFT, 오른쪽으로 이동시 Keys.ARROW_RIGHT
