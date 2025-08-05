# 🚀 프로젝트명 (예: SKN18‑1st‑3Team)

본 프로젝트는 **전기차 등록대수** 증가와 **인프라 확장**, 그리고 **지역별 고용·산업 구조 변화** 간의 관계를 분석하고 시각화하여, 전기차 확산이 사회 및 산업에 미치는 영향을 탐색합니다.

---

## 📋 목차

1. 팀 소개  
2. 프로젝트 개요  
3. 기술 스택  
4. 시스템 구조 및 플로우  
5. 주요 기능  
6. 데이터 흐름 및 저장 방식  
7. UI 구성 (Streamlit 다중 페이지)  
8. 향후 확장 방향  
9. 회고 및 감사 인사  

---

## 1. 팀 소개

## 👥 팀원 소개

| **박세영** | **김담하** | **김민주** | **이상효** | **임승옥** | **채린** |
|:--:|:--:|:--:|:--:|:--:|:--:|
| ![](assets/park.png) | ![](assets/kim_dh.png) | ![](assets/kim_mj.png) | ![](assets/lee_sh.png) | ![](assets/lim_so.png) | ![](assets/chae.png) |
| [@github1](https://github.com/github1) | [@github2](https://github.com/github2) | [@github3](https://github.com/github3) | [@github4](https://github.com/github4) | [@github5](https://github.com/github5) | [@github6](https://github.com/github6) |




---

## 2. 프로젝트 개요

### ✅ 프로젝트 목표  
프로젝트의 주요 의도 및 해결하고자 하는 문제 정의

### 👉 필요성  
- 왜 해당 프로젝트를 수행하게 되었는지  
- 기존 솔루션의 한계 또는 시장/사용자 요구 사항

---

## 3. 기술 스택

| 분야      | 기술/도구                                                     |
|-----------|---------------------------------------------------------------|
| 개발 언어 | Python                                                        |
| 크롤링    | Selenium, BeautifulSoup                                       |
| 데이터 처리 | pandas, SQLAlchemy                                           |
| 데이터베이스 | MySQL                                           |
| 웹 UI     | Streamlit                                 |
| 환경 관리   | .env, requirements.txt                           |

---

## 4. 시스템 구조 및 플로우

### 🏗 아키텍처 구성요소
- 크롤링 모듈 → 데이터 저장 (CSV 또는 DB) → Streamlit 인터페이스

### 🗺 흐름도
1. `faq.py`로 고객 FAQ 수집  
2. `insert_db.py`를 통해 DB에 삽입  
3. `app.py` 실행 → `pages/` 내 개별 페이지 구동  

---

## 5. 주요 기능

### ✔ 크롤링 (`faq.py`)
- 기아 고객 FAQ 웹 페이지에서 카테고리별 질문‑답변 전체 수집
- 페이지 처리 및 반복 데이터 수집 자동화  
- 결과를 `kia_faq_data.csv` 저장

### ✔ DB 저장 (`common/insert_db.py`)
- CSV 파일 기반 MySQL 테이블 생성 및 데이터 삽입

### ✔ UI 조회 (`pages/faq_page.py`)
- FAQ 검색 + 카테고리 필터 기능  
- `st.expander` 기반 질문 펼치기 UI  
- 키워드 기반 실시간 검색

### ✔ 추가 페이지 (`pages/page01.py`, `page02.py` 등)
- 예: 통계 분석, AI 요약, 요금 계산기 등  
- 추가 페이지는 `app.py` 자동 등록

---

## 6. 데이터 흐름 및 저장 방식

- selenium 및 beautifulsoup으로 웹페이지를 크롤링 작업
- 수집 데이터 저장 형태: CSV/XLSX (`kia_faq_data.csv` 등)  
- 이 데이터를 `insert_db.py`로 MySQL 테이블 `kia_faq`에 저장  
- 실시간 조회는 Streamlit이 DB로부터 직접 읽는 방식 또는 pandas CSV 로딩 방식  
- DB 접속 정보는 `.env` 파일에 저장 (host, port, user, password, db_name 등)

---

## 7. UI 구성 (Streamlit 다중 페이지)

```text
CHAP1/
├── assets/                  # 이미지, 로고 등 정적 리소스
│   ├── electric_car.png
│   └── skn_logo.png

├── common/                  # 공통 유틸 및 DB 초기화 코드
│   ├── .env                 # DB 환경 변수 파일
│   ├── create_db.sql        # DB 스키마 생성 쿼리
│   ├── insert_db.py         # CSV → MySQL 데이터 삽입 스크립트
│   └── utils.py             # DB 접속 및 기타 유틸 함수

├── data/
│   └── KIA_FAQ/            
│       ├── faq.py           # Selenium 기반 FAQ 크롤러
│       └── kia_faq_data.csv # 수집된 CSV 데이터

├── pages/                                  # Streamlit 다중 페이지 구성
│   ├── faq_page.py                          # 메인 FAQ 검색 UI
│   ├── 01. Region_Popul_Graph.py           # 지역별 인구-자동차 등록 상관계수
│   ├── 02. Employment_and_Industry.py      # 고용자수-산업 상관계수 페이지
│   ├── 03. Number_of_Registering_Car.py     # 차량 등록 수와 고용/소득/산업 간 상관관계 분석  
│   └── 04. Electric_Car_and_Infra.py    # 전기차 등록 및 인프라 분포 페이지

├── src/
│   └── crawling.py          # 기타 크롤러

├── app.py                   # Streamlit 첫 페이지
└── requirements.txt         # 설치 필요 패키지 목록

```

- `app.py`는 Streamlit `page_config` 기반으로 자동 페이지 라우팅  
- 각 페이지는 독립적으로 구성 가능 (검색, 시각화, 사용자 인터랙션 등)

---

## 8. 향후 확장 방향

- [ ] `page03.py`: 예를 들어 GPT 기반 요약 기능 추가  
- [ ] FAQ 자동 업데이트 주기 설정 (cron 혹은 배치 스케줄러)  
- [ ] 페이징 기능 추가 (검색 결과에 대한 검색 페이징)  
- [ ] Docker 컨테이너화 + 클라우드 배포 (Heroku, AWS 등)  
- [ ] 관리자 페이지 및 CRUD 기반 FAQ 편집 기능

---

## 9. 회고 및 감사 인사

### 🙏 회고
- **팀장**: 전체 흐름 설계와 일정 조율에 주력  
- **팀원 A**: 크롤러 기능 구현 및 디버깅  
- **팀원 B**: UI 디자인 및 검색 기능 구현  

### 💌 감사 인사  
본 프로젝트는 **SK 네트웍스 AI 캠프 1기 3조**의 협업 결과물입니다.  
피드백 및 개선 사항은 언제든 환영합니다!

---

## 📌 실행 가이드 (간단 요약)

```bash
pip install -r requirements.txt

# DB 초기화
mysql -u YOUR_USER -p < common/create_db.sql

# 크롤링 실행 (CSV 생성)
python data/KIA_FAQ/faq.py

# DB 삽입
python common/insert_db.py

# Streamlit 실행
streamlit run app.py
```