# 자동차 등록 현황 및 전기차 수도권 사고위험

import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import json


capital = ["서울","인천","경기"]

# MySQL 연결 함수
def load_data(table_name):
    
    conn = st.connection(
    "project_db", type="sql", autocommit=True
    )

    df=conn.query(f"SELECT * FROM {table_name};")

    return pd.DataFrame(df)

############### 자동차 등록 현황 ###############
# Streamlit 앱
# st.title("자동차 등록 통계 시각화")

# table_name = "registered_car"
# df = load_data(table_name)
# df["year"] = df["year"].astype(int)
# df["value"] = df["value"].astype(str).str.replace(",", "")
# df["value"] = pd.to_numeric(df["value"], errors="coerce")

# # 지표 선택
# metrics_list = df["metrics"].unique().tolist()
# selected_metric = st.selectbox("지표 선택", metrics_list)

# # 선택된 지표에 대한 데이터 필터링
# filtered_df = df[df["metrics"] == selected_metric].sort_values("year")

# # 그래프 출력
# # Altair 차트로 교체
# line_chart = (
#     alt.Chart(filtered_df)
#     .mark_line(point=True)
#     .encode(
#         x=alt.X("year:O", title="연도",axis=alt.Axis(labelAngle=-45)),
#         y=alt.Y("value:Q", title="전기",scale=alt.Scale(domain=[1800, 3000])),
#         tooltip=["year", "value"]
#     )
#     .properties(
#         width=700,
#         height=400,
#         title=f"{selected_metric} 연도별 추이"
#     )
# )


# st.altair_chart(line_chart, use_container_width=True)
# # st.write(df.dtypes)

# # 데이터 테이블도 같이 보여주기
# with st.expander("데이터 보기"):
#     st.dataframe(filtered_df)

############### 면적 당 건물/인구 수 ###############

# DB 테이블 로드
st.header("[면적 당 건물/인구 수]")
table_name = "cal_by_region"
df = load_data(table_name)

# 위치 정보 로드 (지역명 -> [위도, 경도])
with open("./data/geo.json", "r", encoding="utf-8") as f:
    location_coords = json.load(f)

# 지표 선택
metric = st.radio("시각화할 지표를 선택하세요:", ("인구 수", "건물 수"))
metric_col = "cnt_popul" if metric == "인구 수" else "cnt_building"
unit = "명" if metric == "인구 수" else "동"

# 지도 생성 (줌아웃 제한 포함)
m = folium.Map(
    location=[36.5, 127.8],
    zoom_start=7,
    min_zoom=6,  # 줌아웃 제한
    max_zoom=10,
    max_bounds=True
)
m.fit_bounds([[33.0, 124.0], [39.5, 132.0]])  # 한반도 전체 범위

# 값 정규화 (0~1로)
max_value = df[metric_col].max()
heat_data = []

for _, row in df.iterrows():
    region = row["region"]
    coords = location_coords.get(region)
    if not coords:
        continue
    norm_value = row[metric_col] / max_value  # 정규화
    heat_data.append([coords[0], coords[1], norm_value])

    # 값 텍스트 표시
    folium.Marker(
        location=coords,
        icon=folium.DivIcon(html=f"""
            <div style="font-size:10pt; color:black; font-weight:bold; text-align:center;">
                {row[metric_col]:.1f}
            </div>
        """)
    ).add_to(m)

# 히트맵 추가
HeatMap(heat_data, radius=20, blur=20, max_zoom=6).add_to(m)

# 지도 표시
folium_static(m)

# # 컬럼명 변경, 반올림, id 제거, 인덱스 제거
# df_display = df.drop(columns=["id"]) \
#     .rename(columns={"cnt_building": "건물 수(동)", "cnt_popul": "인구 수(명)"}) \
#         .reset_index(drop=True)\
#             .round(2) \
            

# # 표 출력
# st.subheader("📊 지역별 등록대수 및 비율")
# st.table(
#     df_display.style.format({
#         "건물 수(동)": "{:,.2f}",
#         "인구 수(명)": "{:,.2f}"
#     }).set_properties(**{'text-align': 'center'}).set_table_styles(
#         [dict(selector='th', props=[('text-align', 'center')])]
#     )
# )


st.write("")
st.write("")
st.write("")

