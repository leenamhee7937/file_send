import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

# 저장할 폴더 생성
save_folder = "C:/수업일기"
os.makedirs(save_folder, exist_ok=True)

st.title("📘 수업 일기 작성")

# 기본 입력
student_number = st.text_input("🔢 학번", max_chars=10)
student_name = st.text_input("👤 이름", max_chars=10)
today_date = datetime.now().strftime("%Y-%m-%d")
st.markdown(f"📅 **날짜**: `{today_date}`")

# 수업 정보 입력
topic = st.text_input("📝 수업 주제", max_chars=50)
content = st.text_area("📚 수업 내용 요약 (100자 내외)", max_chars=200, height=100)
learning = st.text_area("🔍 학습 과정 및 배움 (태도, 협력, 노력 과정 위주로 200자 내외)", max_chars=200, height=100)
future = st.text_area("🚀 향후 발전 방향 및 더 탐구해보고 싶은 부분 (200자 내외)", max_chars=200, height=100)

# 저장 버튼
if st.button("💾 저장하기"):
    if not student_number or not student_name or not topic:
        st.warning("❗ 학번, 이름, 수업 주제는 필수 입력입니다.")
    else:
        # 파일 이름 설정
        filename = f"{student_number}_{student_name}_{today_date}.pdf"
        filepath = os.path.join(save_folder, filename)

        # PDF 작성
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('ArialUnicode', '', 'arialuni.ttf', uni=True)  # 한글 폰트 필요 시 추가
        pdf.set_font("ArialUnicode", size=12)

        pdf.cell(200, 10, txt="📘 수업 일기", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"학번: {student_number}   이름: {student_name}   날짜: {today_date}", ln=True)
        pdf.ln(5)
        pdf.multi_cell(0, 10, txt=f"📝 수업 주제: {topic}")
        pdf.ln(3)
        pdf.multi_cell(0, 10, txt=f"📚 수업 내용:\n{content}")
        pdf.ln(3)
        pdf.multi_cell(0, 10, txt=f"🔍 학습 내용:\n{learning}")
        pdf.ln(3)
        pdf.multi_cell(0, 10, txt=f"🚀 향후 발전 방향:\n{future}")

        # PDF 저장
        pdf.output(filepath)
        st.success(f"✅ PDF로 저장되었습니다: {filepath}")
