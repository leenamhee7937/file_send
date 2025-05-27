import streamlit as st
import os

# 저장할 폴더 경로 (관리자 PC의 C드라이브)
save_folder = "C:/과제물"
os.makedirs(save_folder, exist_ok=True)

st.title("📄 과제 제출 시스템")

# 학번 입력
student_number = st.text_input("🔢 학번을 입력하세요:")

# 파일 업로드
uploaded_file = st.file_uploader("📎 제출할 파일을 첨부하세요")

# 제출 버튼
if st.button("제출하기"):
    if not student_number:
        st.warning("⚠️ 학번을 입력해주세요.")
    elif not uploaded_file:
        st.warning("⚠️ 파일을 첨부해주세요.")
    else:
        # 확장자 추출
        ext = os.path.splitext(uploaded_file.name)[1]
        filename = f"{student_number}{ext}"
        save_path = os.path.join(save_folder, filename)

        # 파일 저장
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success(f"✅ 제출 완료! 파일이 다음 위치에 저장되었습니다: {save_path}")
