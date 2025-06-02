import streamlit as st
import calendar
import datetime
import pandas as pd
import os
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="2025 학습계획표", layout="wide")
st.title("📘 2025년 학습 계획표 안내")
st.markdown("날짜를 클릭하고 일정을 입력한 뒤 **✅ 일정 입력** 버튼을 누르세요.")

# 🔹 CSV 불러오기 + 인코딩 오류 자동 처리
csv_file = "plan.csv"
if os.path.exists(csv_file):
    try:
        df = pd.read_csv(csv_file, encoding="utf-8-sig")
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(csv_file, encoding="cp949")
        except Exception as e:
            st.error(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
            df = pd.DataFrame(columns=["날짜", "계획"])
else:
    df = pd.DataFrame(columns=["날짜", "계획"])

plan_dict = dict(zip(df["날짜"], df["계획"]))

# 🔸 현재 월 자동 선택
today = datetime.date.today()
default_month = today.month if 3 <= today.month <= 12 else 3
selected_month = st.selectbox("월 선택", list(range(3, 13)), index=default_month - 3, format_func=lambda x: f"{x}월")
year = 2025
month = selected_month

# 클릭된 날짜 저장용 상태 초기화
if "clicked_date" not in st.session_state:
    st.session_state.clicked_date = None

# 요일 헤더
weekdays = ["월", "화", "수", "목", "금", "토", "일"]
cols = st.columns(7)
for i in range(7):
    cols[i].markdown(f"**{weekdays[i]}**")

# 달력 날짜 생성
cal = calendar.Calendar(firstweekday=0)  # 월요일 시작
dates = [day for day in cal.itermonthdates(year, month) if day.month == month]

# 달력 출력
for week_start in range(0, len(dates), 7):
    cols = st.columns(7)
    for i in range(7):
        if week_start + i < len(dates):
            d = dates[week_start + i]
            str_date = str(d)
            plan = plan_dict.get(str_date, "")
            weekday = d.weekday()

            # 요일 색상 지정
            if weekday == 5:
                color = "#0066cc"  # 토
            elif weekday == 6:
                color = "#cc0000"  # 일
            else:
                color = "#000000"  # 평일

            label = f"<span style='color:{color}; font-weight:bold;'>{d.day}</span>"
            if plan:
                button_html = f"""
                <button style='background-color:#d0e8ff;padding:8px;border:none;border-radius:6px;width:100%;cursor:pointer;' 
                        onclick="window.location.href='?clicked_date={str_date}'">
                    {label}<br><span style='font-size:10px;'>{plan[:12]}</span>
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

# 🔹 클릭된 날짜 상태 저장
query_params = st.query_params
clicked = query_params.get("clicked_date", [None])[0]
if clicked:
    st.session_state.clicked_date = clicked

# 🔹 일정 입력 UI
clicked_date = st.session_state.clicked_date
if clicked_date:
    try:
        dt = datetime.datetime.strptime(clicked_date, "%Y-%m-%d").date()
        st.markdown(f"### ✍️ {dt.strftime('%Y년 %m월 %d일')} 일정 입력")
        previous = plan_dict.get(clicked_date, "")
        plan_input = st.text_area("학습 계획을 입력하세요", value=previous, height=150)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ 일정 입력"):
                df = df[df["날짜"] != clicked_date]
                df = pd.concat([df, pd.DataFrame([{"날짜": clicked_date, "계획": plan_input}])], ignore_index=True)
                df.to_csv(csv_file, index=False, encoding="utf-8-sig")
                st.success("일정이 저장되었습니다.")
                st.rerun()

        with col2:
            if st.button("❌ 입력 취소"):
                st.session_state.clicked_date = None
                st.rerun()

    except Exception as e:
        st.warning(f"날짜 파싱 오류: {e}")

# 🔹 PDF 생성 함수
def create_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "2025 학습 계획표", ln=True, align="C")
    pdf.ln(5)

    for _, row in df.iterrows():
        date_str = row["날짜"]
        plan_text = row["계획"]
        pdf.multi_cell(0, 10, f"📅 {date_str} - {plan_text}")
        pdf.ln(1)

    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

# 🔻 PDF 다운로드
with st.expander("📄 계획 PDF 다운로드"):
    if not df.empty:
        pdf_file = create_pdf(df.sort_values("날짜"))
        st.download_button(
            label="📥 PDF 다운로드",
            data=pdf_file,
            file_name="2025_학습계획표.pdf",
            mime="application/pdf"
        )
    else:
        st.info("먼저 계획을 입력하세요.")

# 🔹 전체 계획표 보기
with st.expander("📋 전체 계획 보기"):
    if not df.empty:
        st.dataframe(df.sort_values("날짜"), use_container_width=True)
    else:
        st.info("아직 저장된 계획이 없습니다.")
