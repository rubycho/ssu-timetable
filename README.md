# ssu-timetable

숭실대학교 [과목 조회 시스템](http://ecc.ssu.ac.kr/sap/bc/webdynpro/sap/zcmw2100?sap-language=KO#) 파서 
which is inspired from [gomjellie/pysaint](https://github.com/gomjellie/pysaint).

pysaint와 달리 해당 패키지는 과목 리스트 조회 기능만 가집니다.

## 사용방법
사용방법은 [usage.ipynb](https://github.com/rubycho/ssu-timetable/blob/master/usage.ipynb) 파일을 참고하세요.

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
