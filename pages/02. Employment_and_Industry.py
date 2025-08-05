# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.font_manager as fm
# import platform
# import folium
# from streamlit_folium import st_folium
# import numpy as np
# import base64
# from io import BytesIO
# import plotly.express as px
# import plotly.graph_objects as go

# # 한글 폰트 설정 (운영체제별)
# def set_korean_font():
#     system = platform.system()
#     if system == "Windows":
#         plt.rcParams['font.family'] = 'Malgun Gothic'
#     elif system == "Darwin":  # macOS
#         plt.rcParams['font.family'] = 'AppleGothic'
#     else:  # Linux
#         plt.rcParams['font.family'] = 'DejaVu Sans'
    
#     plt.rcParams['axes.unicode_minus'] = False

# set_korean_font()

# # 📁 데이터 로드 (엑셀 or CSV에서 불러오거나 변수 정의)
# # 여기서는 예시로 전처리된 df_total, df_industry 사용 가정

# @st.cache_data
# def load_data():
#     # df_total: 전국 및 시도별 전체 고용자 수 (2021~2023)
#     # df_industry: 시도별 산업분류별 고용자 수
#     df_total = pd.read_csv("./data/df_total.csv")  # columns: 지역, 2021, 2022, 2023
#     df_industry = pd.read_csv("./data/df_industry.csv")  # columns: 지역, 산업분류, 2021, 2022, 2023
#     return df_total, df_industry

# df_total, df_industry = load_data()

# st.set_page_config(
#     page_title="전국 연도별 고용자 수 및 증가율",
#     layout="centered",
#     initial_sidebar_state="auto"
# )

# # 📌 1. 전국 연도별 고용자 수 및 증가율
# st.header("1. 전국 연도별 고용자 수 및 증가율")

# df_korea = df_total[df_total['지역'] == '전국'].set_index('지역')
# years = ['2021', '2022', '2023']  # 문자열로 변경
# values = df_korea.loc['전국', years]
# growth = values.pct_change() * 100

# # 만 단위로 변환
# values_10k = values / 10000

# # Plotly를 사용한 선형 그래프 (y축 범위 설정)
# fig1 = go.Figure()
# fig1.add_trace(go.Scatter(
#     x=years,
#     y=values_10k,
#     mode='lines+markers',
#     name='전국 고용자 수',
#     line=dict(color='blue', width=3),
#     marker=dict(size=8)
# ))

# fig1.update_layout(
#     title='전국 연도별 고용자 수 (만 명)',
#     xaxis_title='연도',
#     yaxis_title='고용자 수 (만 명)',
#     yaxis=dict(range=[1500, 2500], dtick=200),
#     xaxis=dict(tickmode='array', tickvals=years, ticktext=years),
#     height=400
# )

# st.plotly_chart(fig1, use_container_width=True)

# st.dataframe(pd.DataFrame({
#     '고용자 수 (만 명)': values_10k.astype(int),
#     '전년 대비 증가율 (%)': growth.round(2)
# }))

# # 📌 2. 지역별 고용자 수 (막대 그래프)
# st.header("2. 지역별 전체 고용자 수 (2021–2023)")

# df_region = df_total[df_total['지역'] != '전국'].set_index('지역')
# # 만 단위로 변환
# df_region_10k = df_region / 10000

# # Plotly를 사용한 지역별 막대 그래프
# fig2 = go.Figure()

# for region in df_region_10k.index:
#     fig2.add_trace(go.Bar(
#         x=years,
#         y=df_region_10k.loc[region],
#         name=region,
#         text=df_region_10k.loc[region].astype(int),
#         textposition='auto'
#     ))

# fig2.update_layout(
#     title='지역별 고용자 수 변화 (만 명)',
#     xaxis_title='연도',
#     yaxis_title='고용자 수 (만 명)',
#     yaxis=dict(range=[0, 500], dtick=100),
#     xaxis=dict(tickmode='array', tickvals=years, ticktext=years),
#     height=500,
#     showlegend=True,
#     barmode='group'
# )

# st.plotly_chart(fig2, use_container_width=True)

# st.dataframe(df_region_10k.astype(int))

