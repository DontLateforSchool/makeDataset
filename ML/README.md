python version 3.10환경에서 진행하였습니다.

requirements.txt 파일을 통해 종속 라이브러리를 설치한 후 아래 명령어를 통해 api 서버를 돌립니다.

host와 port는 자유롭게 변경이 가능합니다.

```
uvicorn main:app --reload --host 0.0.0.0 --port 80
```