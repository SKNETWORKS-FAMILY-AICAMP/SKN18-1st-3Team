####################################################################################
# 쪽수 없는 버전

import streamlit as st
import pandas as pd

# MySQL 연결 함수
def load_data():
    
    conn = st.connection(
    "project_db", type="sql", autocommit=True
    )

    df=conn.query("SELECT * FROM kia_faq;")

    return pd.DataFrame(df)

# Streamlit 앱 시작
st.set_page_config(page_title="Kia 고객 FAQ", layout="wide")
st.title("📘 KIA 고객 FAQ")

home_button = st.page_link(
    page="./Main_Page.py",
    label="Home",
    icon="🏠"
)

# 데이터 불러오기
df = load_data()

# 검색창
search_query = st.text_input("🔎 검색어를 입력해 주세요.")

# 카테고리 UI
# categories = ["전체"] + sorted(df["category"].unique().tolist()) #버튼
category_list = df["category"].unique().tolist()
selected_category = st.selectbox("카테고리를 선택하세요", options=["전체"] + category_list)

# 버튼 형태 구현
# col_buttons = st.columns(len(categories))
# for idx, col in enumerate(col_buttons):
#     if col.button(categories[idx], key=f"cat_btn_{idx}"):
#         st.session_state.selected_category = categories[idx]

filtered_df = df.copy()

# 선택된 카테고리에 따라 필터링
if selected_category != "전체":
    filtered_df = df[df["category"] == selected_category]
else:
    filtered_df = df

if search_query:
    filtered_df = filtered_df[
        filtered_df["question"].str.contains(search_query, case=False, na=False) |
        filtered_df["answer"].str.contains(search_query, case=False, na=False)
    ]

# 결과 표시
if filtered_df.empty:
    st.info("검색 결과가 없습니다.")
else:
    for _, row in filtered_df.iterrows():
        with st.expander(f"Q. {row['question']}"):
            st.markdown(f"**A.** {row['answer']}")


#####################################################################################

# import streamlit as st
# import pandas as pd

# # MySQL 연결 함수
# def load_data():
#     conn = st.connection("faq_db", type="sql", autocommit=True)
#     df = conn.query("SELECT * FROM kia_faq;")
#     return pd.DataFrame(df)

# # Streamlit 설정
# st.set_page_config(page_title="Kia 고객 FAQ", layout="wide")
# st.title("📘 Kia 고객 FAQ")

# # 데이터 불러오기
# df = load_data()

# # 검색창
# search_query = st.text_input("🔎 검색어를 입력해 주세요.")

# # 카테고리 선택
# category_list = df["category"].unique().tolist()
# selected_category = st.selectbox("카테고리를 선택하세요", options=["전체"] + category_list)

# # 필터링
# filtered_df = df.copy()

# if selected_category != "전체":
#     filtered_df = filtered_df[filtered_df["category"] == selected_category]

# if search_query:
#     filtered_df = filtered_df[
#         filtered_df["question"].str.contains(search_query, case=False, na=False) |
#         filtered_df["answer"].str.contains(search_query, case=False, na=False)
#     ]

# # --------------------------
# # 페이지네이션 설정
# # --------------------------
# PAGE_SIZE = 10
# total_items = len(filtered_df)
# total_pages = (total_items - 1) // PAGE_SIZE + 1

# # 현재 페이지 상태 초기화
# if "current_page" not in st.session_state:
#     st.session_state.current_page = 1

# # 현재 페이지 범위 지정
# start_idx = (st.session_state.current_page - 1) * PAGE_SIZE
# end_idx = start_idx + PAGE_SIZE
# page_df = filtered_df.iloc[start_idx:end_idx]

# # --------------------------
# # 결과 출력
# # --------------------------
# if page_df.empty:
#     st.info("검색 결과가 없습니다.")
# else:
#     for _, row in page_df.iterrows():
#         with st.expander(f"Q. {row['question']}"):
#             st.markdown(f"**A.** {row['answer']}")

# # --------------------------
# # 페이지네이션 (하단 정렬)
# # --------------------------
# st.markdown("---")
# col1, col2, col3 = st.columns([1, 2, 1])

# with col1:
#     st.button("⬅ 이전", key="prev_btn", disabled=st.session_state.current_page == 1, on_click=lambda: st.session_state.update(current_page=st.session_state.current_page - 1))

