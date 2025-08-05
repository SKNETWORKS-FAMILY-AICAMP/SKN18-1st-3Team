# 🚀 프로젝트명 (예: SKN18‑1st‑3Team)

> 팀명, 프로젝트명, 개발 기간, 슬로건 또는 한 줄 소개

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

| ![편성민](https://user-images.githubusercontent.com/your-path/red.png) | ![김재혁](https://user-images.githubusercontent.com/your-path/blue.png) | ![경규휘](https://user-images.githubusercontent.com/your-path/cyan.png) | ![배민경](https://user-images.githubusercontent.com/your-path/yellow.png) | ![이유호](https://user-images.githubusercontent.com/your-path/black.png) | ![조영훈](https://user-images.githubusercontent.com/your-path/purple.png) |
|:--:|:--:|:--:|:--:|:--:|:--:|
| **편성민** | **김재혁** | **경규휘** | **배민경** | **이유호** | **조영훈** |
| [@PyeonMin](https://github.com/PyeonMin) | [@KimJaeHyeok01](https://github.com/KimJaeHyeok01) | [@kqe123](https://github.com/kqe123) | [@baeminkyeong](https://github.com/baeminkyeong) | [@netsma](https://github.com/netsma) | [@yhcho0319](https://github.com/yhcho0319) |


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
| 데이터베이스 | MySQL 또는 MariaDB                                           |
| 웹 UI     | Streamlit (다중 페이지 지원)                                  |
| 환경 관리   | .env, virtualenv, requirements.txt                           |

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

- 수집 데이터 저장 형태: CSV (`kia_faq_data.csv`)  
- 이 데이터를 `insert_db.py`로 MySQL 테이블 `kia_faq`에 저장  
- 실시간 조회는 Streamlit이 DB로부터 직접 읽는 방식 또는 pandas CSV 로딩 방식  
- DB 접속 정보는 `.env` 파일에 저장 (host, port, user, password, db_name 등)

---

## 7. UI 구성 (Streamlit 다중 페이지)

```text
app.py
└─ pages/
   ├─ faq_page.py    ← FAQ 조회
   ├─ page01.py      ← 통계/시각화 페이지
   ├─ page02.py      ← AI 요약 / 챗봇 페이지
   └─ (page03.py 예정)
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