# # 📌 3. 각 지역별 주 산업 (3개년 평균 기준 상위 3개 비율로 원형 그래프)
# st.header("3. 각 지역별 주 산업(3개년 평균)")

# selected_region = st.selectbox("지역 선택", df_industry["지역"].unique())

# df_selected = df_industry[df_industry["지역"] == selected_region].copy()
# df_selected["평균"] = df_selected[years].mean(axis=1)  # 문자열 리스트 사용
# df_selected = df_selected.sort_values("평균", ascending=False)

# total = df_selected["평균"].sum()
# df_selected["비율(%)"] = (df_selected["평균"] / total * 100).round(2)

# # 원형 그래프 (글자 겹침 방지)
# fig, ax = plt.subplots(figsize=(14, 10))

# # 상위 10개만 표시하고 나머지는 '기타'로 묶기
# top_10 = df_selected.head(10)
# if len(df_selected) > 10:
#     others_sum = df_selected.iloc[10:]['평균'].sum()
#     others_ratio = (others_sum / total * 100).round(2)
    
#     # 상위 10개 + 기타로 데이터 준비
#     plot_data = pd.concat([
#         top_10,
#         pd.DataFrame({
#             '산업분류': ['기타'],
#             '평균': [others_sum],
#             '비율(%)': [others_ratio]
#         })
#     ])
# else:
#     plot_data = df_selected

# wedges, texts, autotexts = ax.pie(plot_data["비율(%)"], 
#                                 labels=plot_data["산업분류"], 
#                                 autopct="%1.1f%%", 
#                                 startangle=90,
#                                 pctdistance=0.85)

# # 텍스트 크기 조정 및 위치 최적화 (3포인트로 변경)
# for text in texts:
#     text.set_fontsize(10)
#     text.set_horizontalalignment('center')
# for autotext in autotexts:
#     autotext.set_fontsize(10)
#     autotext.set_color('white')
#     autotext.set_weight('bold')

# ax.axis('equal')
# st.pyplot(fig)

# # 표로도 출력 (만 단위로 변환)
# df_selected_display = df_selected.copy()
# df_selected_display["평균 (만 명)"] = (df_selected_display["평균"] / 10000).astype(int)
# st.dataframe(df_selected_display[["산업분류", "평균 (만 명)", "비율(%)"]].reset_index(drop=True))

# # 📌 4. 지도에서 지역별 Top 3 산업군 시각화
# st.header("4. 지역별 Top 3 산업군")

# # 각 지역별 Top 3 산업 계산
# def get_top3_industries(df, region):
#     region_data = df[df['지역'] == region].copy()
#     region_data['평균'] = region_data[years].mean(axis=1)
#     return region_data.nlargest(3, '평균')[['산업분류', '평균']]

# # 원형 그래프를 이미지로 변환하는 함수
# def create_pie_chart_image(data, title):
#     fig, ax = plt.subplots(figsize=(6, 4))
    
#     # 산업명을 짧게 표시
#     labels = []
#     for industry in data['산업분류']:
#         # 괄호 앞부분만 사용하고 길면 줄임
#         short_name = industry.split('(')[0]
#         if len(short_name) > 15:
#             short_name = short_name[:15] + '...'
#         labels.append(short_name)
    
#     wedges, texts, autotexts = ax.pie(data['평균'], 
#                                     labels=labels, 
#                                     autopct='%1.1f%%', 
#                                     startangle=90)
    
#     # 텍스트 크기 조정 (더 크게 변경)
#     for text in texts:
#         text.set_fontsize(12)
#     for autotext in autotexts:
#         autotext.set_fontsize(10)
#         autotext.set_color('white')
#         autotext.set_weight('bold')
    
#     ax.set_title(title, fontsize=20, pad=10)
#     ax.axis('equal')
    
#     # 이미지를 base64로 인코딩
#     img_buffer = BytesIO()
#     fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
#     img_buffer.seek(0)
#     img_str = base64.b64encode(img_buffer.getvalue()).decode()
#     plt.close(fig)
    
#     return img_str

# # 한국 지도 중심 좌표 및 경계 설정
# korea_bounds = [[33.0, 124.5], [38.5, 132.0]]  # 한국 경계

