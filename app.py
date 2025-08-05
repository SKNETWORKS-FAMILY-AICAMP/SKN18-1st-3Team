# import streamlit as st

# st.title("SK Networks 18기 3팀")
# st.title("전국 자동차 등록 현황 및 기업 FAQ 조회 시스템")

# st.set_page_config(
#     layout="wide",
#     initial_sidebar_state="auto"  # "expanded", "collapsed", "auto"
# )

# page1_button = st.page_link(
#     page="pages/faq_page.py",
#     label = "KIA FAQ",
#     icon="📘"
#     )

# page2_button = st.page_link(
#     page="pages/page02.py",
#     label = "전기차의 상용화 예측 동향",
#     icon="🔌"
#     )


# page3_button = st.page_link(
#     page="pages/page02.py",
#     label = "Page 2",
#     icon="2️⃣",
#     disabled=True
#     )

import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="전국 자동차 등록 및 FAQ 시스템",
    layout="centered",
    initial_sidebar_state="auto"
)

# 로고 및 제목
st.image("assets/skn_logo.png", width =1000)
st.markdown("## SK Networks 18기 3팀 단위 프로젝트")
st.markdown("## 🚗 전국 자동차 등록 현황 및 기업 FAQ 조회 시스템")

st.markdown("---")

# 페이지 링크 버튼들
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.page_link("pages/01. Region_Popul_Graph.py", icon="📘")
    

with col2:
    st.page_link("pages/02. Employment_and_Industry.py", label="전기차의 상용화 예측 동향", icon="🔌")

with col3:
    st.page_link("pages/03. Number_of_Registering_Car.py", label="Page 2", icon="2️⃣", disabled=True)

with col4:
    pass
