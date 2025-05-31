#!/bin/bash

#한국 기준으로 서버 시간 설정
sudo ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

#패키지 목록 업데이트
sudo apt update

#패키지 목록 업그레이드
sudo apt upgrade

#pip3 설치
sudo apt install python3-pip

#가상 환경 만들기 설치
sudo apt install python3.12-venv

#pip3 가상 환경 만들기
python3 -m venv bitcoinenv

#가상 환경 활성화
source bitcoinenv/bin/activate

# 레포지토리 가져오기
git clone https://github.com/krooner/bithumb-autotrade.git

# 현재 경로 상세 출력
ls -al

# 경로 이동
cd bithumb-autotrade.git

#서버에서 라이브러리 설치
pip3 install -r requirements.txt

#.env 파일 만들고 API KEY 넣기
vim .env

#vim 에디터로 파일 열기
vim autotrade.py
#vim 에디터 입력 모드 전환: i
#vim 에디터 입력 모드 나가기: ESC
#vim 에디터 저장 안하고 나가기: ESC + :q!
#vim 에디터 저장 및 종료: ESC + :wq!

# 그냥 실행하기
python3 autotrade.py

#백그라운드 실행
nohup python3 -u autotrade.py > output.log 2>&1 &

#실행 확인
ps ax | grep .py

#vim 에디터로 열기
vim output.log
#로그 보기
cat output.log
#로그 맨 끝 보기
tail -f output.log

#종료하기 ex. kill -9 13586
kill -9 PID

#백그라운드 실행 (웹 대시보드)
nohup python3 -m streamlit run streamlit_app.py --server.port 8501 > streamlit.log 2>&1 &