############### 전기차 등록수 ###############

st.header("[면적 당 전기차 등록 수]")
table_name = "register_electricity_car"
df = load_data(table_name)

df["is_capital"] = df["region"].isin(capital)

# 등록수 바 그래프
bar_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("region:N", title="지역", axis=alt.Axis(labelAngle=-45)),
    y=alt.Y("register_by_region:Q", title="면적당 전기차 등록수 (대/km²)"),
    color=alt.condition(
        alt.datum.is_capital,
        alt.value("orange"),  # 수도권은 주황색
        alt.value("steelblue")  # 그 외 지역은 파란색
    ),
    tooltip=["region", "register_by_region"]
).properties(title="지역별 면적당 전기차 등록수")

st.altair_chart(bar_chart, use_container_width=True)

st.write("")
st.write("")
st.write("")


############### 전기차 증가량 ###############

st.header("[면적 당 전기차 증가량]")
table_name = "add_electricity_car"
df = load_data(table_name)

df["month"] = pd.to_datetime(df["month"])

df["month_only"] = pd.to_datetime(df["month"]).dt.month
df["month_only"] = df["month_only"]

# 수도권 지역만 필터링
df["group"] = df["region"].apply(lambda x: "수도권" if x in capital else "비수도권")

# 월별 평균값 계산
grouped_df = df.groupby(["month_only", "group"])["add_by_region"].mean().reset_index()

# 선 그래프
# groupby된 데이터는 그대로 사용
chart = alt.Chart(grouped_df).mark_line(point=True).encode(
    x=alt.X("month_only:O", title="월", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("add_by_region:Q", title="면적당 전기차 증가량 (대/km²)"),
    color=alt.Color("group:N", title="구분"),
    tooltip=["month_only", "group", "add_by_region"]
).properties(title="2024년 수도권 vs 비수도권 면적당 전기차 증가량 추이")

st.altair_chart(chart, use_container_width=True)

st.write("")
st.write("")
st.write("")


############### 화재 발생률 ###############

st.header("🔥 면적 당 전기차 배터리 화재 발생률 변화 (2021→2023)")

table_name = "fire_per"
df = load_data(table_name)

df = df.sort_values(by="cnt_fire", ascending=False)
max_val = df["cnt_fire"].max()

# # 막대 그래프 그리기
# for _, row in df.iterrows():
#     # 막대 길이 계산 (불 개수)
#     fire_ratio = int((row["cnt_fire"] / max_val) * 30)  # 최대 30개 불
#     bar = "🔥" * fire_ratio

#     # 출력 (수치는 표시하지 않음)
#     st.markdown(f"""
#     <div style='display: flex; align-items: center; margin-bottom: 4px;'>
#         <div style='width: 60px; font-weight: bold;'>{row['region']}</div>
#         <div style='font-size: 20px; line-height: 1;'>{bar}</div>
#     </div>
#     """, unsafe_allow_html=True)


#시각화
#🔥이모지로 bar 텍스트 생성
max_fire = df["cnt_fire"].max()
df["bar"] = df["cnt_fire"].apply(lambda x: "🔥" * int((x / max_fire) * 20))

# Plotly 그래프
fig = go.Figure()

fig.add_trace(go.Bar(
    x=df["region"],
    y=df["cnt_fire"],
    text=df["bar"],
    textposition='outside',
    marker_color='orangered'
))

fig.update_layout(
    xaxis_title="지역",
    height=500
)

st.plotly_chart(fig, use_container_width=True)


############### 🔌 전기차 충전기 등록 수 변화 (연도별) ###############

# 데이터 불러오기
st.header("🔌 전기차 충전기 등록 수 변화 (연도별)")
table_name = "charge_by_region"
df = load_data(table_name)

# 데이터 전처리
df["year"] = df["year"].astype(str)

# 막대그래프 (연도별 세로 분할, 지역별 옆으로)
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("region:N", title="지역", sort="-y"),
    y=alt.Y("cnt_charge:Q", title="전기차 충전기 등록 수"),
    color=alt.Color("region:N", legend=None),
    tooltip=["year", "region", "cnt_charge"]
).properties(
    width=200,
    height=400
).facet(
    column=alt.Column("year:N", title=None)
)

st.altair_chart(chart, use_container_width=True)