1122 상우진

1. 요청사항
[[SKT]treeD json → 납품 포맷 json 형식으로 변환]

2. 실행방법
python main.py [input dir] [output dir]

1221

1. 수정사항
[’value’: “문장” 에서 문장의 앞 큰따옴표에서 발생하는 오류 사항]
" (큰따옴표+공백)
"\n
-> 이경우에 "로 교체
[’value’: “문장” 에서 문장의 뒤 큰따옴표에서 발생하는 오류 사항]
" (공백+큰따옴표)
\n"
\n\n"
\n" (공백+개행표시+큰따옴표)
-> 이경우에 "로 교체
[그외 문장 내에서 발생하는 오류 사항]
® (공백+해당 특수문자)
->공백 삭제 해당 특수문자만
\n (공백+개행)
-> 공백 삭제 후 개행표시만