# # 지도 생성 (한국으로 고정)
# m = folium.Map(
#     location=[36.5, 127.5], 
#     zoom_start=7, 
#     tiles='OpenStreetMap',
#     max_bounds=korea_bounds,
#     min_zoom=6,
#     max_zoom=10
# )

# # 지역별 좌표 (대략적인 위치)
# region_coords = {
#     '서울특별시': [37.5665, 126.9780],
#     '부산광역시': [35.1796, 129.0756],
#     '대구광역시': [35.8714, 128.6014],
#     '인천광역시': [37.4563, 126.7052],
#     '광주광역시': [35.1595, 126.8526],
#     '대전광역시': [36.3504, 127.3845],
#     '울산광역시': [35.5384, 129.3114],
#     '세종특별자치시': [36.4870, 127.2820],
#     '경기도': [37.4138, 127.5183],
#     '강원특별자치도': [37.8228, 128.1555],
#     '충청북도': [36.8, 127.7],
#     '충청남도': [36.6, 126.9],
#     '전북특별자치도': [35.7175, 127.1530],
#     '전라남도': [34.8679, 126.9910],
#     '경상북도': [36.4919, 128.8889],
#     '경상남도': [35.4606, 128.2132],
#     '제주특별자치도': [33.4996, 126.5312]
# }

# # 각 지역에 마커 추가
# for region in df_industry['지역'].unique():
#     if region == '전국':
#         continue
    
#     if region in region_coords:
#         coords = region_coords[region]
#         top3 = get_top3_industries(df_industry, region)
        
#         # 원형 그래프 생성
#         pie_chart_img = create_pie_chart_image(top3, f"{region} Top 3 산업군")
        
#         # 팝업 내용 생성 (원형 그래프 포함)
#         popup_content = f"""
#         <div style="width: 400px; text-align: center;">
#             <h3 style="margin-bottom: 10px; color: #1f77b4;">{region}</h3>
#             <img src="data:image/png;base64,{pie_chart_img}" 
#             style="width: 100%; max-width: 350px; height: auto;">
#             <div style="margin-top: 10px; font-size: 12px; color: #666;">
#                 <strong>Top 3 산업군:</strong><br>
#         """
        
#         for idx, row in top3.iterrows():
#             industry_name = row['산업분류'].split('(')[0]
#             popup_content += f"• {industry_name}<br>"
        
#         popup_content += "</div></div>"
        
#         folium.Marker(
#             location=coords,
#             popup=folium.Popup(popup_content, max_width=450),
#             tooltip=region,
#             icon=folium.Icon(color='red', icon='info-sign')
#         ).add_to(m)

# # 지도 표시
# st_folium(m, width=800, height=600)

# # 📌 5. 지역별 Top 3 산업 요약
# st.header("5. 지역별 Top 3 산업 요약")

# # 테이블용 지역 필터링
# table_regions = [region for region in df_industry['지역'].unique() if region != '전국']
# selected_table_regions = st.multiselect(
#     "표시할 지역을 선택하세요",
#     options=table_regions,
#     default=table_regions,
#     help="테이블에 표시할 지역을 선택하세요. 선택하지 않으면 모든 지역이 표시됩니다."
# )

# # 선택된 지역이 없으면 모든 지역 표시
# if not selected_table_regions:
#     selected_table_regions = table_regions

# summary_data = []
# for region in df_industry['지역'].unique():
#     if region == '전국' or region not in selected_table_regions:
#         continue
    
#     top3 = get_top3_industries(df_industry, region)
#     for idx, row in top3.iterrows():
#         summary_data.append({
#             '지역': region,
#             '순위': idx + 1,
#             '산업분류': row['산업분류'],
#             '평균 고용자 수 (만 명)': int(row['평균'] / 10000)
#         })

# summary_df = pd.DataFrame(summary_data)
# st.dataframe(summary_df, use_container_width=True)


# ✅ 기존 연산 코드를 유지하면서, 전체적으로 디자인 요소(제목 상자, 구분선, 여백 등)를 추가한 최종 Streamlit 앱 코드입니다.
# 참고: Streamlit v1.27 이상 기준

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import folium
from streamlit_folium import st_folium
import numpy as np
import base64
from io import BytesIO
import plotly.graph_objects as go

