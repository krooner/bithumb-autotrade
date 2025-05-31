# bithumb-autotrade

1. 가상 환경 생성 및 설치
```bash
$ python3 -m venv venv-bithumb
$ source venv-bithumb/bin/activate
(venv-bithumb) $ pip install -r requirements.txt
```

2. .env 파일 생성
```python
# .env

BITHUMB_ACCESS_KEY="<bithumb에서 발급받은 키>"
BITHUMB_SECRET_KEY="<bithumb에서 발급받은 키>"
OPENAI_API_KEY="<OpenAI API 키>"
SERPAPI_API_KEY="<SERPAPI API 키>"
```

> .env를 잘 못 읽어오는 경우는 `load_dotenv(override=True)`