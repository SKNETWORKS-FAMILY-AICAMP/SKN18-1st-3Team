# from socket import MSG_BCAST
# import streamlit as st
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# from scipy.stats import pearsonr
# import statsmodels.formula.api as smf   # (다중회귀 확인용·선택)
# import platform
# import re
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

# st.set_page_config(
#     page_title="📊차량 등록수 vs 고용/소득/산업분포",
#     layout="centered",
#     initial_sidebar_state="auto"
# )

# st.markdown("""
#     <h2 style='text-align: center;'>📊 차량 등록수 <span style='color:#333;'>vs</span> 고용/소득/산업분포</h2>
# """, unsafe_allow_html=True)

# # ──────────────────────────────────────────────────────────────
# # 0. 헬퍼 함수 ─ p-value 형식 지정
# # ──────────────────────────────────────────────────────────────
# def format_p(val: float) -> str:
#     """p-value를 1e-5 미만이면 지수표기로, 아니면 소수점 3째 자리까지"""
#     return f"{val:.3e}" if val < 1e-5 else f"{val:.3f}"


# # ──────────────────────────────────────────────────────────────
# # 1. 데이터 로딩
# # ──────────────────────────────────────────────────────────────
# @st.cache_data
# def load_data():
#     df_total    = pd.read_csv("./data/df_total.csv")     # 고용자 수
#     df_income   = pd.read_csv("./data/df_income.csv")    # 1인당 소득
#     df_vehicle  = pd.read_csv("./data/df_vehicle.csv")   # 차량 등록수
#     df_industry = pd.read_csv("./data/df_industry.csv")  # 산업별 종사자 수
#     return df_total, df_income, df_vehicle, df_industry

# df_total, df_income, df_vehicle, df_industry = load_data()

# # ──────────────────────────────────────────────────────────────
# # 2. 3개년 평균 파생 컬럼 (절대값)
# # ──────────────────────────────────────────────────────────────
# df_total["평균_고용자"] = df_total[["2021", "2022", "2023"]].mean(axis=1) / 1e4  # 만 명
# df_income["평균_소득"]  = df_income[["2021_소득", "2022_소득", "2023_소득"]].mean(axis=1)
# df_vehicle["평균_차량"] = df_vehicle[["2021_차량", "2022_차량", "2023_차량"]].mean(axis=1) / 1e4  # 만 대
# df_industry["평균"]     = df_industry[["2021", "2022", "2023"]].mean(axis=1) / 1e4  # 만 명

# # ──────────────────────────────────────────────────────────────
# # 3-1. 차량 등록수 vs 고용자 수 (절대값)
# # ──────────────────────────────────────────────────────────────
# st.subheader("1. 차량 등록 수 vs 고용자 수 (2021~2023 평균)")

# df1 = (
#     df_total[["지역", "평균_고용자"]]
#     .merge(df_vehicle[["지역", "평균_차량"]], on="지역")
# )
# r1, p1 = pearsonr(df1["평균_고용자"], df1["평균_차량"])
# p1_str = format_p(p1)

# fig1, ax1 = plt.subplots(figsize=(10, 6))
# sns.regplot(x="평균_고용자", y="평균_차량", data=df1, ax=ax1, scatter=False)
# ax1.scatter(df1["평균_고용자"], df1["평균_차량"], alpha=0.7)

# for _, row in df1.iterrows():
#     name = row["지역"]
#     if name.endswith(("특별시", "광역시")):
#         name = name[:-3]
#     elif name.endswith("특별자치시"):
#         name = name[:-5]
#     elif name.endswith("특별자치도"):
#         name = name[:-5]
#     ax1.annotate(name, (row["평균_고용자"], row["평균_차량"]),
#                 xytext=(5, 5), textcoords='offset points', fontsize=8)

# ax1.set_xlabel("평균 고용자 수 (만 명)")
# ax1.set_ylabel("평균 차량 등록 수 (만 대)")
# ax1.set_title(f"상관계수 r = {r1:.2f} (p = {p1_str})")
# st.pyplot(fig1)

# df1_display = df1.copy()
# df1_display.columns = ["지역", "평균 고용자 수 (만 명)", "평균 차량 등록 수 (만 대)"]
# df1_display["상관계수 (r)"] = f"{r1:.3f}"
# df1_display["p-value"]      = p1_str
# st.dataframe(df1_display, hide_index=True)

# # ──────────────────────────────────────────────────────────────
# # 3-2. 차량 등록수 vs 1인당 소득 (절대값)
# # ──────────────────────────────────────────────────────────────
# st.subheader("2. 차량 등록 수 vs 평균 1인당 지역소득 (2021~2023 평균)")