# with col2:
#     st.markdown(f"<p style='text-align:center;'>페이지 {st.session_state.current_page} / {total_pages}</p>", unsafe_allow_html=True)

# with col3:
#     st.button("다음 ➡", key="next_btn", disabled=st.session_state.current_page == total_pages, on_click=lambda: st.session_state.update(current_page=st.session_state.current_page + 1))

#####################################################################################
# import streamlit as st
# import pandas as pd

# # MySQL 연결
# def load_data():
#     conn = st.connection("faq_db", type="sql", autocommit=True)
#     df = conn.query("SELECT * FROM kia_faq;")
#     return pd.DataFrame(df)

# # 페이지 설정
# st.set_page_config(page_title="Kia 고객 FAQ", layout="wide")
# st.title("📘 Kia 고객 FAQ")

# df = load_data()

# # 검색어 및 카테고리 필터
# search_query = st.text_input("🔎 검색어를 입력해 주세요.")
# category_list = df["category"].unique().tolist()
# selected_category = st.selectbox("카테고리를 선택하세요", options=["전체"] + category_list)

# filtered_df = df.copy()
# if selected_category != "전체":
#     filtered_df = filtered_df[filtered_df["category"] == selected_category]

# if search_query:
#     filtered_df = filtered_df[
#         filtered_df["question"].str.contains(search_query, case=False, na=False) |
#         filtered_df["answer"].str.contains(search_query, case=False, na=False)
#     ]

# # 페이지네이션 세팅
# PAGE_SIZE = 10
# total_items = len(filtered_df)
# total_pages = max((total_items - 1) // PAGE_SIZE + 1, 1)

# if "current_page" not in st.session_state:
#     st.session_state.current_page = 1

# # 페이지 범위 계산
# start_idx = (st.session_state.current_page - 1) * PAGE_SIZE
# end_idx = start_idx + PAGE_SIZE
# page_df = filtered_df.iloc[start_idx:end_idx]

# # 질문 출력
# if page_df.empty:
#     st.info("검색 결과가 없습니다.")
# else:
#     for _, row in page_df.iterrows():
#         with st.expander(f"Q. {row['question']}"):
#             st.markdown(f"**A.** {row['answer']}")

# # ---------------------------
# # 페이지네이션 블록 (5개씩)
# # ---------------------------
# st.markdown("---")
# pagination_cols = st.columns([1, 8, 1])

# # 상태 초기화
# if "page_group_start" not in st.session_state:
#     st.session_state.page_group_start = 1
# if "current_page" not in st.session_state:
#     st.session_state.current_page = 1

# # 콜백 함수: 이전/다음 그룹
# def go_prev_group():
#     st.session_state.page_group_start = max(1, st.session_state.page_group_start - 5)
#     st.session_state.current_page = st.session_state.page_group_start

# def go_next_group():
#     st.session_state.page_group_start = min(
#         st.session_state.page_group_start + 5,
#         (total_pages - 1) // 5 * 5 + 1  # 마지막 그룹 시작 페이지
#     )
#     st.session_state.current_page = st.session_state.page_group_start

# with pagination_cols[1]:
#     st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)

#     # 현재 페이지 그룹 리스트
#     page_group = list(range(
#         st.session_state.page_group_start,
#         min(st.session_state.page_group_start + 5, total_pages + 1)
#     ))

#     button_cols = st.columns(len(page_group) + 2)

#     # ← 이전 그룹 버튼
#     button_cols[0].button("←",
#         disabled=st.session_state.page_group_start == 1,
#         on_click=go_prev_group
#     )

#     # 페이지 번호 버튼들
#     for i, page_num in enumerate(page_group):
#         is_current = page_num == st.session_state.current_page
#         label = f"**{page_num}**" if is_current else str(page_num)
#         if button_cols[i + 1].button(label, key=f"page_{page_num}"):
#             st.session_state.current_page = page_num

#     # → 다음 그룹 버튼
#     has_next = st.session_state.page_group_start + 5 <= total_pages
#     button_cols[-1].button("→",
#         disabled=not has_next,
#         on_click=go_next_group
#     )

#     st.markdown("</div>", unsafe_allow_html=True)