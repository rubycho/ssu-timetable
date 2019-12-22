# ssu-timetable

숭실대학교 시간표 시스템 파서 which is inspired from [gomjellie/pysaint](https://github.com/gomjellie/pysaint).

pysaint와 달리 해당 패키지는 시간표 조회 기능만 가집니다.

현재는 과목 리스트 데이터를 추가 처리 없이 html 코드로만 제공합니다.

사용방법은 usage.ipynb 파일을 참고하세요.

## 개발환경
1. lxml 파서 관련 패키지 설치
    ```bash
    sudo apt-get install libxslt-dev
    sudo apt-get install libxml2-dev
    ```
1. pip로 venv에 패키지 설치
    ```bash
    (venv) pip install -r requirements.txt
    ```
