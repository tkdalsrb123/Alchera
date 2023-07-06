2023-07-06

1. 요청사항
[xml 데이터 클래스별 count 코드 요청]

2. 실행방법
python main.py [xml 최상위 경로] [엑셀 파일 경로] [count 저장 경로]

수정
51줄 추가.
dictionary에서 count를 가져오기 때문에 순서 정렬이 안됌.
class_list에 class 순서대로 label에서 count를 가져옴.