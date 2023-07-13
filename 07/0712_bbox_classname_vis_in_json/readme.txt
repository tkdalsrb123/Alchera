2023-07-12

1. 요청사항
[3-016-291 Json 내의 BBox 및 클래스명 시각화]

2. 실행방법
python main.py [input 최상위 폴더] [output 최상위 폴더] [시각화 type 0 or 1]

시각화 type = 0
: surface를 제외한 나머지 시각화

시각화 type = 1
: surface만 시각화

fontsize 조절 방법
: 48line 에서 크기 조정 가능
(굵기는 글씨체를 변경해야 합니다. 49line에서 글꼴을 변경하시면 됩니다. -> 제어판\모양 및 개인 설정\글꼴)

bbox 굵기 조절 방법
: 67line or 84line 에서 draw.rectangle 안에 width 인자를 설정


0713 오류 수정
- 확장자가 JPEG를 가진 파일이 있어 JPEG도 시각화 가능하게 수정
- RGBA 색상값을 가진 파일이 잇어 이미지를 불러올 때 RGB로 변환