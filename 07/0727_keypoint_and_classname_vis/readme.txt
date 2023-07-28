2023-07-27

1. 요청사항
[Keypoint 및 클래스명 시각화]

2. 실행방법
python main.py [input 최상위 폴더] [output 최상위 폴더]

2023-07-28

1. 수정사항
- keypoint 값이 있는 객체만 keypoint와 bbox 같이 시각화
- point가 빈 원이 아닌 점으로 시각화
- bbox 위에만 텍스트 시각화
- 텍스트가 이미지 밖으로 벗어날 경우 박스 하단에 텍스트 시각화

2. 2차 수정사항
- keypoint가 없어도 bbox 시각화
- ActionValue true = 빨간색, false = 파란색 으로 색상 지정