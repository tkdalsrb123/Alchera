2023-08-17

1. 요청사항
[xml 양식 변경]

2. 실행방법
python main.py [input 이미지 최상위 경로] [input xml 최상위 경로] [output 이미지 경로] [output xml 경로]

2023-08-18
1. 수정사항
- 90도로 회전하였을 때 box 좌표가 right top , left bottom 으로 찍혀서 생긴 오류
- 좌표가 left top, right bottom 으로 찍히게 수정