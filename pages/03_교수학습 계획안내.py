import streamlit as st
import calendar
import datetime
import pandas as pd
import os

st.set_page_config(page_title="2025 학습계획표", layout="wide")

st.title("📘 2025년 학습 계획표 안내")
st.markdown("학생 여러분, 날짜를 클릭하고 일정을 입력한 뒤 **✅ 일정 입력** 버튼을 눌러주세요!")

# 파일 설정
SAVE_FILE = "calendar_plan_2025.csv"

# 기존 데이터 불러오기
if os.path.exists(SAVE_FILE):
    df = pd.read_csv(SAVE_FILE)
else:
    df = pd.DataFrame(columns=["날짜", "계획"])

plan_dict = dict(zip(df["날짜"], df["계획"]))

# 현재 월을 기본으로 설정
today = datetime.date.today()
default_month = today.month if 3 <= today.month <= 12 else 3
selected_month = st.selectbox("📅 월을 선택하세요", list(range(3, 13)), index=default_month - 3, format_func=lambda x: f"{x}월")
year = 2025
month = selected_month

# 요일 제목
weekdays = ["월", "화", "수", "목", "금", "토", "일"]
cols = st.columns(7)
for i in range(7):
    cols[i].markdown(f"**{weekdays[i]}**")

# 달력 생성
cal = calendar.Calendar(firstweekday=0)  # 월요일 시작
dates = [day for day in cal.itermonthdates(year, month) if day.month == month]

# 클릭된 날짜 기억
if "clicked_date" not in st.session_state:
    st.session_state.clicked_date = None

# 달력 표시
for week_start in range(0, len(dates), 7):
    cols = st.columns(7)
    for i in range(7):
        if week_start + i < len(dates):
            d = dates[week_start + i]
            str_date = str(d)
            plan = plan_dict.get(str_date, "")
            weekday = d.weekday()  # 월=0, ... 일=6

            # 요일별 색상
            if weekday == 5:
                color = "#0066cc"  # 토요일 파랑
            elif weekday == 6:
                color = "#cc0000"  # 일요일 빨강
            else:
                color = "#000000"  # 평일 검정

            label = f"<span style='color:{color}; font-weight:bold;'>{d.day}</span>"
            if plan:
                button_html = f"""
                <button style='background-color:#d0e8ff;padding:8px;border:none;border-radius:6px;width:100%;cursor:pointer;' 
                        onclick="window.location.href='?clicked_date={str_date}'">
                    {label}<br><span style='font-size:10px;'>{plan[:10]}</span>
                </button>
                """
            else:
                button_html = f"""
                <button style='background-color:#f0f0f0;padding:8px;border:none;border-radius:6px;width:100%;cursor:pointer;' 
                        onclick="window.location.href='?clicked_date={str_date}'">
                    {label}
                </button>
                """
            cols[i].markdown(button_html, unsafe_allow_html=True)

# URL 파라미터에서 클릭된 날짜 받아오기
query_params = st.query_params
clicked = query_params.get("clicked_date", [None])[0]
if clicked:
    st.session_state.clicked_date = clicked

# 일정 입력 폼
clicked_date = st.session_state.clicked_date
if clicked_date:
    try:
        dt = datetime.datetime.strptime(clicked_date, "%Y-%m-%d").date()
        st.markdown(f"### ✍️ {dt.strftime('%Y년 %m월 %d일')} 일정 입력")
        previous = plan_dict.get(clicked_date, "")
        plan_input = st.text_area("학습 계획을 입력하세요", value=previous, height=150)

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("✅ 일정 입력"):
                df = df[df["날짜"] != clicked_date]
                df = pd.concat([df, pd.DataFrame([{"날짜": clicked_date, "계획": plan_input}])], ignore_index=True)
                df.to_csv(SAVE_FILE, index=False, encoding="utf-8-sig")
                st.success("저장 완료! 달력에 반영되었습니다.")
                st.rerun()

        with col2:
            if st.button("❌ 입력 취소"):
                st.session_state.clicked_date = None
                st.rerun()

    except Exception as e:
        st.warning("날짜 형식이 잘못되었습니다.")

# 전체 보기
with st.expander("📄 전체 계획 보기"):
    if not df.empty:
        st.dataframe(df.sort_values("날짜"), use_container_width=True)
    else:
        st.info("아직 저장된 계획이 없습니다.")
