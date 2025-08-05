import streamlit as st
from urllib.parse import quote

# 페이지 설정
st.set_page_config(
    page_title="자동차 등록 분석 대시보드",
    page_icon="🚗",
    layout="centered",
)

# -------------------------------
# 상단 제목 및 설명
# -------------------------------
st.title("🚗 자동차 등록 현황 및 분석 대시보드")
st.markdown("자동차 등록 데이터를 기반으로 한 다양한 사회·경제적 분석 결과를 확인하세요.")

# 조직 로고 (이미지 파일이 있는 경우)# 로고 파일 경로를 여기에 맞게 설정하세요.
st.image(r"./assets/img/image.png", width=800)

st.divider()

# -------------------------------
# 분석 주제와 해당 페이지 키 정의 (파일 이름 기반)
analysis_topics = [
    ("1. 성별에 따른 인구 및 차량 등록의 연관성 분석", "01. Region_Popul_Graph"),
    ("2. 지역별 고용자 수, 소득, 산업 분포 분석", "02. Employment_and_Industry"),
    ("3. 소득, 고용, 산업 구조와 차량 등록의 상관관계 분석", "03. Number_of_Registering_Car"),
    ("4. 전기차 등록 및 충전 인프라 현황", "04. Electric_Car_and_Infra"),
    ("5. 자동차 관련 FAQ 및 참고자료 정리", "FAQ_page")
]

# 버튼 형태로 각 페이지로 이동
for title, filename in analysis_topics:
    encoded_filename = quote(filename)  # 공백 → %20
    with st.container():
        cols = st.columns([0.8, 0.2])  # 제목 : 버튼 비율
        with cols[0]:
            st.markdown(f"#### {title}")
        with cols[1]:
            st.markdown(
                f"""
                <div style='text-align: right; margin-top: 8px;'>
                    <a href='/{encoded_filename}' target='_self'
                    style='font-size: 0.9rem; background-color: #f0f0f0;
                    padding: 6px 12px; border-radius: 6px; text-decoration: none;
                    color: #3366cc;'>Go</a>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)



# -------------------------------
# 조직 및 프로젝트 정보
# -------------------------------
st.markdown("💼 *SK네트웍스 패밀리 AI CAMP 18기 3팀 1차 단위 프로젝트*")