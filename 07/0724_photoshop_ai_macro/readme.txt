2023-07-26

1. 요청사항
[포토샵 AI 합성 메크로 제작]

2. 실행방법
python main.py [input 폴더]

3. 사전작업

3-1. 포토샵 프로그램 사전작업
1. Adobe Photoshop (Beta)를 연다.
2. 파일(F) -> 열기(O) 에서 사용하고자 하는 이미지 한장을 불러온다.
3. 파일(F) -> 내보내기(E) -> PNG(으)로 빠른 내보내기 에서 저장하고자 하는 폴더에 한번 저장한다.
4. 저장한 이미지는 삭제한다.

3-2. 스크립트 사전작업
1. path를 Photoshop.exe 의 경로를 찾아서 바꿔준다.
- Line11 *.connect(path=r"...\Photoshop.exe")

2. 첨부되어있는 마우스 트레이서를 이용하여 좌표를 확인하고 바꿔준다.
- Line13 파일(F) 좌표
- Line14 생성형 범위 시작지점(이미지 좌측 상단 모서리) 좌표
- Line15 생성형 범위 끝지점 좌표
- Line16 생성형 생성 위치(기준 생성형 박스 오른쪽 하단 모서리) 좌표