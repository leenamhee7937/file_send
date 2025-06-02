import streamlit as st
import calendar
import datetime
import pandas as pd
import os

st.set_page_config(page_title="2025 학습계획표 안내", layout="wide")

st.title("📘 2025년 학습 계획표 안내")
st.markdown("""
### 🧑‍🏫 선생님 안내
학생 여러분, 아래 달력에서 각 날짜를 클릭하여 그날의 학습 계획을 직접 입력해보세요.  
성실하게 작성한 계획은 여러분의 자기주도학습 능력을 기르는 데 도움이 됩니다.
""")

# 저장 파일명
SAVE_FILE = "calendar_plan_2025.csv"

# 기존 데이터 로드
if os.path.exists(SAVE_FILE):
    df = pd.read_csv(SAVE_FILE)
else:
    df = pd.DataFrame(columns=["날짜", "계획"])

# 월 선택
selected_month = st.selectbox("📅 월을 선택하세요", list(range(3, 13)), format_func=lambda x: f"{x}월")

# 선택된 월의 달력 생성
year = 2025
month = selected_month
cal = calendar.Calendar()

# 날짜 선택 인터페이스
st.markdown(f"## 🗓️ {year}년 {month}월 달력")

dates = [day for day in cal.itermonthdates(year, month) if day.month == month]
cols = st.columns(7)
weekdays = ["월", "화", "수", "목", "금", "토", "일"]

# 요일 헤더 표시
for i in range(7):
    cols[i].markdown(f"**{weekdays[i]}**")

# 날짜 표기 + 입력 연결
clicked_date = None
for week_start in range(0, len(dates), 7):
    cols = st.columns(7)
    for i in range(7):
        if week_start + i < len(dates):
            d = dates[week_start + i]
            label = f"{d.day}"
            if cols[i].button(label, key=f"{d}"):
                clicked_date = d

# 입력 칸 표시
if clicked_date:
    st.markdown(f"### ✍️ {clicked_date.strftime('%Y년 %m월 %d일')} 학습 계획 입력")
    previous = df[df["날짜"] == str(clicked_date)]["계획"].values
    default_text = previous[0] if len(previous) > 0 else ""
    plan_text = st.text_area("학습 계획", value=default_text, height=150)

    if st.button("저장"):
        # 이전 계획 제거
        df = df[df["날짜"] != str(clicked_date)]
        df = pd.concat([df, pd.DataFrame([{"날짜": str(clicked_date), "계획": plan_text}])], ignore_index=True)
        df.to_csv(SAVE_FILE, index=False, encoding="utf-8-sig")
        st.success("계획이 저장되었습니다.")

# 전체 계획 보기
with st.expander("📄 저장된 학습 계획 전체 보기"):
    if not df.empty:
        df_sorted = df.sort_values("날짜")
        st.dataframe(df_sorted, use_container_width=True)
    else:
        st.info("아직 저장된 계획이 없습니다.")