# ✅ 한글 폰트 설정 (운영체제별)
def set_korean_font():
    system = platform.system()
    if system == "Windows":
        plt.rcParams['font.family'] = 'Malgun Gothic'
    elif system == "Darwin":
        plt.rcParams['font.family'] = 'AppleGothic'
    else:
        plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

# ✅ 데이터 로드
@st.cache_data
def load_data():
    df_total = pd.read_csv("./data/df_total.csv")
    df_industry = pd.read_csv("./data/df_industry.csv")
    return df_total, df_industry

df_total, df_industry = load_data()

st.set_page_config(
    page_title="전국 고용 통계 분석 대시보드",
    layout="centered"
)

# ✅ 헤더 스타일
st.markdown("""
    <div style='background-color:#1f77b4; padding: 1rem 2rem; border-radius: 10px;'>
        <h1 style='color: white;'>📊 전국 고용 통계 분석 대시보드</h1>
        <p style='color: white; font-size: 16px;'>2021~2023년 기준 전국 및 지역별 고용자 수, 산업별 비중을 시각화합니다.</p>
    </div>
    <br>
""", unsafe_allow_html=True)

# =============================================
# 📌 1. 전국 고용자 수 변화
# =============================================
st.subheader("1️⃣ 전국 연도별 고용자 수 및 증가율")

years = ['2021', '2022', '2023']
df_korea = df_total[df_total['지역'] == '전국'].set_index('지역')
values = df_korea.loc['전국', years]
growth = values.pct_change() * 100
values_10k = values / 10000

fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=years,
    y=values_10k,
    mode='lines+markers',
    name='전국 고용자 수',
    line=dict(color='blue', width=3),
    marker=dict(size=8)
))
fig1.update_layout(
    title='전국 고용자 수 (만 명)',
    xaxis_title='연도',
    yaxis_title='고용자 수 (만 명)',
    yaxis=dict(range=[1500, 2500], dtick=200),
    height=400
)

st.plotly_chart(fig1, use_container_width=True)

with st.expander("📋 상세 수치 보기"):
    st.dataframe(pd.DataFrame({
        '고용자 수 (만 명)': values_10k.astype(int),
        '전년 대비 증가율 (%)': growth.round(2)
    }))

st.markdown("---")

# =============================================
# 📌 2. 지역별 고용자 수
# =============================================
st.subheader("2️⃣ 지역별 전체 고용자 수 (2021–2023)")

df_region = df_total[df_total['지역'] != '전국'].set_index('지역')
df_region_10k = df_region / 10000

fig2 = go.Figure()
for region in df_region_10k.index:
    fig2.add_trace(go.Bar(
        x=years,
        y=df_region_10k.loc[region],
        name=region,
        text=df_region_10k.loc[region].astype(int),
        textposition='auto'
    ))
fig2.update_layout(
    title='지역별 고용자 수 변화 (만 명)',
    xaxis_title='연도',
    yaxis_title='고용자 수 (만 명)',
    yaxis=dict(range=[0, 500], dtick=100),
    height=500,
    showlegend=True,
    barmode='group'
)

st.plotly_chart(fig2, use_container_width=True)

with st.expander("📋 지역별 상세 수치 보기"):
    st.dataframe(df_region_10k.astype(int))

st.markdown("---")

# =============================================
# 📌 3. 각 지역별 주 산업
# =============================================
st.subheader("3️⃣ 각 지역별 주 산업 (3개년 평균)")

selected_region = st.selectbox("지역 선택", df_industry["지역"].unique())
df_selected = df_industry[df_industry["지역"] == selected_region].copy()
df_selected["평균"] = df_selected[years].mean(axis=1)
df_selected = df_selected.sort_values("평균", ascending=False)
total = df_selected["평균"].sum()
df_selected["비율(%)"] = (df_selected["평균"] / total * 100).round(2)

