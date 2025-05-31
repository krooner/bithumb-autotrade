# bithumb-autotrade

[[빗썸 x 조코딩] AI 비트코인 투자 자동화 중급 2기 1 DAY 특강](https://event-us.kr/jocoding/event/104209)
- [강의자료](https://jocoding.net/gptbitcoin-bithumb)

# Prerequisite
1. [Bithumb 회원 가입 후 API 키 발급](https://www.bithumb.com/react/api-support/management-api) + [수수료 쿠폰 등록](https://www.bithumb.com/react/info/fee/trade)

> API는 현재 IP 기준으로 발급했을 때 유효하므로, IP가 변경되는 경우 다시 발급받아야 함. 집 인터넷 환경에서 발급받은 API를 다른 곳의 와이파이 연결한 환경에서 쓸 수 없음.

2. [OpenAI 회원 가입, 결제 수단 등록, API 키 발급](https://platform.openai.com/)

3. [AWS 계정 생성 및 결제 수단 등록](https://aws.amazon.com/console/)

4. [GitHub 계정 생성 및 Repository 생성](https://github.com/)

## 작업 환경 설정

1. 가상 환경 생성 및 필요 라이브러리 설치
```bash
$ python3 -m venv venv-bithumb
$ source venv-bithumb/bin/activate
(venv-bithumb) $ pip install -r requirements.txt
```

2. .env 파일 생성 및 설정
```python
# .env

BITHUMB_ACCESS_KEY="<bithumb에서 발급받은 키>"
BITHUMB_SECRET_KEY="<bithumb에서 발급받은 키>"
OPENAI_API_KEY="<OpenAI API 키>"
SERPAPI_API_KEY="<SERPAPI API 키>"
```

> .env를 잘 못 읽어오는 경우는 `load_dotenv(override=True)`

# 과정 설명

|파일|설명|
|---|---|
|[00_mvp.py](./00_mvp.py)|Baseline code; 비트코인 30일 일봉 데이터를 제공하여 ChatGPT로부터 판단을 받아 자동 매매|
|[11_multitimeframe_autotrade.py](./11_multitimeframe_autotrade.py)|비트코인(BTC)의 멀티 타임프레임(1시간, 4시간, 일봉) 차트 데이터를 수집한 뒤, 매수(buy), 매도(sell), 보유(hold) 중 어떤 행동을 할지 AI에게 판단 결과와 이유 요청|
|[12_invest_philosophy_autotrade.py](./12_invest_philosophy_autotrade.py)|"절대 돈을 잃지 않는다"는 투자 철학을 제공하여 AI에게 매수(buy), 매도(sell), 보유(hold) 중 어떤 행동을 할지 판단 결과와 이유 요청|
|[13_news_autotrade.py](./13_news_autotrade.py)|멀티 타임프레임(1시간, 4시간, 일봉) 차트 데이터와 최근 1주일간의 비트코인 관련 뉴스 데이터를 수집한 뒤, 매수(buy), 매도(sell), 보유(hold) 판단을 요청하는 자동매매|
|[14_invest_ratio_autotrade.py](./14_invest_ratio_autotrade.py)|매수(buy), 매도(sell), 보유(hold) 중 하나와 투자 비율(%)을 결정받아 실제 빗썸 거래소에서 해당 비율만큼 자동으로 매매를 실행. 최소 주문 금액 미만일 경우 주문을 실행하지 않음|
|[21_save_db_autotrade.py](./21_save_db_autotrade.py)|거래 실행 후에는 거래 결정, 투자 비율, 사유, 잔고, 가격 등의 정보를 SQLite 데이터베이스에 기록하여 자동매매 내역을 저장|
|[22_retrospect_db_autotrade.py](./22_retrospect_db_autotrade.py)|거래 실행 후에는 결과와 잔고 정보를 SQLite 데이터베이스에 저장하며, 최근 거래 내역도 AI의 의사결정에 반영하여 전략의 일관성과 학습 효과를 높임.|
|[23_summary_autotrade.py](./23_summary_autotrade.py), [autotrade.py](./autotrade.py)|거래 결과와 잔고 정보는 SQLite 데이터베이스에 저장되며, 이 작업은 매일 09:00, 15:00, 21:00에 자동으로 실행되고, AI는 최근 거래 내역까지 참고하여 전략을 개선|
|[streamlit_app.py](./streamlit_app.py)|Streamlit을 이용해 비트코인 자동매매 시스템의 거래 내역과 성과를 시각적으로 보여주는 대시보드 웹앱|
|[ec2_script.sh](./ec2_script.sh)|AWS EC2 인스턴스에 접속하여 실행해야 할 커맨드 목록|

## AWS 클라우드 배포

```bash
# 1. AWS EC2 인스턴스를 생성 및 해당 인스턴스에 접속

$ git clone https://github.com/krooner/bithumb-autotrade.git
$ cd bithumb-autotrade.git
$ vim .env
# API 키 추가
# 주의: Bithumb API 키의 경우는 해당 인스턴스의 Public IP를 추가하여 새로 발급받은 것을 입력해야함.

$ python3 -m venv bithumb-venv
$ source bithumb-venv/bin/activate
(bithumb-venv) $ pip install -r requirements.txt

# 비트코인 자동매매 스크립트 실행
(bithumb-venv) $ nohup python3 -u autotrade.py > output.log 2>&1 &

# Streamlit 기반 시각화 웹앱 실행
(bithumb-venv) nohup python3 -m streamlit run streamlit_app.py --server.port 8501 > streamlit.log 2>&1 &
```