from fpdf import FPDF
import streamlit as st
from datetime import datetime
import os

# PDF 저장 함수
def save_to_pdf(student_id, name, topic, content, learning, development):
    pdf = FPDF()
    pdf.add_page()
    
    # 폰트 경로 지정 (같은 디렉터리에 파일이 있다고 가정)
    font_path = "NotoSansKR-Regular.ttf"
    
    if not os.path.exists(font_path):
        st.error(f"폰트 파일이 없습니다: {font_path}")
        return
    
    pdf.add_font('NotoSans', '', font_path, uni=True)
    pdf.set_font('NotoSans', '', 14)
    
    pdf.cell(200, 10, txt="수업 일기", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"학번: {student_id}", ln=True)
    pdf.cell(200, 10, txt=f"이름: {name}", ln=True)
    pdf.cell(200, 10, txt=f"날짜: {datetime.today().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"수업 주제: {topic}")
    pdf.multi_cell(0, 10, f"수업 내용: {content}")
    pdf.multi_cell(0, 10, f"학습 내용: {learning}")
    pdf.multi_cell(0, 10, f"향후 발전 방향: {development}")
    
    filename = f"{student_id}_{name}_수업일기.pdf"
    pdf.output(filename)
    st.success(f"{filename} 파일로 저장되었습니다.")

# Streamlit UI
st.title("📘 수업 일기 작성")

student_id = st.text_input("학번")
name = st.text_input("이름")
topic = st.text_input("수업 주제", max_chars=80)
content = st.text_area("수업 내용 (200자 이내)", max_chars=200)
learning = st.text_area("학습 내용 (200자 이내)", max_chars=200)
development = st.text_area("향후 발전 방향 (200자 이내)", max_chars=200)

if st.button("저장하기"):
    if not student_id or not name:
        st.warning("학번과 이름을 입력해주세요.")
    else:
        save_to_pdf(student_id, name, topic, content, learning, development)