# df2 = (
#     df_income[["지역", "평균_소득"]]
#     .merge(df_vehicle[["지역", "평균_차량"]], on="지역")
# )
# r2, p2 = pearsonr(df2["평균_소득"], df2["평균_차량"])
# p2_str = format_p(p2)

# fig2, ax2 = plt.subplots(figsize=(10, 6))
# sns.regplot(x="평균_소득", y="평균_차량", data=df2, ax=ax2, scatter=False)
# ax2.scatter(df2["평균_소득"], df2["평균_차량"], alpha=0.7)

# for _, row in df2.iterrows():
#     name = row["지역"]
#     if name.endswith(("특별시", "광역시")):
#         name = name[:-3]
#     elif name.endswith("특별자치시"):
#         name = name[:-5]
#     elif name.endswith("특별자치도"):
#         name = name[:-5]
#     ax2.annotate(name, (row["평균_소득"], row["평균_차량"]),
#                 xytext=(5, 5), textcoords='offset points', fontsize=8)

# ax2.set_xlabel("평균 1인당 소득 (천 원)")
# ax2.set_ylabel("평균 차량 등록 수 (만 대)")
# ax2.set_title(f"상관계수 r = {r2:.2f} (p = {p2_str})")
# st.pyplot(fig2)

# df2_display = df2.copy()
# df2_display.columns = ["지역", "평균 1인당 소득 (천 원)", "평균 차량 등록 수 (만 대)"]
# df2_display["상관계수 (r)"] = f"{r2:.3f}"
# df2_display["p-value"]      = p2_str
# st.dataframe(df2_display, hide_index=True)



# from statsmodels.stats.outliers_influence import variance_inflation_factor

# # (1) 데이터 로드
# df_industry = pd.read_csv("./data/df_industry.csv")  # 열: 지역, 산업분류, 2021, 2022, 2023
# df_vehicle = pd.read_csv("./data/df_vehicle.csv")    # 열: 지역, 2021, 2022, 2023

# # (2) long 포맷으로 변환
# df_long = df_industry.melt(id_vars=["지역", "산업분류"], var_name="연도", value_name="종사자수")
# df_long["산업코드"] = df_long["산업분류"].str.extract(r"(^[A-Z]\.)")

# # (3) 산업 대분류 그룹 정의
# big_code = {
#     "제조_에너지_건설": ["B.", "C.", "D.", "E.", "F."],
#     "유통_물류":         ["G.", "H."],
#     "민간서비스_금융":   ["I.", "J.", "K.", "L.", "M.", "N.", "R.", "S."],
#     "공공_사회서비스":   ["O.", "P.", "Q."]
# }

# # (4) 산업 비중 계산
# total = df_long.groupby(["지역", "연도"])["종사자수"].sum().reset_index(name="전체종사자수")
# df_long = df_long.merge(total, on=["지역", "연도"])
# df_long["비중"] = df_long["종사자수"] / df_long["전체종사자수"]

# # (5) 피벗: 지역-연도별 산업코드 비중
# pivot = df_long.pivot_table(index=["지역", "연도"], columns="산업코드", values="비중", aggfunc="sum")

# # (6) 산업 대분류 비중 계산
# for group, codes in big_code.items():
#     matched = [col for col in pivot.columns if col in codes]
#     pivot[group] = pivot[matched].sum(axis=1)

# # (7) 3개년 평균 계산
# df_avg_industry = (
#     pivot[list(big_code.keys())]
#     .reset_index()
#     .groupby("지역")
#     .mean(numeric_only=True)
#     .reset_index()
# )

# # (8) 차량/고용자 비율 평균 계산
# df_vehicle["차량/고용자"] = df_vehicle[["2021_차량", "2022_차량", "2023_차량"]].mean(axis=1)
# df_avg_vehicle = df_vehicle[["지역", "차량/고용자"]].copy()
# df_avg_vehicle.rename(columns={"차량/고용자": "차량_고용자"}, inplace=True)


# # (9) 병합
# df_merged = pd.merge(df_avg_industry, df_avg_vehicle, on="지역")


# resp = "차량_고용자"  # ← 주의: df_merged에도 이 컬럼명이 있어야 함!
# X_cols = list(big_code.keys())
# formula = f"{resp} ~ {' + '.join(X_cols)} - 1"

# model = smf.ols(formula=formula, data=df_merged).fit(cov_type="HC3")

# # (2) 표준화 회귀분석
# df_std = df_merged.copy()
# for col in X_cols + [resp]:
#     df_std[col] = (df_std[col] - df_std[col].mean()) / df_std[col].std()

# model_std = smf.ols(formula=formula, data=df_std).fit(cov_type="HC3")


# # (3) 다중공선성 지표 VIF

