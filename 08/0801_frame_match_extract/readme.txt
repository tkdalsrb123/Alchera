2023-08-02

1. 요청사항
[기존 DB 비교 후 추가 프레임 추출하여 파일명 변경 ]

2. 스크립트

2-1. extract_full_frame.py

2-1-1. 실행방법
python extract_full_frame.py [input 최상위 폴더] [output 최상위 폴더]

2-2. frame_match_extract.py

2-2-1. 실행방법
python frame_match_extract.py [기존 db 최상위 폴더] [extract_full_frame으로 추출한 db 최상위 폴더] [저장 폴더] [기능 (0 or 1)]

2-2-2. 기능설명
기능 = 0 일때,
맨 앞장을 기준으로 프레임 추출

기능 = 1 일때,
맨 앞장이 기준과 다를 시 제외하고 프레임 추출

2023-08-07

1. 수정사항
- old db에서 프레임이 끊겨있는 경우가 있는데 이때 그냥 넘어간다.