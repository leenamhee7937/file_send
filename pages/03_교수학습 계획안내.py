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
""", unsafe_allow_html=True)

# CSV 저장 경로
SAVE_FILE = "calendar_plan_2025.csv"

# 데이터 로딩
if os.path.exists(SAVE_FILE):
    df = pd.read_csv(SAVE_FILE)
else:
    df = pd.DataFrame(columns=["날짜", "계획"])

# 월 선택
selected_month = st.selectbox("📅 월을 선택하세요", list(range(3, 13)), format_func=lambda x: f"{x}월")
year = 2025
month = selected_month
cal = calendar.Calendar()

# 해당 월 날짜 가져오기
dates = [day for day in cal.itermonthdates(year, month) if day.month == month]
plan_dict = dict(zip(df["날짜"], df["계획"]))

# 요일 표시
st.markdown(f"## 🗓️ {year}년 {month}월")
weekdays = ["월", "화", "수", "목", "금", "토", "일"]
cols = st.columns(7)
for i in range(7):
    cols[i].markdown(f"**{weekdays[i]}**")

# 날짜 클릭 처리용 변수
query_params = st.query_params
clicked_date = query_params.get("clicked_date", None)

# 달력 그리기
for week_start in range(0, len(dates), 7):
    cols = st.columns(7)
    for i in range(7):
        if week_start + i < len(dates):
            d = dates[week_start + i]
            str_date = str(d)
            plan_text = plan_dict.get(str_date, "")

            # 요일 색상 처리 (월=0, ..., 일=6)
            weekday = d.weekday()
            if weekday == 5:  # 토요일
                color = "#0066cc"  # 파랑
            elif weekday == 6:  # 일요일
                color = "#cc0000"  # 빨강
            else:
                color = "#000000"  # 검정

            # 날짜 표시 텍스트
            label = f"<span style='color:{color}; font-weight:bold;'>{d.day}</span>"

            # 버튼 HTML 생성
            if plan_text:
                button_html = f"""
                <button style='background-color:#d0e8ff;padding:8px;border:none;border-radius:5px;width:100%;cursor:pointer;' 
                        onclick="window.location.href='?clicked_date={str_date}'">
                    {label}<br><span style='font-size:10px;'>{plan_text[:10]}</span>
                </button>
                """
            else:
                button_html = f"""
                <button style='background-color:#f0f0f0;padding:8px;border:none;border-radius:5px;width:100%;cursor:pointer;' 
                        onclick="window.location.href='?clicked_date={str_date}'">
                    {label}
                </button>
                """
            cols[i].markdown(button_html, unsafe_allow_html=True)

# 입력 UI
if clicked_date:
    try:
        clicked_dt = datetime.datetime.strptime(clicked_date, "%Y-%m-%d").date()
    except ValueError:
        clicked_dt = None

    if clicked_dt:
        st.markdown(f"### ✍️ {clicked_dt.strftime('%Y년 %m월 %d일')} 학습 계획 입력")
        prev = plan_dict.get(clicked_date, "")
        new_plan = st.text_area("학습 계획", value=prev, height=150)

        if st.button("저장", key="save"):
            # 저장 처리
            df = df[df["날짜"] != clicked_date]
            df = pd.concat([df, pd.DataFrame([{"날짜": clicked_date, "계획": new_plan}])], ignore_index=True)
            df.to_csv(SAVE_FILE, index=False, encoding="utf-8-sig")
            st.success("계획이 저장되었습니다.")
            st.rerun()

# 전체 보기
with st.expander("📄 전체 계획 보기"):
    if not df.empty:
        df_sorted = df.sort_values("날짜")
        st.dataframe(df_sorted, use_container_width=True)
    else:
        st.info("아직 저장된 계획이 없습니다.")