# vif = pd.Series({
#     name: variance_inflation_factor(model.model.exog, i)
#     for i, name in enumerate(model.model.exog_names)
# }).round(2)


# # (4) 회귀 계수 시각화
# coef = model.params
# se = model.bse
# df_c = pd.concat([coef, se], axis=1).reset_index()
# df_c.columns = ["변수", "coef", "se"]
# df_c["low95"] = df_c["coef"] - 1.96 * df_c["se"]
# df_c["high95"] = df_c["coef"] + 1.96 * df_c["se"]
# df_c["sig"] = df_c["low95"] * df_c["high95"] > 0
# df_plot = df_c.sort_values("coef", key=abs, ascending=False)

# # 시각화
# st.subheader("산업종류가 차량/고용자에 미치는 영향")
# fig, ax = plt.subplots(figsize=(8, 5))
# palette = df_plot["sig"].map({True: "tab:blue", False: "tab:gray"}).tolist()
# sns.barplot(x="coef", y="변수", data=df_plot, palette=palette, ax=ax)
# ax.errorbar(df_plot["coef"], range(len(df_plot)), xerr=1.96 * df_plot["se"],
#             fmt="none", ecolor="black", capsize=3)
# ax.axvline(0, color="red", linestyle="--")
# st.pyplot(fig)

# # 표 출력
# st.dataframe(
#     df_plot[["변수", "coef"]].round(3).rename(columns={
#         "coef": "β"
#     }),
#     hide_index=True
# )

from socket import MSG_BCAST
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import statsmodels.formula.api as smf
import platform
import re
from statsmodels.stats.outliers_influence import variance_inflation_factor

# 한국어 폰트 설정
plt.rcParams['axes.unicode_minus'] = False
if platform.system() == "Windows":
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == "Darwin":
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'DejaVu Sans'

st.set_page_config(
    page_title="통계 배경의 차량 등록수 및 고용/소득 구조",
    layout="centered"
)

st.markdown("""
    <div style='background-color:#1f77b4; padding: 1rem 2rem; border-radius: 10px;'>
        <h1 style='color: white;'>🚗 차량 등록 수와 고용/소득/산업 간 상관관계 분석</h1>
        <p style='color: white;'>2021~2023년 기준 평균값을 활용한 상관 분석 및 회귀 분석</p>
    </div>
    <br>
""", unsafe_allow_html=True)

# 데이터 로드 함수
@st.cache_data

def load_data():
    df_total    = pd.read_csv("./data/df_total.csv")
    df_income   = pd.read_csv("./data/df_income.csv")
    df_vehicle  = pd.read_csv("./data/df_vehicle.csv")
    df_industry = pd.read_csv("./data/df_industry.csv")
    return df_total, df_income, df_vehicle, df_industry

df_total, df_income, df_vehicle, df_industry = load_data()

# 파생 평균값 계산
st.markdown("---")
st.subheader("1️⃣ 차량 등록 수 vs 고용자 수")

# 평균 파생
years = ["2021", "2022", "2023"]
df_total["평균_고용자"] = df_total[years].mean(axis=1) / 10000
df_income["평균_소득"] = df_income[[f"{y}_소득" for y in years]].mean(axis=1)
df_vehicle["평균_차량"] = df_vehicle[[f"{y}_차량" for y in years]].mean(axis=1) / 10000

# 고용자 수 vs 차량 등록 수
df1 = df_total[["지역", "평균_고용자"]].merge(df_vehicle[["지역", "평균_차량"]], on="지역")
r1, p1 = pearsonr(df1["평균_고용자"], df1["평균_차량"])
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.regplot(x="평균_고용자", y="평균_차량", data=df1, ax=ax1, scatter=False)
ax1.scatter(df1["평균_고용자"], df1["평균_차량"], alpha=0.7)
for _, row in df1.iterrows():
    name = re.sub(r"(특별시|광역시|특별자치시|특별자치도)$", "", row["지역"])
    ax1.annotate(name, (row["평균_고용자"], row["평균_차량"]), xytext=(5, 5), textcoords='offset points', fontsize=8)
ax1.set_title(f"상관계수 r = {r1:.2f}, p = {p1:.3g}")
ax1.set_xlabel("평균 고용자 수 (만 명)")
ax1.set_ylabel("평균 차량 등록 수 (만 대)")
st.pyplot(fig1)

with st.expander("📋 고용자-차량 수치 보기"):
    st.dataframe(df1.rename(columns={"평균_고용자": "평균 고용자 수 (만 명)", "평균_차량": "평균 차량 등록 수 (만 대)"}))

# 지역소득 vs 차량
st.markdown("---")
st.subheader("2️⃣ 차량 등록 수 vs 1인당 지역소득")