# 원형 그래프
fig, ax = plt.subplots(figsize=(8, 6))
top_10 = df_selected.head(10)
if len(df_selected) > 10:
    others_sum = df_selected.iloc[10:]['평균'].sum()
    others_ratio = (others_sum / total * 100).round(2)
    plot_data = pd.concat([
        top_10,
        pd.DataFrame({'산업분류': ['기타'], '평균': [others_sum], '비율(%)': [others_ratio]})
    ])
else:
    plot_data = df_selected

ax.pie(plot_data["비율(%)"], labels=plot_data["산업분류"], autopct="%1.1f%%", startangle=90)
ax.axis('equal')
st.pyplot(fig)

with st.expander("📋 산업별 상세 수치 보기"):
    df_selected_display = df_selected.copy()
    df_selected_display["평균 (만 명)"] = (df_selected_display["평균"] / 10000).astype(int)
    st.dataframe(df_selected_display[["산업분류", "평균 (만 명)", "비율(%)"]].reset_index(drop=True))

st.markdown("---")

# =============================================
# 📌 4. 지도 시각화 (Top 3 산업)
# =============================================
st.subheader("4️⃣ 지역별 Top 3 산업군 (지도 시각화)")

def get_top3_industries(df, region):
    region_data = df[df['지역'] == region].copy()
    region_data['평균'] = region_data[years].mean(axis=1)
    return region_data.nlargest(3, '평균')[['산업분류', '평균']]

def create_pie_chart_image(data, title):
    fig, ax = plt.subplots(figsize=(6, 4))
    labels = []
    for industry in data['산업분류']:
        short_name = industry.split('(')[0]
        if len(short_name) > 15:
            short_name = short_name[:15] + '...'
        labels.append(short_name)
    ax.pie(data['평균'], labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close(fig)
    return img_str

region_coords = {
    '서울특별시': [37.5665, 126.9780], '부산광역시': [35.1796, 129.0756],
    '대구광역시': [35.8714, 128.6014], '인천광역시': [37.4563, 126.7052],
    '광주광역시': [35.1595, 126.8526], '대전광역시': [36.3504, 127.3845],
    '울산광역시': [35.5384, 129.3114], '세종특별자치시': [36.4870, 127.2820],
    '경기도': [37.4138, 127.5183], '강원특별자치도': [37.8228, 128.1555],
    '충청북도': [36.8, 127.7], '충청남도': [36.6, 126.9],
    '전북특별자치도': [35.7175, 127.1530], '전라남도': [34.8679, 126.9910],
    '경상북도': [36.4919, 128.8889], '경상남도': [35.4606, 128.2132],
    '제주특별자치도': [33.4996, 126.5312]
}

m = folium.Map(location=[36.5, 127.5], zoom_start=7)
for region in df_industry['지역'].unique():
    if region == '전국' or region not in region_coords:
        continue
    coords = region_coords[region]
    top3 = get_top3_industries(df_industry, region)
    pie_chart_img = create_pie_chart_image(top3, f"{region} Top 3 산업군")
    popup_content = f"""
    <div style='width: 300px; text-align: center;'>
        <h4>{region}</h4>
        <img src='data:image/png;base64,{pie_chart_img}' style='width: 90%;'>
    </div>
    """
    folium.Marker(
        location=coords,
        popup=folium.Popup(popup_content, max_width=400),
        tooltip=region,
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

st_folium(m, width=800, height=600)

st.markdown("---")

# =============================================
# 📌 5. 요약 테이블
# =============================================
st.subheader("5️⃣ 지역별 Top 3 산업 요약")

selected_table_regions = st.multiselect(
    "표시할 지역 선택",
    options=[r for r in df_industry['지역'].unique() if r != '전국'],
    default=[r for r in df_industry['지역'].unique() if r != '전국']
)

summary_data = []
for region in selected_table_regions:
    top3 = get_top3_industries(df_industry, region)
    for idx, row in top3.iterrows():
        summary_data.append({
            '지역': region,
            '순위': idx + 1,
            '산업분류': row['산업분류'],
            '평균 고용자 수 (만 명)': int(row['평균'] / 10000)
        })

summary_df = pd.DataFrame(summary_data)
st.dataframe(summary_df, use_container_width=True)

st.markdown("---")

st.caption("데이터 출처: 통계청, 고용노동부, 자체 가공")