df2 = df_income[["지역", "평균_소득"]].merge(df_vehicle[["지역", "평균_차량"]], on="지역")
r2, p2 = pearsonr(df2["평균_소득"], df2["평균_차량"])
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.regplot(x="평균_소득", y="평균_차량", data=df2, ax=ax2, scatter=False)
ax2.scatter(df2["평균_소득"], df2["평균_차량"], alpha=0.7)
for _, row in df2.iterrows():
    name = re.sub(r"(특별시|광역시|특별자치시|특별자치도)$", "", row["지역"])
    ax2.annotate(name, (row["평균_소득"], row["평균_차량"]), xytext=(5, 5), textcoords='offset points', fontsize=8)
ax2.set_title(f"상관계수 r = {r2:.2f}, p = {p2:.3g}")
ax2.set_xlabel("평균 1인당 소득 (천 원)")
ax2.set_ylabel("평균 차량 등록 수 (만 대)")
st.pyplot(fig2)

with st.expander("📋 소득-차량 수치 보기"):
    st.dataframe(df2.rename(columns={"평균_소득": "평균 1인당 소득 (천 원)", "평균_차량": "평균 차량 등록 수 (만 대)"}))

# 회귀분석용 산업코드 파생
st.markdown("---")
st.subheader("3️⃣ 산업 비중별 차량/고용자 비율 영향 분석")

df_industry_long = df_industry.melt(id_vars=["지역", "산업분류"], var_name="연도", value_name="종사자수")
df_industry_long["산업코드"] = df_industry_long["산업분류"].str.extract(r"(^[A-Z]\.)")
total = df_industry_long.groupby(["지역", "연도"])["종사자수"].sum().reset_index(name="전체")
df_industry_long = df_industry_long.merge(total, on=["지역", "연도"])
df_industry_long["비중"] = df_industry_long["종사자수"] / df_industry_long["전체"]

pivot = df_industry_long.pivot_table(index=["지역", "연도"], columns="산업코드", values="비중", aggfunc="sum")

big_code = {
    "제조_에너지_건설": ["B.", "C.", "D.", "E.", "F."],
    "유통_물류":         ["G.", "H."],
    "민간서비스_금융":   ["I.", "J.", "K.", "L.", "M.", "N.", "R.", "S."],
    "공공_사회서비스":   ["O.", "P.", "Q."]
}

for group, codes in big_code.items():
    pivot[group] = pivot[[col for col in pivot.columns if col in codes]].sum(axis=1)

avg_industry = pivot[list(big_code.keys())].reset_index().groupby("지역").mean(numeric_only=True).reset_index()
df_vehicle["차량_고용자"] = df_vehicle[[f"{y}_차량" for y in years]].mean(axis=1)
df_reg = avg_industry.merge(df_vehicle[["지역", "차량_고용자"]], on="지역")

X_cols = list(big_code.keys())
formula = f"차량_고용자 ~ {' + '.join(X_cols)} -1"
model = smf.ols(formula, df_reg).fit(cov_type="HC3")

# 계수 시각화
coef_df = model.params.to_frame("coef").join(model.bse.to_frame("se"))
coef_df["low"] = coef_df["coef"] - 1.96 * coef_df["se"]
coef_df["high"] = coef_df["coef"] + 1.96 * coef_df["se"]
coef_df["sig"] = coef_df["low"] * coef_df["high"] > 0
coef_df = coef_df.reset_index().rename(columns={"index": "변수"})

# sig 컬럼을 문자로 변환
coef_df["sig_label"] = coef_df["sig"].map({True: "유의함", False: "비유의"})

# 시각화
fig3, ax3 = plt.subplots(figsize=(8, 5))
sns.barplot(
    x="coef", y="변수",
    data=coef_df,
    hue="sig_label",
    dodge=False,
    palette={"유의함": "tab:blue", "비유의": "tab:gray"},
    ax=ax3
)
ax3.errorbar(
    coef_df["coef"], range(len(coef_df)),
    xerr=1.96 * coef_df["se"],
    fmt="none", ecolor="black", capsize=3
)
ax3.axvline(0, color="red", linestyle="--")
ax3.legend(title="유의성", loc="lower right")

ax3.errorbar(coef_df["coef"], coef_df.index, xerr=1.96*coef_df["se"], fmt="none", color="black", capsize=3)
ax3.axvline(0, color="red", linestyle="--")
ax3.set_title("산업별 비중이 차량/고용자 수에 미치는 영향")

st.pyplot(fig3)

with st.expander("📋 회귀 분석 계수 보기"):
    st.dataframe(coef_df[["변수", "coef"]].rename(columns={"coef": "β"}).round(3), hide_index=True)

st.caption("출처: 통계청, 고용노동부, 자체 가공")
